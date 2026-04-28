"""
LLM-based structural re-ranker (Stage 2 of two-stage retrieval).

Given a question and a shortlist of candidate nodes (each with a breadcrumb
path that describes where in the document it lives), asks the chat model to
re-rank them by *structural* relevance — i.e. which sections are most likely,
based on their position in the document hierarchy, to contain the answer.

This is deliberately separate from embedding similarity: a section whose
breadcrumb indicates it is about "Contract Formation > Offer and Acceptance"
is structurally relevant to a question about contract validity even if the
specific chunk that surfaced it only contains an oblique reference.
"""
from __future__ import annotations

import json
import re

from openai import AsyncOpenAI

from app.core.config import settings

_SYSTEM = """You are re-ranking document sections by structural relevance to a legal question.

Your goal is NOT to assess whether the retrieved text chunks contain the answer directly.
Instead, assess which sections — based on their hierarchical breadcrumb paths — are most
likely to address the question's topic comprehensively.

You will receive:
  - The user's question
  - A numbered list of candidate sections, each showing its breadcrumb path

Return a JSON array of the candidate indices (0-based integers) ordered from most to least
structurally relevant. Include only indices that have genuine relevance.
Return at most {top_n} indices.

Respond ONLY with the JSON array — no explanation, no markdown fences.
Example: [2, 0, 4]"""


async def rerank(
    question: str,
    candidates: list[dict],
    top_n: int,
) -> list[dict]:
    """
    Re-rank candidates by structural relevance.

    Each candidate dict must have at minimum:
        - "breadcrumb": str
        - (any other keys are passed through unchanged)

    Returns a re-ordered sub-list of at most top_n candidates.
    Falls back to the original ordering if the LLM call fails.
    """
    if not candidates:
        return []
    if len(candidates) <= 1:
        return candidates[:top_n]

    lines = "\n".join(f"{i}: {c['breadcrumb']}" for i, c in enumerate(candidates))
    user_message = f"Question: {question}\n\nCandidate sections:\n{lines}"

    client = AsyncOpenAI(api_key=settings.openai_api_key)
    try:
        response = await client.chat.completions.create(
            model=settings.chat_model,
            temperature=0,
            max_tokens=128,
            messages=[
                {"role": "system", "content": _SYSTEM.format(top_n=top_n)},
                {"role": "user", "content": user_message},
            ],
        )
        raw = (response.choices[0].message.content or "").strip()
        indices = _parse_index_list(raw, len(candidates))
    except Exception:
        indices = list(range(min(top_n, len(candidates))))

    # Build re-ranked list, fall back to original order for any missing items
    seen: set[int] = set()
    result: list[dict] = []
    for idx in indices:
        if 0 <= idx < len(candidates) and idx not in seen:
            result.append(candidates[idx])
            seen.add(idx)
        if len(result) == top_n:
            break

    # Pad with un-selected candidates if fewer than top_n were returned
    for i, c in enumerate(candidates):
        if len(result) == top_n:
            break
        if i not in seen:
            result.append(c)

    return result[:top_n]


def _parse_index_list(text: str, max_index: int) -> list[int]:
    """Extract a JSON integer array from an LLM response robustly."""
    def _from_list(data: object) -> list[int] | None:
        if not isinstance(data, list):
            return None
        result = []
        for x in data:
            try:
                result.append(int(x))
            except (TypeError, ValueError):
                pass
        return result if result else None

    try:
        data = json.loads(text)
        parsed = _from_list(data)
        if parsed is not None:
            return [i for i in parsed if 0 <= i < max_index]
    except json.JSONDecodeError:
        pass

    match = re.search(r"\[[\d,\s]+\]", text)
    if match:
        try:
            data = json.loads(match.group(0))
            parsed = _from_list(data)
            if parsed is not None:
                return [i for i in parsed if 0 <= i < max_index]
        except json.JSONDecodeError:
            pass

    return []
