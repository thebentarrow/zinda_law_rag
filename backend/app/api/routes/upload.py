"""
POST /api/upload

Accepts any of:
  - .csv / .json        → parsed as FAQ rows (title, question, answer, category)
  - .pdf / .docx / .md / .txt  → Proxy-Pointer RAG ingestion:
                            skeleton tree → noise filter → section-aware chunking
                            → breadcrumb prepend → embed → store with full_section_text

Query param `mode`:
  - append  (default) – add to existing knowledge base
  - replace           – delete all FAQs + chunks first, then import
"""
from __future__ import annotations

import csv
import io
import json
from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from app.api.schemas import UploadResult
from app.db.database import get_db
from app.models.document_chunk import DocumentChunk
from app.models.faq import FAQ
from app.services import vector_store
from app.services.ingestion_service import index_faqs, ingest_document

router = APIRouter()

_FAQ_EXTENSIONS = {".csv", ".json"}
_DOC_EXTENSIONS = {".pdf", ".docx", ".md", ".markdown", ".txt"}
_REQUIRED_FAQ_FIELDS = {"title", "question", "answer", "category"}


@router.post("", response_model=UploadResult)
async def upload_content(
    file: Annotated[UploadFile, File(description="FAQ file (.csv/.json) or legal document (.pdf/.md/.txt)")],
    mode: Annotated[str, Form(description="'append' or 'replace'")] = "append",
    db: Session = Depends(get_db),
):
    if mode not in ("append", "replace"):
        raise HTTPException(status_code=400, detail="mode must be 'append' or 'replace'")

    filename = (file.filename or "").lower()
    ext = _file_ext(filename)

    if ext in _FAQ_EXTENSIONS:
        return await _handle_faq_upload(await file.read(), filename, mode, db)
    if ext in _DOC_EXTENSIONS:
        return await _handle_document_upload(
            await file.read(), file.filename or filename, mode, db
        )

    raise HTTPException(
        status_code=400,
        detail=f"Unsupported file type '{ext}'. Accepted: {sorted(_FAQ_EXTENSIONS | _DOC_EXTENSIONS)}",
    )


# ── FAQ path ──────────────────────────────────────────────────────────────────

async def _handle_faq_upload(
    content: bytes, filename: str, mode: str, db: Session
) -> UploadResult:
    rows, parse_errors = _parse_faq_file(content, filename)

    if mode == "replace":
        db.query(FAQ).delete()
        db.commit()
        vector_store.delete_all()

    inserted, skipped = 0, 0
    errors: list[str] = list(parse_errors)
    new_ids: list[int] = []

    for i, row in enumerate(rows):
        missing = _REQUIRED_FAQ_FIELDS - set(row.keys())
        if missing:
            errors.append(f"Row {i + 1}: missing fields {missing}")
            skipped += 1
            continue
        if not all(str(row[f]).strip() for f in _REQUIRED_FAQ_FIELDS):
            errors.append(f"Row {i + 1}: one or more required fields are empty")
            skipped += 1
            continue
        faq = FAQ(
            title=str(row["title"]).strip(),
            question=str(row["question"]).strip(),
            answer=str(row["answer"]).strip(),
            category=str(row["category"]).strip(),
        )
        db.add(faq)
        db.flush()
        new_ids.append(faq.id)
        inserted += 1

    db.commit()

    indexed = 0
    if new_ids:
        try:
            indexed = await index_faqs(db, faq_ids=new_ids)
        except Exception as exc:
            errors.append(f"Indexing error: {exc}")

    return UploadResult(
        upload_type="faqs", inserted=inserted, skipped=skipped, indexed=indexed, errors=errors
    )


def _parse_faq_file(content: bytes, filename: str) -> tuple[list[dict], list[str]]:
    if filename.endswith(".json"):
        try:
            data = json.loads(content)
            if not isinstance(data, list):
                return [], ["JSON must be an array of objects"]
            return data, []
        except json.JSONDecodeError as exc:
            return [], [f"JSON parse error: {exc}"]
    try:
        text = content.decode("utf-8-sig")
        return list(csv.DictReader(io.StringIO(text))), []
    except Exception as exc:
        return [], [f"CSV parse error: {exc}"]


# ── Document path (PP-RAG) ────────────────────────────────────────────────────

async def _handle_document_upload(
    content: bytes, original_filename: str, mode: str, db: Session
) -> UploadResult:
    if mode == "replace":
        db.query(DocumentChunk).delete()
        db.query(FAQ).delete()
        db.commit()
        vector_store.delete_all()

    inserted, errors = await ingest_document(db, content, original_filename)
    db.commit()

    return UploadResult(
        upload_type="document",
        inserted=inserted,
        skipped=0,
        indexed=inserted,  # ingest_document_pp_rag embeds inline
        errors=errors,
    )


def _file_ext(filename: str) -> str:
    dot = filename.rfind(".")
    return filename[dot:] if dot != -1 else ""
