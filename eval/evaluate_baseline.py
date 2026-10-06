"""Phase 2: baseline retrieval quality — Recall@5, Recall@10, MRR@10 for four
retrieval configurations: dense-only, BM25-only, hybrid RRF (no rerank), and
hybrid RRF + cross-encoder rerank. No LLM calls are made anywhere in this script.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from query_rag import (  # noqa: E402
    CANDIDATE_POOL,
    RRF_K,
    bm25_retrieve,
    rerank,
    retrieve_relevant_chunks,
)

QUESTIONS_PATH = Path(__file__).resolve().parent / "questions.jsonl"
RESULTS_PATH = Path(__file__).resolve().parent / "results" / "baseline_retrieval.json"

K_MAX = 10  # retrieve/evaluate up to Recall@10


def load_questions(path: Path) -> list[dict]:
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def _rrf_fuse(dense_chunks: list[dict], sparse_chunks: list[dict]) -> tuple[dict, dict]:
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
    return rrf_scores, chunk_lookup


def dense_only(query: str, k: int = K_MAX) -> list[str]:
    return [c["chunk_id"] for c in retrieve_relevant_chunks(query, n_results=k)]


def bm25_only(query: str, k: int = K_MAX) -> list[str]:
    return [c["chunk_id"] for c in bm25_retrieve(query, n_results=k)]


def hybrid_rrf_only(query: str, k: int = K_MAX, candidate_pool: int = CANDIDATE_POOL) -> list[str]:
    """RRF fusion of dense + BM25 rankings, WITHOUT the cross-encoder rerank step."""
    dense_chunks = retrieve_relevant_chunks(query, n_results=candidate_pool)
    sparse_chunks = bm25_retrieve(query, n_results=candidate_pool)
    rrf_scores, _ = _rrf_fuse(dense_chunks, sparse_chunks)
    return sorted(rrf_scores, key=lambda cid: rrf_scores[cid], reverse=True)[:k]


def hybrid_rrf_rerank(query: str, k: int = K_MAX, candidate_pool: int = CANDIDATE_POOL) -> list[str]:
    """RRF fusion followed by cross-encoder rerank of the fused pool."""
    dense_chunks = retrieve_relevant_chunks(query, n_results=candidate_pool)
    sparse_chunks = bm25_retrieve(query, n_results=candidate_pool)
    rrf_scores, chunk_lookup = _rrf_fuse(dense_chunks, sparse_chunks)
    pooled_ids = sorted(rrf_scores, key=lambda cid: rrf_scores[cid], reverse=True)[:candidate_pool]
    pooled_chunks = [chunk_lookup[cid] for cid in pooled_ids]
    reranked = rerank(query, pooled_chunks, k=k)
    return [c["chunk_id"] for c in reranked]


CONFIGS = {
    "dense_only": dense_only,
    "bm25_only": bm25_only,
    "hybrid_rrf": hybrid_rrf_only,
    "hybrid_rrf_rerank": hybrid_rrf_rerank,
}


def recall_at_k(retrieved: list[str], relevant: set[str], k: int) -> float:
    if not relevant:
        return 0.0
    return len(set(retrieved[:k]) & relevant) / len(relevant)


def mrr_at_k(retrieved: list[str], relevant: set[str], k: int) -> float:
    for rank, cid in enumerate(retrieved[:k], start=1):
        if cid in relevant:
            return 1.0 / rank
    return 0.0


def evaluate(questions: list[dict]) -> dict:
    per_config = {name: {"recall@5": [], "recall@10": [], "mrr@10": []} for name in CONFIGS}
    per_question_results = []

    for q in questions:
        relevant = set(q["relevant_chunk_ids"])
        row = {"id": q["id"], "question": q["question"]}
        for name, fn in CONFIGS.items():
            retrieved = fn(q["question"], K_MAX)
            r5 = recall_at_k(retrieved, relevant, 5)
            r10 = recall_at_k(retrieved, relevant, 10)
            mrr10 = mrr_at_k(retrieved, relevant, 10)
            per_config[name]["recall@5"].append(r5)
            per_config[name]["recall@10"].append(r10)
            per_config[name]["mrr@10"].append(mrr10)
            row[name] = {"retrieved_top10": retrieved, "recall@5": r5, "recall@10": r10, "mrr@10": mrr10}
        per_question_results.append(row)

    n = len(questions)
    summary = {
        name: {
            "n": n,
            "recall@5": sum(vals["recall@5"]) / n if n else 0.0,
            "recall@10": sum(vals["recall@10"]) / n if n else 0.0,
            "mrr@10": sum(vals["mrr@10"]) / n if n else 0.0,
        }
        for name, vals in per_config.items()
    }
    return {"summary": summary, "per_question": per_question_results}


def print_summary(title: str, n: int, summary: dict) -> None:
    print(f"\n=== {title} (n={n}) ===")
    print(f"{'Config':<20}{'Recall@5':>10}{'Recall@10':>11}{'MRR@10':>9}")
    for name, m in summary.items():
        print(f"{name:<20}{m['recall@5']:>10.4f}{m['recall@10']:>11.4f}{m['mrr@10']:>9.4f}")


def main() -> None:
    all_questions = load_questions(QUESTIONS_PATH)
    verified_questions = [q for q in all_questions if q.get("verified")]

    print(f"Loaded {len(all_questions)} questions ({len(verified_questions)} verified)")

    full_report = evaluate(all_questions)
    verified_report = evaluate(verified_questions)

    output = {
        "full_set": {"n": len(all_questions), "summary": full_report["summary"]},
        "verified_subset": {"n": len(verified_questions), "summary": verified_report["summary"]},
        "per_question_full_set": full_report["per_question"],
        "per_question_verified_subset": verified_report["per_question"],
    }

    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(RESULTS_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print_summary("Full set", len(all_questions), full_report["summary"])
    print_summary("Verified subset", len(verified_questions), verified_report["summary"])
    print(f"\nSaved full results to {RESULTS_PATH}")


if __name__ == "__main__":
    main()
