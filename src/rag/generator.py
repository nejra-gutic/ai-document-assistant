import os

from dotenv import load_dotenv
from google import genai


load_dotenv()


def build_prompt(query: str, retrieved_results: list[dict]) -> str:
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

    prompt = f"""
You are a helpful assistant.

Answer the user's question using only the context below.
Respond in the same language as the user's question.

Rules:
- Give only the final answer.
- Do not add notes, explanations about your reasoning, or extra questions.
- Do not repeat the user's question.
- If different sources contain different answers, mention the difference clearly.
- If the answer is not in the context, say in Turkish that there is not enough information.

CONTEXT:
{context}

USER:
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