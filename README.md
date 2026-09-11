# RAG Pipeline

## 1. Overview

A retrieval-augmented generation system over a corpus of roughly 700 arXiv papers on
retrieval-augmented generation, dense/sparse retrieval, and question answering. The
project goes beyond naive dense-vector search: retrieval is hybrid (dense + sparse,
fused and reranked), generation is required to cite the specific chunk each claim came
from, and the pipeline is evaluated against a labeled test set rather than assumed to
work.

## 2. Architecture

```
arXiv download (PDFs)
        |
section-aware chunking (pypdf + tiktoken)
        |
embedding + storage (sentence-transformers -> Chroma)
        |
        v
   query in -----> query classifier ---> out-of-scope? --> short-circuit response
                          |
                          v (factual / multi-hop)
              hybrid retrieval:
                dense (Chroma cosine) ---\
                                          +--> reciprocal rank fusion (RRF)
                sparse (BM25, full corpus)-/
                          |
                          v
              cross-encoder reranking (top candidate pool -> top-5)
                          |
                          v
              Claude generation, one citation per claim
                          |
                          v
                      answer + sources
```

- **Ingestion** (`scripts/download_papers.py`, `scripts/chunk_papers.py`,
  `scripts/embed_and_store.py`): downloads PDFs from arXiv across four query terms
  (to avoid one search dominating the corpus), extracts text with `pypdf`, splits
  each paper into sections by detecting heading lines (Abstract, Introduction,
  Related Work, Methods, Results, Discussion, Conclusion; References is dropped),
  then windows each section into ~500-token chunks with 50-token overlap using
  `tiktoken`. Chunks are embedded with `sentence-transformers/all-MiniLM-L6-v2` and
  stored in a persistent Chroma collection.
- **Hybrid retrieval** (`scripts/query_rag.py:hybrid_retrieve`): dense retrieval
  against Chroma and sparse BM25 retrieval against the full chunk corpus are each run
  independently to a candidate pool, then fused with reciprocal rank fusion (RRF) so
  a chunk surfaced by either method — and especially by both — outranks one found by
  only one signal.
- **Reranking**: the fused candidate pool is re-scored with a cross-encoder
  (`cross-encoder/ms-marco-MiniLM-L-6-v2`) and truncated to the final top-k, since RRF
  scores are a cheap fusion heuristic, not a relevance model.
- **Generation**: the top-k chunks are passed to Claude with a system prompt that
  requires every claim to carry a citation to the specific chunk it came from
  (`[source: paper_title, chunk_N]`), so answers are traceable back to source text
  rather than presented as unattributed prose.
- **Query classifier** (`scripts/query_rag.py:classify_query`): a lightweight Claude
  call classifies each incoming query as `factual`, `multi-hop`, or `out-of-scope`
  before retrieval runs. Only the `out-of-scope` case currently changes behavior — it
  short-circuits straight to a "not in this corpus" response instead of spending a
  retrieval + generation call on a question the corpus can't answer.

## 3. Key design decisions

- **arXiv over SEC filings.** SEC filings were the original candidate corpus but were
  dropped in favor of arXiv papers. The tradeoff: SEC filings have more structural
  complexity (tables, exhibits, inconsistent per-filer formatting) that would have
  demanded a heavier ingestion pipeline, while arXiv PDFs are more uniform and there's
  a much larger volume of them accessible through a simple, well-documented API.
- **Corpus size scoped down from 10,000+ to ~700 documents.** The initial target was
  10,000+ documents; that was cut back to ~700 for feasibility within the project's
  time and compute budget (PDF download rate limits, embedding time, and — more
  importantly — keeping the eval and manual-review loop tractable on a corpus a
  person can still reason about).
- **Local Ollama generation was explored, then dropped.** Local generation via Ollama
  was tried early on to avoid API costs during development, but was reverted in favor
  of the Claude API for production use — local models were weaker at the
  citation-following behavior the system prompt requires, and the API's reliability
  and output quality mattered more than the marginal cost for a project this size.

## 4. Evaluation results

Measured with `scripts/evaluate_retrieval.py` against a 20-question labeled test set
(`data/eval/test_questions.json`), comparing the naive dense-only baseline
(`retrieve_relevant_chunks`) against the hybrid + rerank pipeline
(`hybrid_retrieve`):

| Metric | Naive (dense-only) | Hybrid + rerank |
|---|---|---|
| Precision@5 | 0.30 | 0.64 |
| Avg. latency (retrieval + generation) | 6.97s | 10.63s |

| Metric | Value |
|---|---|
| Faithfulness rate | 90% (18/20) |

Faithfulness is judged by a separate Claude call that checks whether every claim in a
generated answer is actually supported by the retrieved context. Two failures were
found in the 20-question set:

1. **Structural misattribution**: the model attributed a claim to a paper's
   "Requirements" section when the supporting text actually came from that same
   paper's "Challenges" section — the claim itself was in the corpus, but the
   citation pointed at the wrong section of the source.
2. **Fabricated acronym expansion**: the model expanded an acronym used in the
   context with a full-form definition that did not appear anywhere in the retrieved
   chunks, i.e. it filled in a plausible-sounding expansion from its own training
   knowledge rather than the provided context.

## 5. Known limitations

- **Chunking heuristic doesn't perfectly handle all PDF formatting.** Section
  detection relies on matching heading lines by regex; even after fixing the majority
  failure mode, a long tail of roughly 38% of "Front Matter" chunks are still
  misclassified — i.e., text that belongs to a later section gets left attributed to
  the paper's front matter because its heading wasn't recognized. This is a known gap
  in `scripts/chunk_papers.py`, not a silent one.
- **The query router is a first-pass classifier, not a routing strategy.** Today
  `classify_query` only decides whether to short-circuit `out-of-scope` questions.
  `factual` and `multi-hop` queries are both routed through the exact same
  `hybrid_retrieve` + rerank pipeline — there is no differentiated retrieval strategy
  per query type yet (e.g. wider candidate pools or multi-step retrieval for
  multi-hop questions).
- **Hybrid retrieval costs roughly 1.5x the latency of naive retrieval** (10.63s vs.
  6.97s average, end to end) in exchange for the precision@5 gain above. This is a
  real, measured tradeoff, not a rounding error — the BM25 pass over the full corpus,
  RRF fusion, and cross-encoder reranking all add wall-clock time that the naive
  single dense lookup doesn't pay.

## 6. Setup and usage

### Install

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Configure

```bash
cp .env.example .env
# then edit .env and set:
# ANTHROPIC_API_KEY=sk-ant-...
```

### Build the corpus (run once, in order)

```bash
python scripts/download_papers.py   # downloads ~700 PDFs to data/papers/
python scripts/chunk_papers.py      # extracts + section-chunks to data/chunks/chunks.json
python scripts/embed_and_store.py   # embeds chunks into data/chroma_db/ (Chroma)
```

Each step is resumable/idempotent — `download_papers.py` picks up where it left off,
and `embed_and_store.py` upserts by chunk id and prunes orphaned vectors if
`chunks.json` changes.

### Run the API

```bash
uvicorn main:app --reload
```

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "How does RAG reduce hallucination?"}'
```

Or query directly from the command line without the server:

```bash
python scripts/query_rag.py "How does RAG reduce hallucination?"
```

### Run the eval harness

```bash
python scripts/evaluate_retrieval.py
# or against a different labeled test set:
python scripts/evaluate_retrieval.py path/to/other_test_questions.json
```

Prints per-question precision@5, latency, and faithfulness for both pipelines, plus
the summary table shown in section 4.

See `DEPLOYMENT.md` for deploying the API to an AWS EC2 instance.

## 7. Tech stack

- **Language / API**: Python, FastAPI, uvicorn
- **LLM**: Claude (Anthropic API), via the `anthropic` SDK
- **Embeddings**: `sentence-transformers` (`all-MiniLM-L6-v2`)
- **Vector store**: Chroma (persistent client, cosine similarity)
- **Sparse retrieval**: `rank_bm25` (BM25Okapi)
- **Reranking**: `sentence-transformers` cross-encoder (`ms-marco-MiniLM-L-6-v2`)
- **PDF extraction**: `pypdf`
- **Tokenization**: `tiktoken`
- **Corpus source**: arXiv, via the `arxiv` Python client
- **Config**: `python-dotenv`
