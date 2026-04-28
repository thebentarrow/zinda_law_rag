"""
Build a flat list of SectionNodes from a document.

Markdown  → parse # / ## / ### headings precisely.
PDF/text  → heuristic detection of numbered sections and ALL-CAPS headings.
Fallback  → paragraph-based sections when no heading structure is found.

Each SectionNode carries:
  - breadcrumb          full ancestor path, e.g. "Contract Law > Formation > Offer"
  - content             text directly under this heading (no sub-section text)
  - full_section_text   heading + all descendant content (the "pointer" target)
"""
from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class SectionNode:
    node_id: str
    heading: str
    level: int
    breadcrumb: str
    content: str            # direct content only — used for chunking
    full_section_text: str  # complete section including all sub-sections — passed to LLM


def build_sections(text: str, source_name: str, doc_type: str) -> list[SectionNode]:
    """
    Entry point.

    Docling converts PDF and DOCX to markdown before this function is called,
    so all heading-bearing documents arrive here as markdown regardless of their
    original format.  We therefore try markdown parsing first and only fall back
    to heuristic text detection if no headings are found.
    """
    nodes = _from_markdown(text, source_name)

    if not nodes and doc_type == "text":
        nodes = _from_text(text, source_name)

    if not nodes:
        nodes = _fallback_paragraphs(text, source_name)

    return nodes


# ── Markdown ──────────────────────────────────────────────────────────────────

_MD_HEADING = re.compile(r"^(#{1,6})\s+(.+?)(?:\s+#+)?$", re.MULTILINE)


def _from_markdown(text: str, source_name: str) -> list[SectionNode]:
    matches = list(_MD_HEADING.finditer(text))
    if not matches:
        return []

    raw: list[dict] = []
    for i, m in enumerate(matches):
        level = len(m.group(1))
        heading = m.group(2).strip()
        content_start = m.end()
        content_end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        raw.append(
            {
                "idx": i,
                "level": level,
                "heading": heading,
                "direct_content": text[content_start:content_end].strip(),
                "match_start": m.start(),
            }
        )

    # full_section_text: this node's heading + everything until the next sibling/ancestor
    for i, sec in enumerate(raw):
        end = len(text)
        for j in range(i + 1, len(raw)):
            if raw[j]["level"] <= sec["level"]:
                end = raw[j]["match_start"]
                break
        marker = "#" * sec["level"]
        sec["full_section_text"] = f"{marker} {sec['heading']}\n\n{text[matches[i].end():end].strip()}"

    _attach_breadcrumbs(raw, source_name)
    return _to_nodes(raw)


# ── PDF / plain text ──────────────────────────────────────────────────────────

# Patterns tried in order; first match wins for a line.
_TEXT_HEADING_PATTERNS = [
    (re.compile(
        r"^(?:CHAPTER|ARTICLE|SECTION|PART)\s+[\w\-]+[:.—]?\s+\w",
        re.IGNORECASE | re.MULTILINE,
    ), 1),
    (re.compile(r"^\d+\.\d+\.\d+\s+[A-Z]\w.{2,60}$", re.MULTILINE), 3),
    (re.compile(r"^\d+\.\d+\s+[A-Z]\w.{2,60}$", re.MULTILINE), 2),
    (re.compile(r"^\d+\.\s+[A-Z]\w.{2,60}$", re.MULTILINE), 1),
    (re.compile(r"^[A-Z][A-Z\s\-]{5,55}$", re.MULTILINE), 1),  # ALL CAPS
]


def _from_text(text: str, source_name: str) -> list[SectionNode]:
    hits: list[tuple[int, int, str, int]] = []  # (start, end, heading_text, level)
    seen_starts: set[int] = set()

    for pattern, level in _TEXT_HEADING_PATTERNS:
        for m in pattern.finditer(text):
            if m.start() not in seen_starts:
                seen_starts.add(m.start())
                hits.append((m.start(), m.end(), m.group(0).strip(), level))

    hits.sort(key=lambda h: h[0])

    if len(hits) < 2:
        return []

    raw: list[dict] = []
    for i, (start, end, heading_text, level) in enumerate(hits):
        content_end = hits[i + 1][0] if i + 1 < len(hits) else len(text)
        raw.append(
            {
                "idx": i,
                "level": level,
                "heading": heading_text[:120],
                "direct_content": text[end:content_end].strip(),
                "full_section_text": text[start:content_end].strip(),
                "match_start": start,
            }
        )

    _attach_breadcrumbs(raw, source_name)
    return _to_nodes(raw)


# ── Fallback: paragraph blocks ────────────────────────────────────────────────

def _fallback_paragraphs(text: str, source_name: str) -> list[SectionNode]:
    # Use a low threshold (10 chars) so short-line documents (forms, tables,
    # bullet lists) still produce sections rather than an empty list.
    paras = [p.strip() for p in re.split(r"\n{2,}", text) if len(p.strip()) > 10]

    # Last resort: treat the entire text as one section so we never return [].
    if not paras:
        paras = [text.strip()] if text.strip() else []

    doc_label = _short_name(source_name)
    nodes = []
    for i, para in enumerate(paras):
        nodes.append(
            SectionNode(
                node_id=f"para_{i}",
                heading=f"Paragraph {i + 1}",
                level=1,
                breadcrumb=doc_label,
                content=para,
                full_section_text=para,
            )
        )
    return nodes


# ── Helpers ───────────────────────────────────────────────────────────────────

def _attach_breadcrumbs(raw: list[dict], source_name: str) -> None:
    doc_label = _short_name(source_name)
    stack: list[tuple[int, str]] = []  # (level, heading)
    for sec in raw:
        while stack and stack[-1][0] >= sec["level"]:
            stack.pop()
        stack.append((sec["level"], sec["heading"]))
        parts = [doc_label] + [h for _, h in stack]
        sec["breadcrumb"] = " > ".join(parts)


def _to_nodes(raw: list[dict]) -> list[SectionNode]:
    return [
        SectionNode(
            node_id=f"node_{s['idx']}",
            heading=s["heading"],
            level=s["level"],
            breadcrumb=s["breadcrumb"],
            content=s["direct_content"],
            full_section_text=s["full_section_text"],
        )
        for s in raw
    ]


def _short_name(source_name: str) -> str:
    """Strip extension and path separators for a clean document label."""
    name = re.sub(r"\.[^.]+$", "", source_name)
    name = re.sub(r"[/\\]", " / ", name)
    return name.strip() or source_name
