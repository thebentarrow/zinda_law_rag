from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.schemas import QueryRequest, QueryResponse
from app.db.database import get_db
from app.services.rag_service import RAGService

router = APIRouter()


@router.post("", response_model=QueryResponse)
async def submit_query(payload: QueryRequest, db: Session = Depends(get_db)):
    try:
        rag = RAGService()
        result = await rag.answer(payload.question, db)
        return result
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
