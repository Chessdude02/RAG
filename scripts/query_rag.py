"""Retrieve relevant chunks from Chroma and generate a cited answer with the Anthropic API."""
import json
import re
import sys
from pathlib import Path

import anthropic
import chromadb
from dotenv import load_dotenv
from rank_bm25 import BM25Okapi
from sentence_transformers import CrossEncoder, SentenceTransformer

load_dotenv()

CHROMA_DIR = Path(__file__).resolve().parent.parent / "data" / "chroma_db"
CHUNKS_PATH = Path(__file__).resolve().parent.parent / "data" / "chunks" / "chunks.json"
COLLECTION_NAME = "rag_papers"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CROSS_ENCODER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"
ANTHROPIC_MODEL = "claude-sonnet-5"
MAX_TOKENS = 1024
TOP_K = 5
CANDIDATE_POOL = 20  # per-retriever candidates fed into RRF, ahead of the final top-k
RRF_K = 60

SYSTEM_PROMPT = """You are a research assistant answering questions using only the \
provided excerpts from arXiv papers on retrieval-augmented generation.

Rules:
- Answer using only the information in the provided context. If the context does \
not contain enough information to answer, say so.
- Every claim you make must be followed by a citation to the chunk(s) it came from, \
formatted exactly as: [source: paper_title, chunk_N]
- Use the paper_title and chunk_N values exactly as given in the context labels.
- If multiple chunks support a claim, cite them together, \
e.g. [source: paper_title, chunk_2][source: paper_title, chunk_5]."""

_embedding_model = None
_collection = None
_anthropic_client = None
_bm25_index = None
_bm25_chunks = None
_cross_encoder = None


def get_embedding_model() -> SentenceTransformer:
    global _embedding_model
    if _embedding_model is None:
        _embedding_model = SentenceTransformer(EMBEDDING_MODEL)
    return _embedding_model


def get_cross_encoder() -> CrossEncoder:
    global _cross_encoder
    if _cross_encoder is None:
        _cross_encoder = CrossEncoder(CROSS_ENCODER_MODEL)
    return _cross_encoder


def get_collection():
    global _collection
    if _collection is None:
        client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        _collection = client.get_collection(COLLECTION_NAME)
    return _collection


def get_anthropic_client() -> anthropic.Anthropic:
    global _anthropic_client
    if _anthropic_client is None:
        _anthropic_client = anthropic.Anthropic()
    return _anthropic_client


def retrieve_relevant_chunks(query: str, n_results: int = TOP_K) -> list[dict]:
    """Embed the query and fetch the top-n most relevant chunks from Chroma."""
    model = get_embedding_model()
    query_embedding = model.encode([query]).tolist()

    collection = get_collection()
    results = collection.query(query_embeddings=query_embedding, n_results=n_results)

    chunks = []
    for chunk_id, doc, meta, distance in zip(
        results["ids"][0], results["documents"][0], results["metadatas"][0], results["distances"][0]
    ):
        chunks.append({"chunk_id": chunk_id, "text": doc, "metadata": meta, "distance": distance})
    return chunks


def _tokenize(text: str) -> list[str]:
    return re.findall(r"\w+", text.lower())


def get_bm25_index() -> tuple[BM25Okapi, list[dict]]:
    """Build (once) a BM25Okapi index over the full chunk corpus."""
    global _bm25_index, _bm25_chunks
    if _bm25_index is None:
        if not CHUNKS_PATH.exists():
            raise FileNotFoundError(f"{CHUNKS_PATH} not found. Run chunk_papers.py first.")
        with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
            _bm25_chunks = json.load(f)
        tokenized_corpus = [_tokenize(chunk["text"]) for chunk in _bm25_chunks]
        _bm25_index = BM25Okapi(tokenized_corpus)
    return _bm25_index, _bm25_chunks


def bm25_retrieve(query: str, n_results: int = CANDIDATE_POOL) -> list[dict]:
    """Rank the full corpus with BM25 and return the top-n chunks."""
    bm25, chunks = get_bm25_index()
    scores = bm25.get_scores(_tokenize(query))
    ranked_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:n_results]

    return [
        {
            "chunk_id": chunks[i]["chunk_id"],
            "text": chunks[i]["text"],
            "metadata": chunks[i]["metadata"],
            "score": float(scores[i]),
        }
        for i in ranked_indices
    ]


def rerank(query: str, chunks: list[dict], k: int = TOP_K) -> list[dict]:
    """Re-score candidate chunks with a cross-encoder and return the top-k by that score."""
    if not chunks:
        return []

    model = get_cross_encoder()
    pairs = [(query, chunk["text"]) for chunk in chunks]
    scores = model.predict(pairs)

    for chunk, score in zip(chunks, scores):
        chunk["rerank_score"] = float(score)

    ranked = sorted(chunks, key=lambda c: c["rerank_score"], reverse=True)
    return ranked[:k]


def hybrid_retrieve(query: str, k: int = TOP_K, candidate_pool: int = CANDIDATE_POOL) -> list[dict]:
    """Fuse dense (Chroma) and sparse (BM25) rankings via reciprocal rank fusion (RRF),
    then re-sort the fused pool with a cross-encoder before truncating to the final top-k.

    Each retriever contributes 1/(RRF_K + rank) per chunk it surfaces, using its
    own 1-indexed rank; a chunk found by both retrievers sums both contributions.
    """
    dense_chunks = retrieve_relevant_chunks(query, n_results=candidate_pool)
    sparse_chunks = bm25_retrieve(query, n_results=candidate_pool)

    rrf_scores: dict[str, float] = {}
    chunk_lookup: dict[str, dict] = {}

    for rank, chunk in enumerate(dense_chunks, start=1):
        chunk_id = chunk["chunk_id"]
        rrf_scores[chunk_id] = rrf_scores.get(chunk_id, 0.0) + 1.0 / (RRF_K + rank)
        chunk_lookup[chunk_id] = chunk

    for rank, chunk in enumerate(sparse_chunks, start=1):
        chunk_id = chunk["chunk_id"]
        rrf_scores[chunk_id] = rrf_scores.get(chunk_id, 0.0) + 1.0 / (RRF_K + rank)
        chunk_lookup.setdefault(chunk_id, chunk)

    # Keep a wider pool (candidate_pool) from the fusion step for the cross-encoder to re-sort.
    pooled_ids = sorted(rrf_scores, key=lambda cid: rrf_scores[cid], reverse=True)[:candidate_pool]
    pooled_chunks = [{**chunk_lookup[chunk_id], "rrf_score": rrf_scores[chunk_id]} for chunk_id in pooled_ids]

    return rerank(query, pooled_chunks, k=k)


def extract_text(response: anthropic.types.Message) -> str:
    """Pull the text out of a Claude response, skipping any leading ThinkingBlock."""
    for block in response.content:
        if block.type == "text":
            return block.text
    raise ValueError("No text block found in response.content")


def build_context(chunks: list[dict]) -> str:
    blocks = []
    for chunk in chunks:
        meta = chunk["metadata"]
        label = f"[{meta['source_paper']}, chunk_{meta['chunk_index']}]"
        blocks.append(f"{label}\n{chunk['text']}")
    return "\n\n---\n\n".join(blocks)


def generate_answer(query: str, chunks: list[dict], client: anthropic.Anthropic) -> str:
    context = build_context(chunks)
    user_message = (
        f"Context excerpts:\n\n{context}\n\n---\n\nQuestion: {query}"
    )

    response = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=MAX_TOKENS,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )
    return extract_text(response)


def answer_query(query: str, n_results: int = TOP_K) -> dict:
    """Full retrieve-then-generate pipeline. Returns the answer and retrieved chunks."""
    chunks = hybrid_retrieve(query, k=n_results)
    answer = generate_answer(query, chunks, get_anthropic_client())
    return {"query": query, "answer": answer, "chunks": chunks}


if __name__ == "__main__":
    query = " ".join(sys.argv[1:]) or "How does retrieval augmented generation reduce hallucination?"

    print(f"Query: {query}\n")
    result = answer_query(query)

    print("Retrieved chunks:")
    for chunk in result["chunks"]:
        meta = chunk["metadata"]
        scores = ", ".join(
            f"{key}={chunk[key]:.4f}" for key in ("rrf_score", "rerank_score") if key in chunk
        )
        print(f"  - {meta['source_paper']} (chunk_{meta['chunk_index']}, {scores})")

    print("\nAnswer:\n")
    print(result["answer"])
