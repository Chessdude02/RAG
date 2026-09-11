"""FastAPI service exposing the RAG retrieve-and-generate pipeline."""
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from scripts.query_rag import (
    answer_query,
    get_bm25_index,
    get_collection,
    get_cross_encoder,
    get_embedding_model,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Warm up the embedding/cross-encoder models, Chroma collection, and BM25 index
    # so the first request isn't slow.
    get_embedding_model()
    get_collection()
    get_bm25_index()
    get_cross_encoder()
    yield


app = FastAPI(title="RAG Pipeline API", lifespan=lifespan)


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1)


class Source(BaseModel):
    paper_title: str
    arxiv_id: str
    chunk_index: int
    url: str
    rrf_score: float | None = None
    rerank_score: float | None = None


class QueryResponse(BaseModel):
    answer: str
    sources: list[Source]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    try:
        result = answer_query(request.question)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Failed to generate answer: {exc}")

    sources = [
        Source(
            paper_title=chunk["metadata"]["source_paper"],
            arxiv_id=chunk["metadata"]["arxiv_id"],
            chunk_index=chunk["metadata"]["chunk_index"],
            url=chunk["metadata"]["url"],
            rrf_score=chunk.get("rrf_score"),
            rerank_score=chunk.get("rerank_score"),
        )
        for chunk in result["chunks"]
    ]

    return QueryResponse(answer=result["answer"], sources=sources)
