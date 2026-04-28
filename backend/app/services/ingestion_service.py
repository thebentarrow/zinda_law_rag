from __future__ import annotations

import logging
import re

from sqlalchemy.orm import Session

from app.models.faq import FAQ
from app.models.document_chunk import DocumentChunk
from app.services.embedding_service import EmbeddingService
from app.services import vector_store
from app.services.document_parser import parse_bytes
from app.services.chunking_service import chunk_text

logger = logging.getLogger(__name__)


# ── FAQ indexing ──────────────────────────────────────────────────────────────

async def index_faqs(db: Session, faq_ids: list[int] | None = None) -> int:
    """Embed and upsert FAQs into the vector store."""
    embedding_svc = EmbeddingService()

    q = db.query(FAQ)
    if faq_ids:
        q = q.filter(FAQ.id.in_(faq_ids))
    faqs: list[FAQ] = q.all()
    if not faqs:
        return 0

    texts = [f"{faq.title}\n{faq.question}\n{faq.answer}" for faq in faqs]
    embeddings = await embedding_svc.embed_batch(texts)

    vector_store.upsert_faqs(
        ids=[f"faq_{faq.id}" for faq in faqs],
        embeddings=embeddings,
        documents=texts,
        metadatas=[
            {
                "type": "faq",
                "faq_id": faq.id,
                "title": faq.title,
                "category": faq.category,
            }
            for faq in faqs
        ],
    )
    return len(faqs)


# ── Document indexing (startup re-index of existing rows) ─────────────────────

async def index_document_chunks(
    db: Session, chunk_ids: list[int] | None = None
) -> int:
    """Embed and upsert existing DocumentChunk rows (e.g., on startup re-sync)."""
    embedding_svc = EmbeddingService()

    q = db.query(DocumentChunk)
    if chunk_ids:
        q = q.filter(DocumentChunk.id.in_(chunk_ids))
    chunks: list[DocumentChunk] = q.all()
    if not chunks:
        return 0

    texts = [c.content for c in chunks]
    embeddings = await embedding_svc.embed_batch(texts)

    vector_store.upsert_chunks(
        ids=[f"chunk_{c.id}" for c in chunks],
        embeddings=embeddings,
        documents=texts,
        metadatas=[
            {
                "type": "chunk",
                "chunk_id": c.id,
                "source_name": c.source_name,
                "doc_id": c.doc_id or _normalise_doc_id(c.source_name),
                "doc_type": c.doc_type,
                "chunk_index": c.chunk_index,
            }
            for c in chunks
        ],
    )
    return len(chunks)


# ── Document ingestion (upload path) ─────────────────────────────────────────

async def ingest_document(
    db: Session,
    content: bytes,
    filename: str,
) -> tuple[int, list[str]]:
    """
    Parse a document, split into overlapping chunks, embed, and store.

    Returns (chunks_inserted, error_messages).
    Does NOT commit — caller is responsible for db.commit().
    """
    errors: list[str] = []

    try:
        clean_text, doc_type = parse_bytes(content, filename)
    except ValueError as exc:
        return 0, [str(exc)]

    if not clean_text.strip():
        return 0, ["File produced no extractable text"]

    logger.info("Parsed '%s': %d chars, doc_type=%s", filename, len(clean_text), doc_type)

    chunks = chunk_text(clean_text)
    if not chunks:
        return 0, ["Document produced no text chunks"]

    logger.info("'%s': %d chunks", filename, len(chunks))

    doc_id = _normalise_doc_id(filename)
    embedding_svc = EmbeddingService()
    new_chunk_ids: list[int] = []
    embed_texts: list[str] = []

    for idx, chunk_content in enumerate(chunks):
        embed_text = chunk_content
        row = DocumentChunk(
            source_name=filename,
            doc_id=doc_id,
            doc_type=doc_type,
            chunk_index=idx,
            content=chunk_content,
            node_id="",
            breadcrumb="",
            section_heading="",
            section_full_text="",
        )
        db.add(row)
        db.flush()
        new_chunk_ids.append(row.id)
        embed_texts.append(embed_text)

    try:
        embeddings = await embedding_svc.embed_batch(embed_texts)
        vector_store.upsert_chunks(
            ids=[f"chunk_{cid}" for cid in new_chunk_ids],
            embeddings=embeddings,
            documents=embed_texts,
            metadatas=[
                {
                    "type": "chunk",
                    "chunk_id": cid,
                    "source_name": filename,
                    "doc_id": doc_id,
                    "doc_type": doc_type,
                    "chunk_index": idx,
                }
                for idx, cid in enumerate(new_chunk_ids)
            ],
        )
    except Exception as exc:
        errors.append(f"Embedding/indexing error: {exc}")

    return len(new_chunk_ids), errors


# ── Helpers ───────────────────────────────────────────────────────────────────

def _normalise_doc_id(source_name: str) -> str:
    return re.sub(r"[^\w]", "_", source_name.lower()).strip("_")
