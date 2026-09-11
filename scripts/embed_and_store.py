"""Embed chunks with sentence-transformers and store them in a persistent Chroma collection."""
import json
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

CHUNKS_PATH = Path(__file__).resolve().parent.parent / "data" / "chunks" / "chunks.json"
CHROMA_DIR = Path(__file__).resolve().parent.parent / "data" / "chroma_db"
COLLECTION_NAME = "rag_papers"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
BATCH_SIZE = 64


def load_chunks() -> list[dict]:
    if not CHUNKS_PATH.exists():
        raise FileNotFoundError(f"{CHUNKS_PATH} not found. Run chunk_papers.py first.")
    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def embed_and_store() -> None:
    chunks = load_chunks()
    print(f"Loaded {len(chunks)} chunks from {CHUNKS_PATH}")

    print(f"Loading embedding model: {EMBEDDING_MODEL}")
    model = SentenceTransformer(EMBEDDING_MODEL)

    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    ids = [c["chunk_id"] for c in chunks]
    documents = [c["text"] for c in chunks]
    metadatas = [c["metadata"] for c in chunks]

    for start in range(0, len(chunks), BATCH_SIZE):
        end = start + BATCH_SIZE
        batch_ids = ids[start:end]
        batch_docs = documents[start:end]
        batch_meta = metadatas[start:end]

        embeddings = model.encode(batch_docs, show_progress_bar=False).tolist()

        collection.upsert(
            ids=batch_ids,
            embeddings=embeddings,
            documents=batch_docs,
            metadatas=batch_meta,
        )
        print(f"Stored chunks {start}-{min(end, len(chunks))}/{len(chunks)}")

    existing_ids = collection.get(include=[])["ids"]
    orphaned_ids = [i for i in existing_ids if i not in set(ids)]
    if orphaned_ids:
        collection.delete(ids=orphaned_ids)
        print(f"Deleted {len(orphaned_ids)} orphaned vectors no longer in {CHUNKS_PATH}")

    print(f"\nCollection '{COLLECTION_NAME}' now has {collection.count()} vectors")
    print(f"Persisted to {CHROMA_DIR}")


if __name__ == "__main__":
    embed_and_store()
