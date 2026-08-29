import os

from dotenv import load_dotenv
from google import genai


load_dotenv()


def build_prompt(
    query: str,
    retrieved_results: list[dict],
    history: list[dict]
) -> str:
    context_parts = []

    for i, result in enumerate(retrieved_results, start=1):
        if result.get("question") and result.get("answer"):
            context_parts.append(
                f"""
Source {i}
Section: {result.get("section", "")}
Question: {result["question"]}
Answer: {result["answer"]}
"""
            )
        else:
            context_parts.append(
                f"""
Source {i}
Content:
{result["text"]}
"""
            )

    context = "\n".join(context_parts)

    history_parts = []

    for item in history[-5:]:
        history_parts.append(
            f"""
User: {item["question"]}
Assistant: {item["answer"]}
"""
        )

    conversation_history = "\n".join(history_parts)

    prompt = f"""
You are a helpful assistant.

Answer the user's question using only the document context and conversation history below.
Respond in the same language as the user's question.

Rules:
- Give only the final answer.
- Do not add notes, explanations about your reasoning, or extra questions.
- Do not repeat the user's question.
- Use conversation history to understand follow-up questions.
- Use the document context as the source of factual information.
- If the answer cannot be determined from the document context and conversation history, say that there is not enough information in the same language as the user's question.

CONVERSATION HISTORY:
{conversation_history}

DOCUMENT CONTEXT:
{context}

CURRENT USER QUESTION:
{query}

RESPONSE:
"""

    return prompt


class Generator:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set.")

        self.client = genai.Client(
            api_key=api_key
        )

    def generate(self, prompt: str) -> str:
        interaction = self.client.interactions.create(
            model="gemini-3.6-flash",
            input=prompt
        )

        return interaction.output_text.strip()