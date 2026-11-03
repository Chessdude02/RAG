"""Writes the five Step 5 planted-failure patches (eval/planted_failures/*.patch)
against the committed scripts/query_rag.py. Re-run after editing query_rag.py:
    python eval/planted_failures/make_patches.py
"""
import subprocess
from pathlib import Path

RAG = Path(__file__).resolve().parents[2]
SRC = RAG / "scripts" / "query_rag.py"
OUT = RAG / "eval" / "planted_failures"
OUT.mkdir(parents=True, exist_ok=True)

assert subprocess.run(["git", "diff", "--quiet", "scripts/query_rag.py"], cwd=RAG).returncode == 0
original = SRC.read_text(encoding="utf-8")

PROMPT_OLD = '''SYSTEM_PROMPT = """You are a research assistant answering questions using only the \\
provided excerpts from arXiv papers on retrieval-augmented generation.

Rules:
- Answer using only the information in the provided context. If the context does \\
not contain enough information to answer, say so.
- Every claim'''

CITE_OLD = '''- Every claim you make must be followed by a citation to the chunk(s) it came from, \\
formatted exactly as: [source: paper_title, chunk_N]
- Use the paper_title and chunk_N values exactly as given in the context labels.
- If multiple chunks support a claim, cite them together, \\
e.g. [source: paper_title, chunk_2][source: paper_title, chunk_5]."""'''

PATCHES = {
    "1_weaker_prompt": [(PROMPT_OLD, '''SYSTEM_PROMPT = """You are a knowledgeable research assistant answering questions \\
about retrieval-augmented generation. Some excerpts from arXiv papers are provided \\
for reference.

Rules:
- Every claim''')],
    "2_shuffled_contexts": [
        ('''_bm25_index = None''', '''_bm25_index = None
_previous_chunks = None  # PLANTED FAILURE: generation gets the previous query's chunks'''),
        ('''    answer = generate_answer(query, chunks, client)
    return {"query": query, "answer": answer, "classification": classification, "chunks": chunks}''',
         '''    global _previous_chunks
    generation_chunks = _previous_chunks or chunks
    _previous_chunks = chunks
    answer = generate_answer(query, generation_chunks, client)
    return {"query": query, "answer": answer, "classification": classification, "chunks": chunks}'''),
    ],
    "3_top_k_1": [
        ("TOP_K = 5\n", "TOP_K = 1\n"),
        ("MULTI_HOP_TOP_K = 8 ", "MULTI_HOP_TOP_K = 1 "),
    ],
    "4_smaller_model": [('"RAG_GENERATION_MODEL", "ministral-14b-latest")', '"RAG_GENERATION_MODEL", "ministral-3b-latest")')],
    "5_no_citation_rule": [(CITE_OLD, '''- Write a clear, well-organized answer."""''')],
}

try:
    for name, pairs in PATCHES.items():
        s = original
        for old, new in pairs:
            assert s.count(old) == 1, (name, old[:60])
            s = s.replace(old, new)
        SRC.write_text(s, encoding="utf-8")
        diff = subprocess.run(["git", "diff", "scripts/query_rag.py"], cwd=RAG,
                              capture_output=True, text=True, check=True).stdout
        (OUT / f"{name}.patch").write_text(diff, encoding="utf-8", newline="\n")
        print(name, len(diff.splitlines()), "diff lines")
finally:
    SRC.write_text(original, encoding="utf-8")
assert subprocess.run(["git", "diff", "--quiet", "scripts/query_rag.py"], cwd=RAG).returncode == 0
print("query_rag.py restored")
