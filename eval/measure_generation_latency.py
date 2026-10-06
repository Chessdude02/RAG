"""Phase 2: generation-call latency (p50, p95), measured once (not per-environment).

This is the only script in Phase 2 that calls the Claude API. It measures pure
generation latency (the Claude API round trip) on a fixed sample of 10 questions,
repeated 3 times each (30 calls total, seed-independent sampling: first 10
verified questions in file order). Treated as an environment-independent
component of end-to-end latency, since it's dominated by network round-trip to
Anthropic's API rather than by which machine issues the request -- retrieval and
rerank latency (the CPU-bound, environment-dependent parts) are measured
separately in measure_latency.py, which makes no API calls.

Also records actual token usage and dollar cost from response.usage so the
report can state real spend, not an estimate.
"""
import json
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from query_rag import (  # noqa: E402
    ANTHROPIC_MODEL,
    MAX_TOKENS,
    SYSTEM_PROMPT,
    build_context,
    extract_text,
    get_anthropic_client,
    hybrid_retrieve,
)

QUESTIONS_PATH = Path(__file__).resolve().parent / "questions.jsonl"
RESULTS_PATH = Path(__file__).resolve().parent / "results" / "generation_latency.json"

N_QUERIES = 10
REPS = 3

# Sonnet 5 pricing, $/1M tokens (see eval/results/ for the model this pipeline uses)
INPUT_PRICE_PER_MTOK = 2.00
OUTPUT_PRICE_PER_MTOK = 10.00


def load_questions(path: Path) -> list[dict]:
    with open(path, "r", encoding="utf-8") as f:
        records = [json.loads(line) for line in f if line.strip()]
    verified = [r for r in records if r.get("verified")]
    return verified[:N_QUERIES]


def percentile(values: list[float], pct: float) -> float:
    values = sorted(values)
    if not values:
        return 0.0
    idx = (len(values) - 1) * pct
    lo, hi = int(idx), min(int(idx) + 1, len(values) - 1)
    frac = idx - lo
    return values[lo] + (values[hi] - values[lo]) * frac


def main() -> None:
    questions = load_questions(QUESTIONS_PATH)
    assert len(questions) == N_QUERIES, f"expected {N_QUERIES} verified questions, got {len(questions)}"

    client = get_anthropic_client()
    latencies = []
    input_tokens_total = 0
    output_tokens_total = 0
    calls_made = 0
    per_call = []

    print(f"Retrieving context for {N_QUERIES} questions (not timed; retrieval already measured separately)...")
    contexts = {q["id"]: hybrid_retrieve(q["question"], k=5) for q in questions}

    print(f"Making {N_QUERIES} x {REPS} = {N_QUERIES * REPS} generation calls...")
    for rep in range(REPS):
        for q in questions:
            chunks = contexts[q["id"]]
            t0 = time.perf_counter()
            _, usage = _generate_answer_with_usage(q["question"], chunks, client)
            t1 = time.perf_counter()
            calls_made += 1
            latency = t1 - t0
            latencies.append(latency)
            input_tokens_total += usage.input_tokens
            output_tokens_total += usage.output_tokens
            per_call.append({
                "id": q["id"],
                "rep": rep + 1,
                "latency_s": latency,
                "input_tokens": usage.input_tokens,
                "output_tokens": usage.output_tokens,
            })
            print(f"  [{calls_made}/{N_QUERIES * REPS}] {q['id']} rep {rep+1}: {latency:.2f}s "
                  f"({usage.input_tokens} in / {usage.output_tokens} out)")

    cost = (input_tokens_total / 1_000_000) * INPUT_PRICE_PER_MTOK + \
           (output_tokens_total / 1_000_000) * OUTPUT_PRICE_PER_MTOK

    summary = {
        "n_queries": N_QUERIES,
        "reps": REPS,
        "n_calls": calls_made,
        "model": ANTHROPIC_MODEL,
        "p50_s": percentile(latencies, 0.50),
        "p95_s": percentile(latencies, 0.95),
        "median_s": statistics.median(latencies),
        "mean_s": statistics.mean(latencies),
        "input_tokens_total": input_tokens_total,
        "output_tokens_total": output_tokens_total,
        "actual_cost_usd": round(cost, 4),
    }

    output = {"summary": summary, "per_call": per_call}
    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print(f"\np50: {summary['p50_s']:.2f}s   p95: {summary['p95_s']:.2f}s   median: {summary['median_s']:.2f}s")
    print(f"Actual cost: ${cost:.4f} ({calls_made} calls, {input_tokens_total} in / {output_tokens_total} out tokens)")
    print(f"Saved to {RESULTS_PATH}")


def _generate_answer_with_usage(query: str, chunks: list[dict], client):
    """Mirrors query_rag.generate_answer but also returns response.usage for cost tracking."""
    context = build_context(chunks)
    user_message = f"Context excerpts:\n\n{context}\n\n---\n\nQuestion: {query}"
    response = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=MAX_TOKENS,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )
    return extract_text(response), response.usage


if __name__ == "__main__":
    main()
