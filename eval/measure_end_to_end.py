"""End-to-end latency and API cost of answer_query on the current pipeline
(classifier + hybrid retrieval + routing + generation), with models and indexes
warmed up first so the numbers reflect steady-state serving.

Questions: the 20 verified single-paper questions in questions.jsonl plus the
10 multi-hop questions, so both routes are exercised.
"""
import json
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import query_rag  # noqa: E402

EVAL_DIR = Path(__file__).resolve().parent
RESULTS_PATH = EVAL_DIR / "results" / "end_to_end.json"

# claude-sonnet-5 list price, USD per million tokens (input, output).
PRICE_PER_MTOK = (2.00, 10.00)


def load(path: Path) -> list[dict]:
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def percentile(values: list[float], p: float) -> float:
    ordered = sorted(values)
    return ordered[min(len(ordered) - 1, round(p / 100 * (len(ordered) - 1)))]


def main() -> None:
    questions = [q for q in load(EVAL_DIR / "questions.jsonl") if q.get("verified")]
    questions += load(EVAL_DIR / "multihop_questions.jsonl")

    for warm in (query_rag.get_embedding_model, query_rag.get_cross_encoder,
                 query_rag.get_collection, query_rag.get_bm25_index):
        warm()

    # Count tokens on every Claude call answer_query makes (classify, decompose, generate).
    client = query_rag.get_anthropic_client()
    original_create = client.messages.create
    usage = {"input": 0, "output": 0}

    def counting_create(**kwargs):
        response = original_create(**kwargs)
        usage["input"] += response.usage.input_tokens
        usage["output"] += response.usage.output_tokens
        return response

    client.messages.create = counting_create

    rows = []
    for q in questions:
        usage.update(input=0, output=0)
        start = time.perf_counter()
        result = query_rag.answer_query(q["question"])
        elapsed = time.perf_counter() - start
        cost = (usage["input"] * PRICE_PER_MTOK[0] + usage["output"] * PRICE_PER_MTOK[1]) / 1e6
        rows.append({"id": q["id"], "classification": result["classification"],
                     "latency_s": round(elapsed, 2), "input_tokens": usage["input"],
                     "output_tokens": usage["output"], "cost_usd": round(cost, 5)})
        print(rows[-1], flush=True)

    def summarize(subset: list[dict]) -> dict:
        lat = [r["latency_s"] for r in subset]
        return {"n": len(subset), "p50_s": percentile(lat, 50), "p95_s": percentile(lat, 95),
                "mean_s": round(statistics.mean(lat), 2),
                "mean_cost_usd": round(statistics.mean(r["cost_usd"] for r in subset), 5)}

    summary = {"all": summarize(rows)}
    for cls in sorted({r["classification"] for r in rows}):
        summary[cls] = summarize([r for r in rows if r["classification"] == cls])
    print(json.dumps(summary, indent=2))

    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULTS_PATH.write_text(json.dumps({"summary": summary, "per_query": rows}, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
