"""Phase 0: count papers and chunks actually present in the Chroma store.

Ground truth is the Chroma collection itself (not chunks.json, which could be
stale relative to what was actually embedded). Also cross-checks against
chunks.json and the papers directory and records any mismatch.
"""
import json
from collections import Counter
from pathlib import Path

import chromadb

ROOT = Path(__file__).resolve().parent.parent
CHROMA_DIR = ROOT / "data" / "chroma_db"
CHUNKS_PATH = ROOT / "data" / "chunks" / "chunks.json"
PAPERS_DIR = ROOT / "data" / "papers"
COLLECTION_NAME = "rag_papers"
OUTPUT_PATH = Path(__file__).resolve().parent / "results" / "corpus_stats.json"


def main() -> None:
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    collection = client.get_collection(COLLECTION_NAME)

    chroma_count = collection.count()
    all_rows = collection.get(include=["metadatas"])
    paper_ids_in_chroma = Counter(
        meta["source_paper"] for meta in all_rows["metadatas"] if meta and "source_paper" in meta
    )

    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        chunks_json = json.load(f)
    chunks_json_count = len(chunks_json)
    paper_ids_in_json = Counter(c["metadata"]["source_paper"] for c in chunks_json)

    pdf_files = [p.name for p in PAPERS_DIR.glob("*.pdf")]

    stats = {
        "chroma_collection": COLLECTION_NAME,
        "chroma_chunk_count": chroma_count,
        "chroma_unique_papers": len(paper_ids_in_chroma),
        "chunks_json_chunk_count": chunks_json_count,
        "chunks_json_unique_papers": len(paper_ids_in_json),
        "pdf_files_in_papers_dir": len(pdf_files),
        "chroma_matches_chunks_json": chroma_count == chunks_json_count
        and dict(paper_ids_in_chroma) == dict(paper_ids_in_json),
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)

    print(json.dumps(stats, indent=2))
    print(f"\nSaved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
