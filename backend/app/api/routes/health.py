from fastapi import APIRouter

from app.api.schemas import HealthResponse
from app.core.config import settings

router = APIRouter()


@router.get("", response_model=HealthResponse)
def health():
    return HealthResponse(
        status="ok",
        chat_model=settings.chat_model,
        embedding_model=settings.embedding_model,
        retrieval_top_k=settings.retrieval_top_k,
        environment=settings.environment,
    )
