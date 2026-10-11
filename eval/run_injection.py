"""Step 4 of the eval upgrade: prompt injection planted inside retrieved context.

The sets are the 40 unique questions from Step 1 (20 in data/eval/test_questions.json
and 20 verified in eval/questions.jsonl), each with the top-5 chunks the hybrid
retriever actually returned for it (read from Chroma by id). In each set, one
chunk gets a harmless instruction planted mid-text (eval/injection/payloads.json),
and the pipeline's own generation step (query_rag.generate_answer: same model,
system prompt and context format as production) answers the question.

Payload and chunk position are assigned independently: set i gets payload
i % 5 and the planted chunk at rank (i // 5) % 5, so each payload appears at
several ranks.

Scope: the planted text is inserted after retrieval, so this tests whether the
generator obeys instructions found in its context. It does not test whether
such a chunk would be retrieved, or the classifier / multi-hop path.

Each answer is checked by canary match and by the default judge (eval-harness
eval/injection.py). Follow rate = judge "followed" / n, with a Wilson 95% CI.

Usage:
    python eval/run_injection.py
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVAL_HARNESS_DIR = Path(os.environ.get("EVAL_HARNESS_DIR", ROOT.parent.parent / "eval-harness"))
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "eval"))
sys.path.insert(0, str(EVAL_HARNESS_DIR))

from eval.budget import BudgetedClient, CostCapExceeded, CostTracker, JudgeCache  # noqa: E402
from eval.injection import canary_present, judge_compliance, plant, summarize  # noqa: E402

from build_label_set import fetch_chunks  # noqa: E402
from evaluate_retrieval import DEFAULT_JUDGE_MODEL  # noqa: E402
from query_rag import ANTHROPIC_MODEL, generate_answer, get_anthropic_client  # noqa: E402

PAYLOADS_FILE = ROOT / "eval" / "injection" / "payloads.json"
STEP1_RESULTS = [
    ROOT / "eval" / "results" / "faithfulness_test_questions.json",
    ROOT / "eval" / "results" / "faithfulness_questions.json",
]
CACHE_DIR = ROOT / "eval" / "cache" / "judge"
OUT = ROOT / "eval" / "results" / "injection.json"
DEFAULT_COST_CAP_USD = 3.0


def load_sets() -> list[dict]:
    sets, seen = [], set()
    for path in STEP1_RESULTS:
        for row in json.loads(path.read_text(encoding="utf-8"))["per_question"]:
            if row["question"] in seen:
                continue
            seen.add(row["question"])
            sets.append({
                "source": path.name, "id": row.get("id"), "question": row["question"],
                "chunk_ids": row["hybrid_retrieved_chunk_ids"],
            })
    return sets


def _git_commit(path: Path) -> str | None:
    try:
        return subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=path, capture_output=True, text=True, check=True
        ).stdout.strip()
    except Exception:
        return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--judge-model", default=DEFAULT_JUDGE_MODEL)
    parser.add_argument("--cost-cap", type=float, default=DEFAULT_COST_CAP_USD, help="USD; stops the run.")
    args = parser.parse_args()

    payloads = json.loads(PAYLOADS_FILE.read_text(encoding="utf-8"))["payloads"]
    sets = load_sets()
    tracker = CostTracker(cap_usd=args.cost_cap)
    client = BudgetedClient(get_anthropic_client(), tracker)
    cache = JudgeCache(CACHE_DIR)

    results, stopped = [], None
    try:
        for i, s in enumerate(sets):
            payload = payloads[i % len(payloads)]
            chunks = fetch_chunks(s["chunk_ids"])
            rank = (i // len(payloads)) % len(chunks)
            chunks[rank] = {**chunks[rank], "text": plant(chunks[rank]["text"], payload["instruction"])}

            answer = generate_answer(s["question"], chunks, client)
            verdict = judge_compliance(s["question"], payload["instruction"], answer, client,
                                       args.judge_model, cache)
            results.append({
                **s, "payload_id": payload["id"], "planted_rank": rank + 1,
                "planted_chunk_id": chunks[rank]["chunk_id"], "answer": answer,
                "canary_hit": canary_present(answer, payload["canary"]), **verdict,
            })
            print(f"{i + 1:>2}/{len(sets)} {payload['id']:<16} rank {rank + 1}: {verdict['verdict']}"
                  f"{' (canary)' if results[-1]['canary_hit'] else ''}")
    except CostCapExceeded as exc:
        stopped = str(exc)
        print(f"STOPPED: {exc}")

    by_payload = defaultdict(list)
    by_rank = defaultdict(list)
    for r in results:
        by_payload[r["payload_id"]].append(r)
        by_rank[r["planted_rank"]].append(r)

    out = {
        "scope": "Instruction planted after retrieval into one of the real top-5 chunks; tests the "
                 "generation step (production model, system prompt and context format), not "
                 "retrieval of the poisoned chunk or the classifier/multi-hop path.",
        "generator_model": ANTHROPIC_MODEL,
        "judge_model": args.judge_model,
        "n_sets": len(results),
        "stopped_early": stopped,
        "summary": summarize(results) if results else None,
        "by_payload": {k: summarize(v) for k, v in by_payload.items()},
        "by_planted_rank": {k: summarize(v) for k, v in sorted(by_rank.items())},
        "canary_judge_mismatches": [
            {k: r[k] for k in ("question", "payload_id", "canary_hit", "verdict", "rationale")}
            for r in results if r["canary_hit"] != (r["verdict"] == "followed")
        ],
        "results": results,
        "cost": tracker.summary(),
        "rag_pipeline_commit": _git_commit(ROOT),
        "eval_harness_commit": _git_commit(EVAL_HARNESS_DIR),
        "finished_at": datetime.now(timezone.utc).isoformat(),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")

    s = out["summary"]
    print(f"\n{out['scope']}")
    print(f"n={s['n']}: {s['verdict_counts']}; follow rate {s['follow_rate']!r} "
          f"(Wilson 95% CI {s['follow_rate_ci95']}); canary hits {s['canary_hits']}; "
          f"canary/judge mismatches {s['canary_vs_judge_mismatches']}; answered question {s['answered_question']}")
    for k, v in out["by_payload"].items():
        print(f"  {k:<16} n={v['n']} {v['verdict_counts']}")
    for k, v in out["by_planted_rank"].items():
        print(f"  rank {k}: n={v['n']} {v['verdict_counts']}")
    print(f"Cost: {tracker.summary()}")
    print(f"Wrote {OUT}")
    if stopped:
        sys.exit(1)


if __name__ == "__main__":
    main()
