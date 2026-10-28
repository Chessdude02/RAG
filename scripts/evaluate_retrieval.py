"""Evaluate retrieval quality via precision@5 against a labeled test set.

Compares the naive dense-only baseline (retrieve_relevant_chunks) against the
hybrid dense+BM25+RRF+rerank pipeline (hybrid_retrieve) on precision@5 and
end-to-end latency, and scores the hybrid pipeline's generated answers for
faithfulness against their retrieved context:

- answer-level: does every claim hold up (one yes/no per answer, same prompt
  as before, so it compares with earlier results);
- claim-level: the answer is split into single claims and each is judged
  supported / not supported / contradicted.

Both scorers live in the eval-harness repo (eval/faithfulness.py); this script
only runs the pipeline and hands them {question, contexts, answer} records.
Judge calls are cached on disk (eval/cache/judge/), and every Claude call in
the run -- generation included -- counts toward a hard cost cap that stops the
run. Results are written to eval/results/faithfulness_<test set>.json.

Usage:
    python scripts/evaluate_retrieval.py                       # data/eval/test_questions.json
    python scripts/evaluate_retrieval.py eval/questions.jsonl  # verified questions only
    python scripts/evaluate_retrieval.py --judge-model claude-sonnet-5 --cost-cap 3  # Step 1's judge
"""
import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVAL_HARNESS_DIR = Path(
    os.environ.get("EVAL_HARNESS_DIR", ROOT.parent.parent / "eval-harness")
)
sys.path.insert(0, str(EVAL_HARNESS_DIR))

from eval.budget import BudgetedClient, CostCapExceeded, CostTracker, JudgeCache  # noqa: E402
from eval.faithfulness import aggregate, score_record  # noqa: E402

from query_rag import (  # noqa: E402
    GENERATION_MODEL,
    build_context,
    generate_answer,
    get_llm_client,
    hybrid_retrieve,
    retrieve_relevant_chunks,
)

DEFAULT_TEST_SET = ROOT / "data" / "eval" / "test_questions.json"
RESULTS_DIR = ROOT / "eval" / "results"
JUDGE_CACHE_DIR = ROOT / "eval" / "cache" / "judge"
# ministral-8b-latest agreed best with human labels in the Mistral round of Step 2
# (binary kappa 0.7431 vs 0.6504 for ministral-3b-latest; eval/results/judge_agreement.json).
# The Claude round picked claude-opus-5-5 (judge_agreement_claude.json). Step 1's saved
# results were judged by claude-sonnet-5; pass --judge-model claude-sonnet-5 to reproduce them.
DEFAULT_JUDGE_MODEL = "ministral-8b-latest"
DEFAULT_COST_CAP_USD = float(os.environ.get("EVAL_COST_CAP_USD", "5"))
TOP_K = 5


def load_test_set(path: Path) -> list[dict]:
    """A JSON list of {question, relevant_chunk_ids}, or a JSONL file in the
    eval/questions.jsonl format, of which only `verified` rows are used."""
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found. Expected a JSON list of "
            '{"question": "...", "relevant_chunk_ids": ["..."]} objects, or a JSONL file.'
        )
    with open(path, "r", encoding="utf-8") as f:
        if path.suffix == ".jsonl":
            rows = [json.loads(line) for line in f if line.strip()]
            return [r for r in rows if r.get("verified")]
        return json.load(f)


def precision_at_k(retrieved_ids: list[str], relevant_ids: set[str], k: int) -> float:
    top_k = retrieved_ids[:k]
    if not top_k:
        return 0.0
    hits = sum(1 for chunk_id in top_k if chunk_id in relevant_ids)
    return hits / len(top_k)


def evaluate(test_set: list[dict], client, judge_model: str, cache: JudgeCache, k: int = TOP_K) -> dict:
    per_question = []
    failures = []
    stopped = None

    for item in test_set:
        question = item["question"]
        relevant_ids = set(item["relevant_chunk_ids"])

        try:
            naive_start = time.perf_counter()
            naive_chunks = retrieve_relevant_chunks(question, n_results=k)
            naive_answer = generate_answer(question, naive_chunks, client)
            naive_latency = time.perf_counter() - naive_start
            naive_ids = [chunk["chunk_id"] for chunk in naive_chunks]
            naive_precision = precision_at_k(naive_ids, relevant_ids, k)

            hybrid_start = time.perf_counter()
            hybrid_chunks = hybrid_retrieve(question, k=k)
            hybrid_answer = generate_answer(question, hybrid_chunks, client)
            hybrid_latency = time.perf_counter() - hybrid_start
            hybrid_ids = [chunk["chunk_id"] for chunk in hybrid_chunks]
            hybrid_precision = precision_at_k(hybrid_ids, relevant_ids, k)

            # One context string per chunk, formatted exactly as the generator saw it.
            record = {
                "question": question,
                "contexts": [build_context([chunk]) for chunk in hybrid_chunks],
                "answer": hybrid_answer,
            }
            faithfulness = score_record(record, client, judge_model, cache)

            per_question.append(
                {
                    "id": item.get("id"),
                    "question": question,
                    "relevant_chunk_ids": sorted(relevant_ids),
                    "naive_retrieved_chunk_ids": naive_ids,
                    "naive_precision": naive_precision,
                    "naive_latency": naive_latency,
                    "hybrid_retrieved_chunk_ids": hybrid_ids,
                    "hybrid_precision": hybrid_precision,
                    "hybrid_latency": hybrid_latency,
                    "hybrid_answer": hybrid_answer,
                    "is_faithful": faithfulness["answer_level"]["is_faithful"],
                    "unsupported_claims": faithfulness["answer_level"]["unsupported_claims"],
                    "claims": faithfulness["claims"],
                    "n_claims": faithfulness["n_claims"],
                    "claim_support_rate": faithfulness["claim_support_rate"],
                    "faithfulness_score": faithfulness,
                }
            )
        except CostCapExceeded as exc:
            stopped = str(exc)
            print(f"STOPPED: {exc}")
            break
        except Exception as exc:
            print(f"ERROR: question failed, skipping: {question!r} -> {exc!r}")
            failures.append({"question": question, "error": repr(exc)})
            continue

    n = len(per_question) or 1
    return {
        "k": k,
        "per_question": per_question,
        "failures": failures,
        "stopped_early": stopped,
        "mean_naive_precision": sum(r["naive_precision"] for r in per_question) / n,
        "mean_hybrid_precision": sum(r["hybrid_precision"] for r in per_question) / n,
        "mean_naive_latency": sum(r["naive_latency"] for r in per_question) / n,
        "mean_hybrid_latency": sum(r["hybrid_latency"] for r in per_question) / n,
        "faithfulness_rate": sum(1 for r in per_question if r["is_faithful"]) / n,
        "faithfulness": aggregate([r["faithfulness_score"] for r in per_question]),
    }


def print_report(report: dict) -> None:
    k = report["k"]
    for r in report["per_question"]:
        print(f"Q: {r['question']}")
        print(f"  precision@{k}   naive: {r['naive_precision']:.2f}   hybrid: {r['hybrid_precision']:.2f}")
        print(f"  latency (s)     naive: {r['naive_latency']:.2f}   hybrid: {r['hybrid_latency']:.2f}")
        print(f"  relevant:       {r['relevant_chunk_ids']}")
        print(f"  naive retrieved:  {r['naive_retrieved_chunk_ids']}")
        print(f"  hybrid retrieved: {r['hybrid_retrieved_chunk_ids']}")
        print(f"  faithful: {'yes' if r['is_faithful'] else 'no'}")
        if not r["is_faithful"] and r["unsupported_claims"]:
            print(f"    unsupported claims: {r['unsupported_claims']}")
        for c in r["claims"]:
            if c["verdict"] != "supported":
                print(f"    claim {c['verdict']}: {c['claim']}")
        print()

    n = len(report["per_question"])
    f = report["faithfulness"]
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"{'Metric':<24}{'Naive':>15}{'Hybrid':>15}")
    print(f"{'Precision@' + str(k):<24}{report['mean_naive_precision']:>15.4f}{report['mean_hybrid_precision']:>15.4f}")
    print(f"{'Avg latency (s)':<24}{report['mean_naive_latency']:>15.4f}{report['mean_hybrid_latency']:>15.4f}")
    print()
    print(f"Faithfulness rate (hybrid answers, n={n}): {report['faithfulness_rate']:.4f}")
    print(
        f"Claim-level: {f['n_supported']}/{f['n_claims']} claims supported "
        f"(micro {f['claim_support_rate_micro']}), {f['n_not_supported']} not supported, "
        f"{f['n_contradicted']} contradicted; "
        f"{f['answers_all_claims_supported']}/{f['n_answers_with_claims']} answers with every claim supported"
    )
    print(f"Models: generator={report['generator_model']} judge={report['judge_model']}")
    print(f"Cost: {report['cost']}")

    failures = report["failures"]
    if failures:
        print()
        print(f"Failed questions ({len(failures)}, excluded from the metrics above):")
        for fail in failures:
            print(f"  - {fail['question']!r}: {fail['error']}")
    if report["stopped_early"]:
        print(f"\nRun stopped early by the cost cap: {report['stopped_early']}")


def _git_commit(path: Path) -> str | None:
    try:
        return subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=path, capture_output=True, text=True, check=True
        ).stdout.strip()
    except Exception:
        return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("test_set", nargs="?", type=Path, default=DEFAULT_TEST_SET)
    parser.add_argument("--judge-model", default=DEFAULT_JUDGE_MODEL)
    parser.add_argument("--cost-cap", type=float, default=DEFAULT_COST_CAP_USD, help="USD; stops the run.")
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    test_set = load_test_set(args.test_set)
    tracker = CostTracker(cap_usd=args.cost_cap)
    client = BudgetedClient(get_llm_client(), tracker)
    cache = JudgeCache(JUDGE_CACHE_DIR)

    report = evaluate(test_set, client, args.judge_model, cache, k=TOP_K)
    report.update(
        {
            "test_set": args.test_set.resolve().relative_to(ROOT).as_posix(),
            "n_questions_in_set": len(test_set),
            "generator_model": GENERATION_MODEL,
            "judge_model": args.judge_model,
            "cost": tracker.summary(),
            "rag_pipeline_commit": _git_commit(ROOT),
            "eval_harness_commit": _git_commit(EVAL_HARNESS_DIR),
            "finished_at": datetime.now(timezone.utc).isoformat(),
        }
    )
    print_report(report)

    out = args.out or RESULTS_DIR / f"faithfulness_{args.test_set.stem}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nWrote {out}")
    if report["stopped_early"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
