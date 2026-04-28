from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.schemas import FAQListResponse
from app.db.database import get_db
from app.models.faq import FAQ

router = APIRouter()


@router.get("", response_model=FAQListResponse)
def list_faqs(
    category: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    q = db.query(FAQ)
    if category:
        q = q.filter(FAQ.category == category)
    total = q.count()
    faqs = q.order_by(FAQ.id).offset((page - 1) * page_size).limit(page_size).all()
    return FAQListResponse(total=total, faqs=faqs)
