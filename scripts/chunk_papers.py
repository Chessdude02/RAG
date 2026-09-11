"""Extract text from downloaded PDFs, split it by detected section, then
chunk each section into overlapping token windows.

Section detection looks for standalone heading lines (Abstract, Introduction,
Related Work, Methods, Results, Discussion, Conclusion, References), allowing
common numbering prefixes ("1.", "I.") and case-insensitive matching. Splitting
by section first keeps unrelated topics out of the same chunk; long sections
are then windowed with tiktoken so no chunk exceeds ~500 tokens. The
References section is dropped entirely since it's mostly citations with low
retrieval value.
"""
import json
import re
from pathlib import Path

import tiktoken
from pypdf import PdfReader

PAPERS_DIR = Path(__file__).resolve().parent.parent / "data" / "papers"
CHUNKS_DIR = Path(__file__).resolve().parent.parent / "data" / "chunks"
METADATA_PATH = PAPERS_DIR / "papers_metadata.json"
OUTPUT_PATH = CHUNKS_DIR / "chunks.json"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
ENCODING_NAME = "cl100k_base"

FRONT_MATTER = "Front Matter"
EXCLUDED_SECTIONS = {"References"}

# Canonical section name -> regex alternatives that identify its heading line.
SECTION_ALIASES = [
    ("Abstract", ["abstract"]),
    ("Introduction", ["introduction"]),
    ("Related Work", ["related works?", "background"]),
    ("Methods", ["methods?", "methodology", "approach"]),
    ("Results", ["results", "experiments?", "evaluation"]),
    ("Discussion", ["discussion"]),
    ("Conclusion", ["conclusions?", "concluding remarks"]),
    ("References", ["references", "bibliography"]),
]

# Optional leading numbering, e.g. "1.", "2)", "I.", before the heading word.
_NUM_PREFIX = r"^\s*(?:(?:[0-9]{1,2}|[IVXLCDM]{1,4})[.\):]?\s+)?"

_HEADING_PATTERNS = [
    (canonical, re.compile(_NUM_PREFIX + rf"(?:{'|'.join(aliases)})\s*[:.]?\s*$", re.IGNORECASE))
    for canonical, aliases in SECTION_ALIASES
]

# PDF text extraction sometimes collapses "Abstract" (or another heading)
# straight into the following sentence on one line -- common in IEEE-style
# two-column layouts, e.g. "Abstract—Retrieval-Augmented Generation ...".
# Match that and split the heading from the body text that follows it.
_INLINE_HEADING_PATTERNS = [
    (canonical, re.compile(_NUM_PREFIX + rf"(?:{'|'.join(aliases)})\s*[—–:]\s*(?P<rest>\S.*)$", re.IGNORECASE))
    for canonical, aliases in SECTION_ALIASES
]


def detect_heading(line: str) -> str | None:
    stripped = line.strip()
    if not stripped or len(stripped) > 40:
        return None
    for canonical, pattern in _HEADING_PATTERNS:
        if pattern.match(stripped):
            return canonical
    return None


def match_inline_heading(line: str) -> tuple[str, str] | None:
    stripped = line.strip()
    if not stripped:
        return None
    for canonical, pattern in _INLINE_HEADING_PATTERNS:
        m = pattern.match(stripped)
        if m:
            return canonical, m.group("rest").strip()
    return None


def split_into_sections(text: str) -> list[tuple[str, str]]:
    """Split text into (section_name, body) pairs in reading order."""
    sections = []
    current_name = FRONT_MATTER
    current_lines: list[str] = []

    for line in text.split("\n"):
        heading = detect_heading(line)
        if heading:
            if current_lines:
                sections.append((current_name, "\n".join(current_lines).strip()))
            current_name = heading
            current_lines = []
            continue

        inline = match_inline_heading(line)
        if inline:
            heading, rest = inline
            if current_lines:
                sections.append((current_name, "\n".join(current_lines).strip()))
            current_name = heading
            current_lines = [rest] if rest else []
            continue

        current_lines.append(line)

    if current_lines:
        sections.append((current_name, "\n".join(current_lines).strip()))

    return [(name, body) for name, body in sections if body]


def extract_text(pdf_path: Path) -> str:
    reader = PdfReader(str(pdf_path))
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(pages)


def chunk_tokens(encoding, text: str, chunk_size: int, overlap: int) -> list[str]:
    tokens = encoding.encode(text, disallowed_special=())
    if not tokens:
        return []

    stride = chunk_size - overlap
    chunks = []
    for start in range(0, len(tokens), stride):
        window = tokens[start : start + chunk_size]
        if not window:
            break
        chunks.append(encoding.decode(window))
        if start + chunk_size >= len(tokens):
            break
    return chunks


def build_chunks() -> list[dict]:
    if not METADATA_PATH.exists():
        raise FileNotFoundError(
            f"{METADATA_PATH} not found. Run download_papers.py first."
        )

    with open(METADATA_PATH, "r", encoding="utf-8") as f:
        papers_metadata = json.load(f)

    encoding = tiktoken.get_encoding(ENCODING_NAME)
    CHUNKS_DIR.mkdir(parents=True, exist_ok=True)

    all_chunks = []
    failed_papers = []
    for i, paper in enumerate(papers_metadata):
        pdf_path = PAPERS_DIR / paper["filename"]
        if not pdf_path.exists():
            print(f"Skipping missing PDF: {pdf_path}")
            continue

        print(f"Extracting + chunking: {paper['title']}")
        try:
            text = extract_text(pdf_path)
            sections = split_into_sections(text)

            paper_chunks: list[tuple[str, str]] = []
            for section_name, section_text in sections:
                if section_name in EXCLUDED_SECTIONS:
                    continue
                for chunk_text in chunk_tokens(encoding, section_text, CHUNK_SIZE, CHUNK_OVERLAP):
                    paper_chunks.append((section_name, chunk_text))

            for idx, (section_name, chunk_text) in enumerate(paper_chunks):
                all_chunks.append(
                    {
                        "chunk_id": f"{paper['arxiv_id']}_{idx}",
                        "text": chunk_text,
                        "metadata": {
                            "source_paper": paper["title"],
                            "arxiv_id": paper["arxiv_id"],
                            "source_file": paper["filename"],
                            "url": paper["url"],
                            "section": section_name,
                            "chunk_index": idx,
                            "total_chunks": len(paper_chunks),
                            "num_tokens": len(encoding.encode(chunk_text, disallowed_special=())),
                        },
                    }
                )
        except Exception as exc:
            # Some arXiv PDFs have malformed fonts/encodings that trip up
            # pypdf's text extraction; skip them rather than losing the
            # whole batch's progress.
            print(f"  Skipped (extraction failed: {exc})")
            failed_papers.append(paper["arxiv_id"])
            continue

        if (i + 1) % 50 == 0:
            with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
                json.dump(all_chunks, f, indent=2, ensure_ascii=False)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)

    print(f"\nCreated {len(all_chunks)} chunks from {len(papers_metadata) - len(failed_papers)} papers")
    if failed_papers:
        print(f"Skipped {len(failed_papers)} papers due to extraction errors: {failed_papers}")
    print(f"Chunks saved to {OUTPUT_PATH}")
    return all_chunks


if __name__ == "__main__":
    build_chunks()
