from __future__ import annotations

from datetime import datetime
from sqlalchemy import String, Text, Integer, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    source_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    doc_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True, default="")
    doc_type: Mapped[str] = mapped_column(String(20), nullable=False)
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    # ── Proxy-Pointer RAG fields ──────────────────────────────────────────────
    # node_id: unique identifier for the section within the document.
    #   Multiple chunks may share the same node_id (when a section is long enough
    #   to require several chunks). Deduplication during retrieval collapses them
    #   back to one representative node.
    node_id: Mapped[str] = mapped_column(String(255), nullable=False, default="")

    # breadcrumb: full ancestor path prepended to the chunk before embedding.
    #   e.g. "Contract Law Guide > Formation > Offer and Acceptance"
    #   Acts as the "proxy" — the embedding encodes both location and content.
    breadcrumb: Mapped[str] = mapped_column(Text, nullable=False, default="")

    # section_heading: the immediate heading of the section this chunk belongs to.
    section_heading: Mapped[str] = mapped_column(Text, nullable=False, default="")

    # section_full_text: the complete, unbroken section text (heading + all
    #   descendant content).  This is the "pointer" target — what gets passed
    #   to the synthesis LLM instead of the isolated chunk.
    section_full_text: Mapped[str] = mapped_column(Text, nullable=False, default="")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
