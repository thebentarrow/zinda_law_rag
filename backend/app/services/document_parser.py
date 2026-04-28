"""
Parse documents into clean markdown text.

PDF   → pymupdf4llm  (font-size heading detection, outputs ATX markdown natively)
DOCX  → python-docx  (maps Word heading styles → ATX markdown)
MD    → decoded directly
TXT   → decoded directly
"""
from __future__ import annotations

import io
import logging
import re

logger = logging.getLogger(__name__)


def parse_bytes(content: bytes, filename: str) -> tuple[str, str]:
    """
    Return (clean_text, doc_type).

    clean_text is markdown-formatted for PDF and DOCX so the skeleton builder
    uses its precise heading parser.

    Raises ValueError for unsupported file types.
    """
    name = filename.lower()

    if name.endswith(".pdf"):
        return _parse_pdf(content), "pdf"
    if name.endswith(".docx"):
        return _parse_docx(content), "docx"
    if name.endswith(".md") or name.endswith(".markdown"):
        return _normalise(content.decode("utf-8-sig", errors="replace")), "markdown"
    if name.endswith(".txt"):
        return _normalise(content.decode("utf-8-sig", errors="replace")), "text"

    raise ValueError(
        f"Unsupported file type for '{filename}'. "
        "Accepted: .pdf, .docx, .md, .markdown, .txt"
    )


def _parse_pdf(content: bytes) -> str:
    import os
    import tempfile
    import pymupdf
    import pymupdf4llm

    logger.info("PDF parser: received %d bytes", len(content))

    tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
    try:
        tmp.write(content)
        tmp.close()

        # Stage 1: pymupdf4llm — preserves heading structure as markdown
        md = pymupdf4llm.to_markdown(tmp.name)
        real_chars = len(re.sub(r"[-\s]", "", md))
        logger.info("PDF parser: pymupdf4llm → %d chars, %d non-separator chars", len(md), real_chars)

        if real_chars < 50:
            # Stage 2: PyMuPDF basic text extraction — works for most encoded PDFs
            logger.info("PDF parser: falling back to basic text extraction")
            doc = pymupdf.open(tmp.name)
            pages = [page.get_text("text") for page in doc]
            doc.close()
            md = "\n\n".join(p for p in pages if p.strip())
            logger.info("PDF parser: basic extraction → %d chars", len(md))

        if len(re.sub(r"\s", "", md)) < 50:
            # Stage 3: OCR — for scanned/image-only PDFs (requires tesseract-ocr)
            logger.info("PDF parser: falling back to OCR (scanned PDF detected)")
            doc = pymupdf.open(tmp.name)
            ocr_pages: list[str] = []
            for page in doc:
                tp = page.get_textpage_ocr(language="eng", dpi=300, full=True)
                text = page.get_text(textpage=tp)
                if text.strip():
                    ocr_pages.append(text)
            doc.close()
            md = "\n\n".join(ocr_pages)
            logger.info("PDF parser: OCR → %d chars", len(md))

    finally:
        os.unlink(tmp.name)

    result = _normalise(md)
    logger.info("PDF parser: final text length %d chars", len(result))
    return result


def _parse_docx(content: bytes) -> str:
    from docx import Document
    from docx.oxml.ns import qn

    doc = Document(io.BytesIO(content))
    lines: list[str] = []

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue
        style = para.style.name if para.style else ""
        if style.startswith("Heading 1"):
            lines.append(f"# {text}")
        elif style.startswith("Heading 2"):
            lines.append(f"## {text}")
        elif style.startswith("Heading 3"):
            lines.append(f"### {text}")
        elif style.startswith("Heading 4"):
            lines.append(f"#### {text}")
        else:
            lines.append(text)

    return _normalise("\n\n".join(lines))


def _normalise(text: str) -> str:
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = "\n".join(line.rstrip() for line in text.splitlines())
    return text.strip()
