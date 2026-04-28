import os
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.database import Base, engine, SessionLocal
from app.models.faq import FAQ
from app.models.query_log import QueryLog  # noqa: F401 – ensures table is created
from app.models.document_chunk import DocumentChunk  # noqa: F401 – ensures table is created
from app.db.seed_data import SEED_FAQS


def create_tables() -> None:
    os.makedirs(os.path.dirname(engine.url.database), exist_ok=True)
    Base.metadata.create_all(bind=engine)


def migrate_document_chunks() -> None:
    """
    Add Proxy-Pointer RAG columns to document_chunks if they were created
    before this schema version.  SQLite supports ADD COLUMN idempotently
    when the column does not already exist.
    """
    new_cols = {
        "doc_id": "TEXT NOT NULL DEFAULT ''",
        "node_id": "TEXT NOT NULL DEFAULT ''",
        "breadcrumb": "TEXT NOT NULL DEFAULT ''",
        "section_heading": "TEXT NOT NULL DEFAULT ''",
        "section_full_text": "TEXT NOT NULL DEFAULT ''",
    }
    with engine.connect() as conn:
        rows = conn.execute(text("PRAGMA table_info(document_chunks)")).fetchall()
        existing = {row[1] for row in rows}
        for col, definition in new_cols.items():
            if col not in existing:
                conn.execute(
                    text(f"ALTER TABLE document_chunks ADD COLUMN {col} {definition}")
                )
        conn.commit()


def seed_faqs(db: Session, overwrite: bool = False) -> int:
    if overwrite:
        db.query(FAQ).delete()
        db.commit()

    existing_count = db.query(FAQ).count()
    if existing_count > 0 and not overwrite:
        return 0

    faqs = [FAQ(**row) for row in SEED_FAQS]
    db.add_all(faqs)
    db.commit()
    return len(faqs)


def init_db(seed: bool = True) -> None:
    create_tables()
    migrate_document_chunks()
    if seed:
        db = SessionLocal()
        try:
            seed_faqs(db)
        finally:
            db.close()
