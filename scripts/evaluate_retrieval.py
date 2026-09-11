"""Evaluate retrieval quality via precision@5 against a labeled test set.

Compares the naive dense-only baseline (retrieve_relevant_chunks) against the
hybrid dense+BM25+RRF+rerank pipeline (hybrid_retrieve) on precision@5 and
end-to-end latency, and reports a faithfulness rate for the hybrid pipeline's
generated answers (does every claim in the answer hold up against its context,
per a separate Claude judgment call).
"""
import json
import re
import sys
import time
from pathlib import Path

from query_rag import (
    ANTHROPIC_MODEL,
    build_context,
    extract_text,
    generate_answer,
    get_anthropic_client,
    hybrid_retrieve,
    retrieve_relevant_chunks,
)

DEFAULT_TEST_SET = Path(__file__).resolve().parent.parent / "data" / "eval" / "test_questions.json"
TOP_K = 5

FAITHFULNESS_PROMPT = """You are evaluating whether an AI-generated answer is fully \
supported by the provided context excerpts. Do not use any outside knowledge - judge \
only whether each claim in the answer follows from the context.

Context:
{context}

Answer:
{answer}

Respond in exactly this format, with no other text:
FAITHFUL: yes or no
UNSUPPORTED_CLAIMS: a semicolon-separated list of claims from the answer that are not \
supported by the context, or "none" if the answer is fully faithful."""


def load_test_set(path: Path) -> list[dict]:
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found. Expected a JSON list of "
            '{"question": "...", "relevant_chunk_ids": ["..."]} objects.'
        )
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def precision_at_k(retrieved_ids: list[str], relevant_ids: set[str], k: int) -> float:
    top_k = retrieved_ids[:k]
    if not top_k:
        return 0.0
    hits = sum(1 for chunk_id in top_k if chunk_id in relevant_ids)
    return hits / len(top_k)


def check_faithfulness(question: str, context: str, answer: str, client) -> dict:
    """Ask Claude to judge whether every claim in `answer` is supported by `context`."""
    prompt = FAITHFULNESS_PROMPT.format(context=context, answer=answer)
    response = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )

    try:
        text = extract_text(response)
    except ValueError:
        # TEMP DEBUG
        print("DEBUG check_faithfulness: extract_text failed")
        print(f"  question: {question}")
        print(f"  stop_reason: {response.stop_reason}")
        print(f"  content blocks ({len(response.content)}):")
        for i, block in enumerate(response.content):
            print(f"    [{i}] type={block.type!r} block={block!r}")
        raise

    faithful_match = re.search(r"FAITHFUL:\s*(yes|no)", text, re.IGNORECASE)
    is_faithful = faithful_match is not None and faithful_match.group(1).lower() == "yes"

    claims_match = re.search(r"UNSUPPORTED_CLAIMS:\s*(.*)", text, re.IGNORECASE | re.DOTALL)
    unsupported_claims = claims_match.group(1).strip() if claims_match else text.strip()
    if unsupported_claims.lower() == "none":
        unsupported_claims = ""

    return {"is_faithful": is_faithful, "unsupported_claims": unsupported_claims}


def evaluate(test_set: list[dict], k: int = TOP_K) -> dict:
    client = get_anthropic_client()
    per_question = []
    failures = []

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

            faithfulness = check_faithfulness(
                question, build_context(hybrid_chunks), hybrid_answer, client
            )

            per_question.append(
                {
                    "question": question,
                    "relevant_chunk_ids": sorted(relevant_ids),
                    "naive_retrieved_chunk_ids": naive_ids,
                    "naive_precision": naive_precision,
                    "naive_latency": naive_latency,
                    "hybrid_retrieved_chunk_ids": hybrid_ids,
                    "hybrid_precision": hybrid_precision,
                    "hybrid_latency": hybrid_latency,
                    "is_faithful": faithfulness["is_faithful"],
                    "unsupported_claims": faithfulness["unsupported_claims"],
                }
            )
        except Exception as exc:
            print(f"ERROR: question failed, skipping: {question!r} -> {exc!r}")
            failures.append({"question": question, "error": repr(exc)})
            continue

    n = len(per_question) or 1
    return {
        "k": k,
        "per_question": per_question,
        "failures": failures,
        "mean_naive_precision": sum(r["naive_precision"] for r in per_question) / n,
        "mean_hybrid_precision": sum(r["hybrid_precision"] for r in per_question) / n,
        "mean_naive_latency": sum(r["naive_latency"] for r in per_question) / n,
        "mean_hybrid_latency": sum(r["hybrid_latency"] for r in per_question) / n,
        "faithfulness_rate": sum(1 for r in per_question if r["is_faithful"]) / n,
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
        print()

    n = len(report["per_question"])
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"{'Metric':<24}{'Naive':>15}{'Hybrid':>15}")
    print(f"{'Precision@' + str(k):<24}{report['mean_naive_precision']:>15.4f}{report['mean_hybrid_precision']:>15.4f}")
    print(f"{'Avg latency (s)':<24}{report['mean_naive_latency']:>15.4f}{report['mean_hybrid_latency']:>15.4f}")
    print()
    print(
        f"Faithfulness rate (hybrid answers, n={n}): "
        f"{report['faithfulness_rate']:.4f}"
    )

    failures = report["failures"]
    if failures:
        print()
        print(f"Failed questions ({len(failures)}, excluded from the metrics above):")
        for f in failures:
            print(f"  - {f['question']!r}: {f['error']}")


if __name__ == "__main__":
    test_set_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_TEST_SET
    test_set = load_test_set(test_set_path)
    report = evaluate(test_set, k=TOP_K)
    print_report(report)
