from __future__ import annotations

import logging

from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

from app.core.config import settings
from app.models.faq import FAQ
from app.models.document_chunk import DocumentChunk
from app.models.query_log import QueryLog
from app.services.embedding_service import EmbeddingService
from app.services.llm_service import LLMService
from app.services import vector_store
from app.services.guardrails import check_input, validate_output

_BLOCKED_PLACEHOLDER = "[BLOCKED BY INPUT GUARDRAIL]"


class RAGService:
    def __init__(self) -> None:
        self._embedding_svc = EmbeddingService()
        self._llm_svc = LLMService()

    async def answer(self, question: str, db: Session) -> dict:

        # ── 1. Input guardrail ────────────────────────────────────────────────
        input_check = await check_input(question)
        if not input_check.passed:
            log = QueryLog(
                user_question=question,
                retrieved_faq_ids=[],
                retrieved_faq_titles=[],
                ai_response=_BLOCKED_PLACEHOLDER,
                chat_model=settings.chat_model,
                embedding_model=settings.embedding_model,
            )
            db.add(log)
            db.commit()
            db.refresh(log)
            return {
                "answer": input_check.rejection_message,
                "sources": [],
                "log_id": log.id,
                "blocked": True,
            }

        # ── 2. Embed query ────────────────────────────────────────────────────
        query_embedding = await self._embedding_svc.embed(question)

        # ── 3. Retrieve top-K chunks / FAQs ───────────────────────────────────
        results = vector_store.query_similar(
            embedding=query_embedding,
            top_k=settings.retrieval_top_k,
        )

        for r in results:
            meta = r["metadata"]
            logger.info(
                "Retrieved: type=%s id=%s distance=%.4f source=%s",
                meta.get("type"),
                meta.get("chunk_id") or meta.get("faq_id"),
                r["distance"],
                meta.get("source_name") or meta.get("title", "")[:60],
            )

        # ── 4. Hydrate from SQLite ────────────────────────────────────────────
        context_pieces: list[dict] = []
        sources: list[dict] = []
        faq_ids_logged: list[int] = []
        faq_titles_logged: list[str] = []

        for result in results:
            meta = result["metadata"]
            item_type = meta.get("type", "faq")

            if item_type == "chunk":
                chunk_id = int(meta["chunk_id"])
                chunk = db.query(DocumentChunk).filter(DocumentChunk.id == chunk_id).first()
                if chunk:
                    context_pieces.append(
                        {
                            "type": "chunk",
                            "source": chunk.source_name,
                            "content": chunk.content,
                        }
                    )
                    sources.append(
                        {
                            "id": chunk.id,
                            "type": "chunk",
                            "title": chunk.source_name,
                            "question": f"Chunk {chunk.chunk_index + 1}",
                            "category": chunk.doc_type.upper(),
                        }
                    )

            else:
                faq_id = int(meta["faq_id"])
                faq = db.query(FAQ).filter(FAQ.id == faq_id).first()
                if faq:
                    context_pieces.append(
                        {
                            "type": "faq",
                            "title": faq.title,
                            "question": faq.question,
                            "answer": faq.answer,
                        }
                    )
                    sources.append(
                        {
                            "id": faq.id,
                            "type": "faq",
                            "title": faq.title,
                            "question": faq.question,
                            "category": faq.category,
                        }
                    )
                    faq_ids_logged.append(faq.id)
                    faq_titles_logged.append(faq.title)

        # ── 5. Generate answer ────────────────────────────────────────────────
        ai_response = await self._llm_svc.generate(question, context_pieces)

        # ── 6. Output guardrail ───────────────────────────────────────────────
        final_response = validate_output(ai_response).response

        # ── 7. Log ────────────────────────────────────────────────────────────
        log = QueryLog(
            user_question=question,
            retrieved_faq_ids=faq_ids_logged,
            retrieved_faq_titles=faq_titles_logged,
            ai_response=final_response,
            chat_model=settings.chat_model,
            embedding_model=settings.embedding_model,
        )
        db.add(log)
        db.commit()
        db.refresh(log)

        return {
            "answer": final_response,
            "sources": sources,
            "log_id": log.id,
            "blocked": False,
        }
