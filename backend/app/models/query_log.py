from datetime import datetime
from sqlalchemy import String, Text, DateTime, JSON, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class QueryLog(Base):
    __tablename__ = "query_logs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_question: Mapped[str] = mapped_column(Text, nullable=False)
    retrieved_faq_ids: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    retrieved_faq_titles: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    ai_response: Mapped[str] = mapped_column(Text, nullable=False)
    chat_model: Mapped[str] = mapped_column(String(100), nullable=False)
    embedding_model: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
