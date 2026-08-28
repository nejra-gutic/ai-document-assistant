def build_prompt(query: str, retrieved_results: list[dict]) -> str:
    context_parts = []

    for i, result in enumerate(retrieved_results, start=1):
        context_parts.append(
            f"""
Source {i}
Section: {result["section"]}
Question: {result["question"]}
Answer: {result["answer"]}
"""
        )

    context = "\n".join(context_parts)

    prompt = f"""
You are a helpful assistant.

Answer the user's question in Turkish using only the context below.
If the answer cannot be found in the context, say in Turkish that you do not have enough information.

CONTEXT:
{context}

USER QUESTION:
{query}

ANSWER:
"""

    return prompt