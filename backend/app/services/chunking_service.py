"""Split a long text into overlapping chunks suitable for embedding."""
from __future__ import annotations

CHUNK_SIZE = 1500   # characters (~375 tokens)
OVERLAP = 200       # characters carried over between chunks

# Preferred split points, tried in order (most natural → least natural)
_SEPARATORS = ["\n\n", "\n", ". ", " "]


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = OVERLAP) -> list[str]:
    if len(text) <= chunk_size:
        return [text] if text.strip() else []

    chunks: list[str] = []
    start = 0

    while start < len(text):
        end = start + chunk_size

        if end >= len(text):
            tail = text[start:].strip()
            if tail:
                chunks.append(tail)
            break

        split_at = _find_split(text, start, end)
        chunk = text[start:split_at].strip()
        if chunk:
            chunks.append(chunk)

        start = max(start + 1, split_at - overlap)

    return chunks


def _find_split(text: str, start: int, end: int) -> int:
    for sep in _SEPARATORS:
        pos = text.rfind(sep, start, end)
        if pos > start:
            return pos + len(sep)
    return end
