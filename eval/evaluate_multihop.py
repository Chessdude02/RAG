"""Multi-hop routing check: does decomposing a question into sub-questions
retrieve more of the chunks it needs than a single hybrid pass?

Each question in multihop_questions.jsonl needs two chunks from two different
papers. Both strategies return MULTI_HOP_TOP_K chunks, so recall is compared at
the same k. Recall is reported per chunk and per paper: the labels name one
chunk per paper (usually its abstract), but a different chunk of the right
paper often answers the question just as well. The decomposed strategy makes
one Claude call per question (the decomposition), and its sub-questions vary
from run to run; pass --no-llm to run only the single-pass baseline.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from query_rag import (  # noqa: E402
    MULTI_HOP_TOP_K,
    get_anthropic_client,
    hybrid_retrieve,
    multi_hop_retrieve,
)

QUESTIONS_PATH = Path(__file__).resolve().parent / "multihop_questions.jsonl"
RESULTS_PATH = Path(__file__).resolve().parent / "results" / "multihop_retrieval.json"


def recall(chunk_ids: list[str], relevant: set[str]) -> float:
    return len(relevant & set(chunk_ids)) / len(relevant)


def paper_recall(chunk_ids: list[str], relevant: set[str]) -> float:
    """Chunk ids are `<arxiv_id>_<index>`; count a paper as found if any of its chunks is."""
    papers = {cid.rsplit("_", 1)[0] for cid in relevant}
    return len(papers & {cid.rsplit("_", 1)[0] for cid in chunk_ids}) / len(papers)


def main() -> None:
    use_llm = "--no-llm" not in sys.argv
    with open(QUESTIONS_PATH, "r", encoding="utf-8") as f:
        questions = [json.loads(line) for line in f if line.strip()]

    client = get_anthropic_client() if use_llm else None
    rows = []
    for q in questions:
        relevant = set(q["relevant_chunk_ids"])
        single = hybrid_retrieve(q["question"], k=MULTI_HOP_TOP_K)
        single_ids = [c["chunk_id"] for c in single]
        row = {
            "id": q["id"],
            "single_pass_recall": recall(single_ids, relevant),
            "single_pass_paper_recall": paper_recall(single_ids, relevant),
        }
        if use_llm:
            decomposed_ids = [c["chunk_id"] for c in multi_hop_retrieve(q["question"], client, single)]
            row["decomposed_recall"] = recall(decomposed_ids, relevant)
            row["decomposed_paper_recall"] = paper_recall(decomposed_ids, relevant)
        rows.append(row)
        print(row)

    summary = {"n": len(rows), "k": MULTI_HOP_TOP_K}
    for key in ("single_pass_recall", "single_pass_paper_recall", "decomposed_recall", "decomposed_paper_recall"):
        if rows and key in rows[0]:
            summary[f"mean_{key}"] = sum(r[key] for r in rows) / len(rows)
            summary[f"both_found_{key}"] = sum(r[key] == 1.0 for r in rows)
    print(json.dumps(summary, indent=2))

    if use_llm:
        RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
        RESULTS_PATH.write_text(json.dumps({"summary": summary, "per_question": rows}, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
