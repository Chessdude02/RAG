"""Unit tests for scripts/query_rag.py. No models, index, or API calls: Claude is
replaced with a fake client and retrieval with canned rankings."""
import sys
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest
from rank_bm25 import BM25Okapi

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import query_rag  # noqa: E402

CORPUS = [
    "dense retrieval with bi-encoders",
    "sparse retrieval with bm25 and term weighting",
    "hybrid retrieval fuses dense and sparse rankings",
    "cross encoder reranking of retrieved passages",
    "bm25 bm25 repeated term frequency",
]


class FakeClient:
    """Mimics client.messages.create, returning `text` (or only a thinking block)."""

    def __init__(self, text=None):
        self.text = text
        self.calls = []
        self.messages = self

    def create(self, **kwargs):
        self.calls.append(kwargs)
        if self.text is None:
            return SimpleNamespace(content=[SimpleNamespace(type="thinking", thinking="")])
        return SimpleNamespace(content=[SimpleNamespace(type="text", text=self.text)])


def chunk(cid):
    return {"chunk_id": cid, "text": cid, "metadata": {}}


def test_inverted_bm25_matches_bm25okapi():
    tokenized = [query_rag._tokenize(doc) for doc in CORPUS]
    reference, fast = BM25Okapi(tokenized), query_rag.InvertedBM25(tokenized)
    for query in ["bm25 retrieval", "dense sparse hybrid", "reranking", "term not in corpus"]:
        tokens = query_rag._tokenize(query)
        np.testing.assert_allclose(fast.get_scores(tokens), reference.get_scores(tokens), atol=1e-12)


@pytest.mark.parametrize("reply, expected", [
    ("factual", "factual"),
    ("Multi-hop", "multi-hop"),
    ("out-of-scope", "out-of-scope"),
    ("no idea", "factual"),  # unparseable: fail open into retrieval
    (None, "factual"),       # no text block at all
])
def test_classify_query(reply, expected):
    client = FakeClient(reply)
    assert query_rag.classify_query("q", client) == expected
    assert client.calls[0]["thinking"] == {"type": "disabled"}


def test_decompose_query_strips_list_markers_and_caps():
    client = FakeClient("1. first?\n- second?\n\n3) third?\n* fourth?")
    assert query_rag.decompose_query("q", client) == ["first?", "second?", "third?"]
    assert query_rag.decompose_query("q", FakeClient(None)) == []


def test_multi_hop_retrieve_interleaves_and_dedupes(monkeypatch):
    rankings = {"sub a": [chunk("a1"), chunk("x"), chunk("a2")], "sub b": [chunk("b1"), chunk("b2")]}
    monkeypatch.setattr(query_rag, "decompose_query", lambda q, c: ["sub a", "sub b"])
    monkeypatch.setattr(query_rag, "hybrid_retrieve", lambda q, k: rankings[q])
    original = [chunk("o1"), chunk("x"), chunk("o2")]

    merged = query_rag.multi_hop_retrieve("q", None, original, k=6)
    assert [c["chunk_id"] for c in merged] == ["o1", "a1", "b1", "x", "b2", "o2"]


def test_multi_hop_retrieve_falls_back_to_original(monkeypatch):
    monkeypatch.setattr(query_rag, "decompose_query", lambda q, c: [])
    original = [chunk(f"o{i}") for i in range(10)]
    assert query_rag.multi_hop_retrieve("q", None, original, k=8) == original[:8]


@pytest.mark.parametrize("classification, expected_ids", [
    ("factual", ["o0", "o1", "o2", "o3", "o4"]),
    ("multi-hop", ["mh"]),
    ("out-of-scope", []),
])
def test_answer_query_routes_by_classification(monkeypatch, classification, expected_ids):
    monkeypatch.setattr(query_rag, "get_anthropic_client", lambda: FakeClient("answer"))
    monkeypatch.setattr(query_rag, "classify_query", lambda q, c: classification)
    monkeypatch.setattr(query_rag, "hybrid_retrieve", lambda q, k: [chunk(f"o{i}") for i in range(k)])
    monkeypatch.setattr(query_rag, "multi_hop_retrieve", lambda q, c, original: [chunk("mh")])
    monkeypatch.setattr(query_rag, "generate_answer", lambda q, chunks, c: "answer")

    result = query_rag.answer_query("q")
    assert result["classification"] == classification
    assert [c["chunk_id"] for c in result["chunks"]] == expected_ids
