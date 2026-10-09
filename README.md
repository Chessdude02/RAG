# RAG Pipeline

[![Eval regression gate](https://github.com/Chessdude02/RAG/actions/workflows/eval-gate.yml/badge.svg)](https://github.com/Chessdude02/RAG/actions/workflows/eval-gate.yml)

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
                          |              (hybrid retrieval of the original query
                          |               runs concurrently with this call)
                          v
              factual: top-5 of the original query
              multi-hop: decompose into <=3 sub-questions, retrieve each,
                         interleave rankings -> top-8
                          |
              each retrieval pass is hybrid:
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
  only one signal. BM25 is scored over an inverted index (`InvertedBM25`) that
  reproduces `rank_bm25`'s BM25Okapi scores exactly but only touches documents
  containing each query term: ~3 ms per query instead of ~220 ms.
- **Reranking**: the fused candidate pool is re-scored with a cross-encoder
  (`cross-encoder/ms-marco-MiniLM-L-6-v2`) and truncated to the final top-k, since RRF
  scores are a cheap fusion heuristic, not a relevance model.
- **Generation**: the top-k chunks are passed to Claude with a system prompt that
  requires every claim to carry a citation to the specific chunk it came from
  (`[source: paper_title, chunk_N]`), so answers are traceable back to source text
  rather than presented as unattributed prose.
- **Query classifier** (`scripts/query_rag.py:classify_query`): a lightweight Claude
  call classifies each incoming query as `factual`, `multi-hop`, or `out-of-scope`
  and the category picks the retrieval strategy:
  - `out-of-scope` short-circuits to a "not in this corpus" response with no
    generation call.
  - `factual` uses one hybrid retrieval pass and passes the top 5 chunks.
  - `multi-hop` asks Claude to split the question into up to 3 single-passage
    sub-questions (`decompose_query`), runs hybrid retrieval for each, and
    interleaves the per-question rankings (original query first) into the top 8
    chunks. Interleaving, rather than reranking everything against the original
    question, keeps chunks that answer only one part of it.

  The hybrid pass on the original query starts in a background thread while the
  classifier call is in flight, so classification no longer adds its latency in
  front of retrieval.

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

Headline numbers (October 2026). Each row names the script that reproduces it.

| What | Result | Measured by |
|---|---|---|
| Retrieval Recall@5 | **0.88** (dense-only: 0.52) | `eval/evaluate_baseline.py`, 60 labeled questions |
| Retrieval Precision@5 | **0.64** (dense-only: 0.30) | `scripts/evaluate_retrieval.py`, 20 labeled questions |
| Multi-hop: both source papers retrieved | **9–10 of 10** (single pass: 8/10) | `eval/evaluate_multihop.py` |
| Faithfulness (every claim supported by context) | **90%** (18/20) | Claude judge, `scripts/evaluate_retrieval.py` |
| Answer quality, Claude judge composite | **0.97–0.98** | CI eval gate, 20 labeled questions |
| Adversarial red-team pass rate | **96–100%** of 24 prompts | CI eval gate (injection, hallucination bait, over-refusal) |
| End-to-end latency, factual queries | **p50 4.3 s**, p95 12.8 s | `eval/measure_end_to_end.py`, laptop CPU |
| End-to-end latency, multi-hop queries | p50 18.5 s, p95 26.1 s | same |
| API cost per query | **$0.013** factual, $0.028 multi-hop | same, at list price |
| BM25 scoring time | **~3 ms** (was ~220 ms) | inverted index, identical scores |

On the 60-question set, BM25 alone also reaches Recall@5 0.88 (MRR@10 0.75 vs.
0.74 for hybrid + rerank). Those questions were each written from a single chunk,
which favors exact keyword overlap, so the set shows hybrid retrieval beats dense
retrieval by a wide margin but does not separate it from BM25.

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
  Section labels are metadata only (not used in retrieval or in the generation
  context), and headings with paper-specific titles (e.g. "3 Proposed Framework")
  are not recognized, so their text inherits the previous recognized section's
  label — which is why Introduction and Related Work are over-represented. Fixing
  the split would renumber chunk ids and invalidate every labeled eval set.
- **Multi-hop routing is evaluated on a small set.** `eval/multihop_questions.jsonl`
  has 10 questions that each need two different papers;
  `eval/evaluate_multihop.py` compares one hybrid pass with decomposition, both at
  k=8. Decomposition reached both papers for 9–10 of 10 questions across runs
  (single pass: 8/10) and raised labeled-chunk recall from 0.55 to 0.65–0.70.
  Ten questions is too few to separate prompt variants, and the sub-questions
  vary between runs. Multi-hop queries also pay an extra Claude call plus one
  cross-encoder pass per sub-question.
- **Latency is dominated by the cross-encoder and by answer length.** The
  cross-encoder takes ~1.9 s of the ~2.1 s retrieval time on a laptop CPU, and
  multi-hop queries run one pass per sub-question and produce answers 2–3x
  longer, which is why they sit at ~18 s p50 against ~4 s for factual queries. Shrinking its
  candidate pool from 20 to 10 halves that but drops Recall@5 on the eval-harness
  set from 1.00 to 0.84, so the pool stays at 20.

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

### Run the unit tests

```bash
pip install -r requirements-dev.txt
python -m pytest tests -q   # offline: no models, index, or API calls
```

### CI eval regression gate

Every push to `main` runs `.github/workflows/eval-gate.yml`, which checks out the
separate (private) `eval-harness` repo and runs its 20 labeled questions plus 24
cached red-team prompts (hallucination bait, prompt injection, over-refusal) through
`answer_query`. Each answer is scored with ROUGE-L, BLEU, embedding similarity, and
a Claude judge. The gate fails if:

- fewer than 80% of cases run without crashing, or
- any tracked metric drops more than 0.05 below the last passing run.

The baseline (run 37688638060, 2026-10-07): 44/44 cases ran, ROUGE-L 0.18, semantic
similarity 0.73, judge composite 0.98, red-team pass rate 0.96.

`data/chroma_db/` and `data/chunks/` are gitignored (~420 MB), so the workflow
downloads them from the `corpus-v1` GitHub release. **If you rebuild the corpus,
re-upload the asset**, or CI keeps testing against the old index:

```bash
tar -czf rag-corpus.tar.gz data/chroma_db data/chunks/chunks.json
gh release upload corpus-v1 rag-corpus.tar.gz --clobber
```

Required repo secrets: `ANTHROPIC_API_KEY`, and `EVAL_HARNESS_TOKEN` (a
fine-grained PAT with read access to the eval-harness repo).

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
