# Zinda Law — Legal FAQ Assistant

A retrieval-augmented generation (RAG) web application that lets users ask questions against a knowledge base of legal FAQs and uploaded legal documents, and receive AI-generated answers grounded in that content.

---

## Summary

Zinda Law combines a curated set of 75 legal FAQ pairs with user-uploaded documents to form a searchable knowledge base. When a user submits a question, the system retrieves the most semantically relevant content and uses an LLM to generate a clear, contextual answer with source attribution.

Key capabilities:

- **Ask questions** — natural-language queries answered using retrieved FAQs and document content
- **Upload documents** — ingest PDF, DOCX, Markdown, or plain text files; scanned PDFs are handled automatically via OCR
- **Browse FAQs** — view and filter the 75 built-in legal FAQ pairs across six categories (Contracts, Employment, Intellectual Property, Liability, Privacy, Business Law)
- **Query logs** — every question and AI response is logged and viewable for review
- **Guardrails** — input safety classifier blocks prompt injection and harmful requests; all responses include a legal disclaimer

---

## Technology Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.12 · FastAPI · Uvicorn |
| **Frontend** | React 18 · TypeScript · Vite · shadcn/ui · Tailwind CSS |
| **Relational store** | SQLite (via SQLAlchemy) |
| **Vector store** | ChromaDB (SQLite-backed) |
| **PDF parsing** | pymupdf4llm · PyMuPDF · Tesseract OCR (scanned PDFs) |
| **DOCX parsing** | python-docx |
| **Embeddings** | OpenAI `text-embedding-3-small` (configurable) |
| **LLM** | OpenAI `gpt-4o-mini` (configurable) |
| **Infrastructure** | Docker · Docker Compose |
| **Cloud** | Google Cloud Run · Cloud Build · Artifact Registry |

---

## Deploy with Docker

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
- An [OpenAI API key](https://platform.openai.com/api-keys)

### 1. Clone the repository

```bash
git clone https://github.com/thebentarrow/zinda_law_rag.git
cd zinda_law_rag
```

### 2. Create the environment file

```bash
cp .env.example .env
```

Open `.env` and set your OpenAI API key:

```
OPENAI_API_KEY=sk-...
```

All other values have working defaults and can be left as-is for a local deployment.

### 3. Build and start

```bash
docker compose up --build
```

The first build takes 5–10 minutes while Python dependencies (including Tesseract OCR support) are installed. Subsequent starts are fast.

### 4. Open the app

| Service | URL |
|---|---|
| Frontend | http://localhost |
| Backend API docs | http://localhost:8000/docs |

### 5. Stop

```bash
docker compose down
```

Data (SQLite database, ChromaDB index) is persisted in a Docker volume named `app_data` and survives container restarts. To wipe all data and start fresh:

```bash
docker compose down -v
```

---

## Configuration

All configurable values are documented in `.env.example`. The most commonly changed settings:

| Variable | Default | Description |
|---|---|---|
| `OPENAI_API_KEY` | — | Required |
| `CHAT_MODEL` | `gpt-4o-mini` | LLM used for answer generation |
| `EMBEDDING_MODEL` | `text-embedding-3-small` | Embedding model |
| `RETRIEVAL_TOP_K` | `2` | Number of sources retrieved per query |

---

## Documentation

| Document | Description |
|---|---|
| [Pipeline reference](docs/pipelines.md) | How documents are parsed, chunked, embedded, and retrieved; how the query pipeline works end-to-end |
| [GCP deployment guide](docs/deploy-gce.md) | Step-by-step instructions to deploy on a GCP e2-standard-2 Compute Engine instance, including how to stop and restart the VM |

---

## Technical Challenges
- PDFs had scanned text not actual text causing our original document parser to return 0 chunks. Fixed by employing an OCR method as an alternative if the text based extraction yielded such result.
- Originally wanted to use docling but it caused building the image to take over 20min and cold starts took a very long time. Reverted to a simpler pymupdf4llm and PyMuPDF.
