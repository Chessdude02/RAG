"""Phase 2: retrieval + rerank latency (p50, p95), measured locally.

No LLM calls. Each stage is timed across all 60 questions, repeated REPS times
(>=3, per the project's measurement rules), and reported as p50/p95 over the
full sample (n = num_questions * REPS). Models are warmed up once before timing
starts so first-call load time doesn't pollute the measurements.
"""
import json
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from query_rag import (  # noqa: E402
    CANDIDATE_POOL,
    RRF_K,
    bm25_retrieve,
    get_bm25_index,
    get_collection,
    get_cross_encoder,
    get_embedding_model,
    rerank,
    retrieve_relevant_chunks,
)

QUESTIONS_PATH = Path(__file__).resolve().parent / "questions.jsonl"
RESULTS_PATH = Path(__file__).resolve().parent / "results" / "latency_local.json"
HARDWARE_PATH = Path(__file__).resolve().parent / "results" / "hardware.json"

REPS = 3


def load_questions(path: Path) -> list[dict]:
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def percentile(values: list[float], pct: float) -> float:
    values = sorted(values)
    if not values:
        return 0.0
    idx = (len(values) - 1) * pct
    lo, hi = int(idx), min(int(idx) + 1, len(values) - 1)
    frac = idx - lo
    return values[lo] + (values[hi] - values[lo]) * frac


def warm_up() -> None:
    get_embedding_model()
    get_cross_encoder()
    get_collection()
    get_bm25_index()
    q = "warm up query about retrieval augmented generation"
    retrieve_relevant_chunks(q, n_results=CANDIDATE_POOL)
    bm25_retrieve(q, n_results=CANDIDATE_POOL)


def measure(questions: list[dict]) -> dict:
    samples = {"dense_retrieval_s": [], "bm25_retrieval_s": [], "rerank_s": [], "hybrid_total_s": []}

    for rep in range(REPS):
        for q in questions:
            query = q["question"]

            t0 = time.perf_counter()
            dense_chunks = retrieve_relevant_chunks(query, n_results=CANDIDATE_POOL)
            t1 = time.perf_counter()
            samples["dense_retrieval_s"].append(t1 - t0)

            t0 = time.perf_counter()
            sparse_chunks = bm25_retrieve(query, n_results=CANDIDATE_POOL)
            t1 = time.perf_counter()
            samples["bm25_retrieval_s"].append(t1 - t0)

            rrf_scores: dict[str, float] = {}
            chunk_lookup: dict[str, dict] = {}
            for rank, chunk in enumerate(dense_chunks, start=1):
                cid = chunk["chunk_id"]
                rrf_scores[cid] = rrf_scores.get(cid, 0.0) + 1.0 / (RRF_K + rank)
                chunk_lookup[cid] = chunk
            for rank, chunk in enumerate(sparse_chunks, start=1):
                cid = chunk["chunk_id"]
                rrf_scores[cid] = rrf_scores.get(cid, 0.0) + 1.0 / (RRF_K + rank)
                chunk_lookup.setdefault(cid, chunk)
            pooled_ids = sorted(rrf_scores, key=lambda cid: rrf_scores[cid], reverse=True)[:CANDIDATE_POOL]
            pooled_chunks = [chunk_lookup[cid] for cid in pooled_ids]

            t0 = time.perf_counter()
            rerank(query, pooled_chunks, k=10)
            t1 = time.perf_counter()
            rerank_time = t1 - t0
            samples["rerank_s"].append(rerank_time)

            hybrid_total = samples["dense_retrieval_s"][-1] + samples["bm25_retrieval_s"][-1] + rerank_time
            samples["hybrid_total_s"].append(hybrid_total)

        print(f"  rep {rep + 1}/{REPS} done ({len(questions)} questions)")

    return samples


def main() -> None:
    questions = load_questions(QUESTIONS_PATH)
    print(f"Warming up models...")
    warm_up()

    print(f"Measuring latency over {len(questions)} questions x {REPS} reps...")
    samples = measure(questions)

    summary = {}
    for stage, values in samples.items():
        summary[stage] = {
            "n": len(values),
            "p50": percentile(values, 0.50),
            "p95": percentile(values, 0.95),
            "median": statistics.median(values),
            "mean": statistics.mean(values),
        }

    hardware = json.loads(HARDWARE_PATH.read_text(encoding="utf-8")) if HARDWARE_PATH.exists() else {}

    output = {
        "environment": "local",
        "hardware": hardware.get("local"),
        "n_questions": len(questions),
        "reps": REPS,
        "n_samples_per_stage": len(questions) * REPS,
        "summary_seconds": summary,
    }

    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print(f"\n{'Stage':<20}{'p50 (ms)':>12}{'p95 (ms)':>12}{'median (ms)':>14}")
    for stage, m in summary.items():
        print(f"{stage:<20}{m['p50']*1000:>12.1f}{m['p95']*1000:>12.1f}{m['median']*1000:>14.1f}")

    print(f"\nSaved to {RESULTS_PATH}")


if __name__ == "__main__":
    main()
