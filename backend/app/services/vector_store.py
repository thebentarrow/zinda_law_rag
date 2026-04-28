from __future__ import annotations

import os
import chromadb
from chromadb.config import Settings as ChromaSettings

from app.core.config import settings


_client: chromadb.PersistentClient | None = None
_COLLECTION_NAME = "knowledge_base"


def get_chroma_client() -> chromadb.PersistentClient:
    global _client
    if _client is None:
        os.makedirs(settings.chroma_path, exist_ok=True)
        _client = chromadb.PersistentClient(
            path=settings.chroma_path,
            settings=ChromaSettings(anonymized_telemetry=False),
        )
    return _client


def get_collection() -> chromadb.Collection:
    client = get_chroma_client()
    return client.get_or_create_collection(
        name=_COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )


# ── Upsert ────────────────────────────────────────────────────────────────────

def upsert_faqs(
    ids: list[str],
    embeddings: list[list[float]],
    documents: list[str],
    metadatas: list[dict],
) -> None:
    get_collection().upsert(ids=ids, embeddings=embeddings, documents=documents, metadatas=metadatas)


def upsert_chunks(
    ids: list[str],
    embeddings: list[list[float]],
    documents: list[str],
    metadatas: list[dict],
) -> None:
    get_collection().upsert(ids=ids, embeddings=embeddings, documents=documents, metadatas=metadatas)


# ── Query ─────────────────────────────────────────────────────────────────────

def query_similar(embedding: list[float], top_k: int) -> list[dict]:
    results = get_collection().query(
        query_embeddings=[embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )
    items = []
    for i in range(len(results["ids"][0])):
        items.append(
            {
                "chroma_id": results["ids"][0][i],
                "document": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i],
            }
        )
    return items


# ── Delete ────────────────────────────────────────────────────────────────────

def delete_faq(faq_id: int) -> None:
    get_collection().delete(ids=[f"faq_{faq_id}"])


def delete_chunk(chunk_id: int) -> None:
    get_collection().delete(ids=[f"chunk_{chunk_id}"])


def delete_all() -> None:
    """Drop and recreate the collection, removing all FAQs and document chunks."""
    client = get_chroma_client()
    client.delete_collection(_COLLECTION_NAME)
    client.get_or_create_collection(
        name=_COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )


# Keep old name as alias so existing call-sites in faqs.py still compile
delete_all_faqs = delete_all
