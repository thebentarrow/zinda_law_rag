from datetime import datetime
from pydantic import BaseModel, Field


# ── FAQ ──────────────────────────────────────────────────────────────────────

class FAQBase(BaseModel):
    title: str
    question: str
    answer: str
    category: str


class FAQResponse(FAQBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class FAQListResponse(BaseModel):
    total: int
    faqs: list[FAQResponse]


# ── Query ────────────────────────────────────────────────────────────────────

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=5, max_length=2000)


class SourceItem(BaseModel):
    id: int
    type: str        # "faq" | "chunk"
    title: str
    question: str
    category: str


class QueryResponse(BaseModel):
    answer: str
    sources: list[SourceItem]
    log_id: int
    blocked: bool = False


# ── Logs ─────────────────────────────────────────────────────────────────────

class LogEntry(BaseModel):
    id: int
    user_question: str
    retrieved_faq_ids: list[int]
    retrieved_faq_titles: list[str]
    ai_response: str
    chat_model: str
    embedding_model: str
    created_at: datetime

    model_config = {"from_attributes": True}


class LogListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    logs: list[LogEntry]


# ── Upload ───────────────────────────────────────────────────────────────────

class UploadResult(BaseModel):
    upload_type: str          # "faqs" | "document"
    inserted: int             # FAQ rows OR document chunks written
    skipped: int
    indexed: int
    errors: list[str]


# ── Health ───────────────────────────────────────────────────────────────────

class HealthResponse(BaseModel):
    status: str
    chat_model: str
    embedding_model: str
    retrieval_top_k: int
    environment: str
