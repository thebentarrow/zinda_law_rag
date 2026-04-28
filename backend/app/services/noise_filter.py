"""
LLM-based noise filter for skeleton tree nodes.

Sends node headings + breadcrumbs to the chat model and asks it to identify
nodes that are structural noise rather than substantive content.

Six noise categories (matching the article):
  1. Table of contents / index entries
  2. Repeated page headers or footers
  3. Boilerplate (copyright, disclaimers, contact info, revision history)
  4. Navigation elements (see also, further reading, glossary stubs)
  5. Document metadata (version, date, author blocks)
  6. Empty or trivially short sections (fewer than ~30 words of content)
"""
from __future__ import annotations

import json
import logging
import re

from openai import AsyncOpenAI

from app.core.config import settings
from app.services.skeleton_builder import SectionNode

logger = logging.getLogger(__name__)

_SYSTEM = """You are filtering structural noise from a legal document skeleton.

Remove ONLY nodes that are clearly structural scaffolding with no substantive legal content:
1. Table of contents or index pages (lists of section titles and page numbers only)
2. Repeated page headers or footers (document title, page number, date repeated on every page)
3. Pure boilerplate with no legal substance: copyright lines, printing instructions, blank pages
4. Navigation stubs: "See also", "Further reading", standalone reference lists
5. Document metadata blocks: version history tables, author/approver signature blocks

Do NOT remove:
- Legal clauses, definitions, or obligations — even if they are short
- Numbered sections (1. 2. 1.1 etc.) — these are substantive contract or statute content
- Sections with fewer than 30 words — brevity does not make a clause noise
- Recitals, whereas clauses, or preamble text

You will receive a JSON array of skeleton nodes. Each node has "node_id", "heading",
"breadcrumb", "word_count", and "content_preview" (first 120 chars of content).
Return a JSON array of node_ids to exclude. If nothing qualifies, return [].

Respond ONLY with the JSON array — no explanation, no markdown fences."""


async def filter_noise(nodes: list[SectionNode]) -> list[SectionNode]:
    """Return nodes with noise entries removed."""
    if not nodes:
        return nodes

    skeleton_payload = [
        {
            "node_id": n.node_id,
            "heading": n.heading,
            "breadcrumb": n.breadcrumb,
            "word_count": len(n.full_section_text.split()),
            "content_preview": n.full_section_text[:120].replace("\n", " "),
        }
        for n in nodes
    ]

    logger.info("Noise filter: evaluating %d sections", len(nodes))

    client = AsyncOpenAI(api_key=settings.openai_api_key)
    response = await client.chat.completions.create(
        model=settings.chat_model,
        temperature=0,
        max_tokens=512,
        messages=[
            {"role": "system", "content": _SYSTEM},
            {"role": "user", "content": json.dumps(skeleton_payload)},
        ],
    )

    raw = (response.choices[0].message.content or "").strip()
    noise_ids = _parse_id_list(raw)

    if noise_ids:
        logger.info("Noise filter: removing %d sections: %s", len(noise_ids), noise_ids)
        keep = [n for n in nodes if n.node_id not in noise_ids]
        result = keep if keep else nodes  # never return empty
        logger.info("Noise filter: %d sections remaining", len(result))
        return result

    logger.info("Noise filter: no sections removed")
    return nodes


def _parse_id_list(text: str) -> set[str]:
    """Extract a JSON array of strings from an LLM response robustly."""
    try:
        data = json.loads(text)
        if isinstance(data, list):
            return {str(x) for x in data if isinstance(x, str)}
    except json.JSONDecodeError:
        pass

    # Try to find an array embedded in surrounding text
    match = re.search(r"\[.*?\]", text, re.DOTALL)
    if match:
        try:
            data = json.loads(match.group(0))
            if isinstance(data, list):
                return {str(x) for x in data if isinstance(x, str)}
        except json.JSONDecodeError:
            pass

    return set()
