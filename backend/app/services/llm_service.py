from openai import AsyncOpenAI

from app.core.config import settings

_SYSTEM_PROMPT = """You are a knowledgeable legal information assistant.
You answer questions clearly and accurately using only the provided context.
Always frame your answers as general legal information, not as advice for a specific situation.
If the context does not contain sufficient information to answer the question, say so honestly rather than speculating.
Do not invent case law, statutes, or legal principles not present in the context.
Always include a disclaimer that your response is informational only and does not constitute legal advice."""


class LLMService:
    def __init__(self) -> None:
        self._client = AsyncOpenAI(api_key=settings.openai_api_key)

    async def generate(self, question: str, context_pieces: list[dict]) -> str:
        context_blocks = []
        for piece in context_pieces:
            if piece["type"] == "faq":
                context_blocks.append(
                    f"FAQ — {piece['title']}\nQ: {piece['question']}\nA: {piece['answer']}"
                )
            else:
                context_blocks.append(
                    f"Document excerpt — {piece['source']}\n{piece['content']}"
                )

        context_text = "\n\n".join(context_blocks) if context_blocks else "No relevant context found."

        user_message = (
            f"Using the following legal context, answer the question below.\n\n"
            f"--- Context ---\n{context_text}\n\n"
            f"--- Question ---\n{question}"
        )

        response = await self._client.chat.completions.create(
            model=settings.chat_model,
            temperature=settings.chat_temperature,
            max_tokens=settings.chat_max_tokens,
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
        )
        return response.choices[0].message.content or ""
