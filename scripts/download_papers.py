"""Download a topically diverse set of arXiv papers as PDFs.

Pulls from several related query terms instead of one, so the corpus isn't
dominated by near-duplicate top hits for a single search. Respects arXiv's
rate limits: the arxiv.Client enforces >=3s between search API requests, and
we add the same delay between PDF downloads (a separate HTTP call the client
doesn't throttle for us).
"""
import json
import re
import time
from pathlib import Path

import arxiv

QUERIES = [
    "retrieval augmented generation",
    "dense passage retrieval",
    "information retrieval neural",
    "question answering transformers",
]
TARGET_TOTAL = 700  # aim for the middle of the requested 500-800 range
MAX_TOTAL = 800
PER_QUERY_TARGET = TARGET_TOTAL // len(QUERIES)
MAX_RESULTS_PER_QUERY = 300  # buffer against cross-query duplicates
REQUEST_DELAY_SECONDS = 3.0  # arXiv API etiquette: max 1 request / 3s

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "papers"
METADATA_PATH = DATA_DIR / "papers_metadata.json"


def safe_filename(arxiv_id: str, title: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", title).strip("_").lower()[:80]
    return f"{arxiv_id}_{slug}.pdf"


def load_existing_metadata() -> list[dict]:
    if METADATA_PATH.exists():
        with open(METADATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_metadata(metadata: list[dict]) -> None:
    with open(METADATA_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)


def download_papers() -> list[dict]:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    client = arxiv.Client(
        page_size=100,
        delay_seconds=REQUEST_DELAY_SECONDS,
        num_retries=3,
    )

    # Resumable: pick up where a previous (possibly crashed) run left off,
    # instead of losing already-downloaded progress.
    metadata = load_existing_metadata()
    seen_ids = {paper["arxiv_id"] for paper in metadata}
    per_query_counts: dict[str, int] = {}
    for paper in metadata:
        query_key = paper.get("query")
        per_query_counts[query_key] = per_query_counts.get(query_key, 0) + 1
    if metadata:
        print(f"Resuming: {len(metadata)} papers already recorded.")

    for query in QUERIES:
        if len(metadata) >= MAX_TOTAL:
            break

        added_for_query = per_query_counts.get(query, 0)
        if added_for_query >= PER_QUERY_TARGET:
            print(f"\n=== Query: '{query}' === already has {added_for_query}, skipping")
            continue

        print(f"\n=== Query: '{query}' ===")
        search = arxiv.Search(
            query=query,
            max_results=MAX_RESULTS_PER_QUERY,
            sort_by=arxiv.SortCriterion.Relevance,
        )

        for result in client.results(search):
            if added_for_query >= PER_QUERY_TARGET or len(metadata) >= MAX_TOTAL:
                break

            arxiv_id = result.get_short_id()
            if arxiv_id in seen_ids:
                continue

            filename = safe_filename(arxiv_id, result.title)
            filepath = DATA_DIR / filename

            if not filepath.exists():
                print(f"Downloading ({len(metadata) + 1}): {result.title}")
                try:
                    result.download_pdf(dirpath=str(DATA_DIR), filename=filename)
                except Exception as exc:
                    # arXiv occasionally 404s on withdrawn/malformed entries;
                    # skip and keep going rather than losing hours of progress.
                    print(f"  Skipped (download failed: {exc})")
                    time.sleep(REQUEST_DELAY_SECONDS)
                    continue
                time.sleep(REQUEST_DELAY_SECONDS)
            else:
                print(f"Already downloaded: {filename}")

            seen_ids.add(arxiv_id)
            metadata.append(
                {
                    "arxiv_id": arxiv_id,
                    "title": result.title,
                    "authors": [a.name for a in result.authors],
                    "published": result.published.isoformat(),
                    "url": result.entry_id,
                    "filename": filename,
                    "query": query,
                }
            )
            added_for_query += 1
            per_query_counts[query] = added_for_query
            save_metadata(metadata)

        print(f"Query '{query}' now has {added_for_query} papers")

    print(f"\nDownloaded {len(metadata)} papers to {DATA_DIR}")
    print(f"Metadata saved to {METADATA_PATH}")
    return metadata


if __name__ == "__main__":
    download_papers()
