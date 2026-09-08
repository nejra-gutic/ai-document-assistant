import os
import base64

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

    def describe_image(
        self,
        image_path: str,
        mime_type: str = "image/png"
    ) -> str:

        with open(image_path, "rb") as image_file:
            image_bytes = image_file.read()

        image_base64 = base64.b64encode(
            image_bytes
        ).decode("utf-8")

        interaction = self.client.interactions.create(
            model="gemini-3.6-flash",
            input=[
                {
                    "type": "image",
                    "data": image_base64,
                    "mime_type": mime_type
                },
                {
                    "type": "text",
                    "text": (
                        "Describe this image in detail. "
                        "If it is a chart, include all important values, labels, "
                        "and relationships. If it is a diagram, explain its structure."
                    )
                }
            ]
        )

        return interaction.output_text.strip()

    def generate(self, prompt: str) -> str:
        interaction = self.client.interactions.create(
            model="gemini-3.6-flash",
            input=prompt
        )

        return interaction.output_text.strip()