import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.init_db import init_db
from app.services.ingestion_service import index_faqs, index_document_chunks  # noqa: F401
from app.db.database import SessionLocal
from app.api.routes import query, logs, faqs, health, upload

logging.basicConfig(level=settings.log_level.upper())
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing database...")
    init_db(seed=True)
    logger.info("Indexing knowledge base into vector store...")
    db = SessionLocal()
    try:
        faq_count = await index_faqs(db)
        chunk_count = await index_document_chunks(db)
        logger.info("Indexed %d FAQs and %d document chunks", faq_count, chunk_count)
    finally:
        db.close()
    yield
    logger.info("Shutting down")


app = FastAPI(
    title="Zinda Law RAG API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(query.router, prefix="/api/query", tags=["query"])
app.include_router(logs.router, prefix="/api/logs", tags=["logs"])
app.include_router(faqs.router, prefix="/api/faqs", tags=["faqs"])
app.include_router(upload.router, prefix="/api/upload", tags=["upload"])
app.include_router(health.router, prefix="/api/health", tags=["health"])
