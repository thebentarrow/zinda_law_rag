from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.schemas import LogListResponse
from app.db.database import get_db
from app.models.query_log import QueryLog

router = APIRouter()


@router.get("", response_model=LogListResponse)
def get_logs(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    total = db.query(QueryLog).count()
    logs = (
        db.query(QueryLog)
        .order_by(QueryLog.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )
    return LogListResponse(total=total, page=page, page_size=page_size, logs=logs)
