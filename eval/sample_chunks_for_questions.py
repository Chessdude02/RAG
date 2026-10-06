"""Phase 1 helper: deterministically sample candidate chunks to draft eval questions from.

Samples more than needed (POOL_SIZE) with a fixed seed so that skipping unusable
chunks (too short, pure headings/references, boilerplate) during manual question
drafting doesn't break reproducibility -- the sample order itself is fixed.
"""
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHUNKS_PATH = ROOT / "data" / "chunks" / "chunks.json"
OUTPUT_PATH = Path(__file__).resolve().parent / "candidate_chunks.jsonl"

SEED = 42
POOL_SIZE = 90


def main() -> None:
    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    rng = random.Random(SEED)
    sample = rng.sample(chunks, POOL_SIZE)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        for c in sample:
            f.write(json.dumps({
                "chunk_id": c["chunk_id"],
                "source_paper": c["metadata"]["source_paper"],
                "chunk_index": c["metadata"]["chunk_index"],
                "section": c["metadata"].get("section", ""),
                "text": c["text"],
            }) + "\n")

    print(f"Sampled {len(sample)} candidate chunks (seed={SEED}) -> {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
