from transformers import AutoModelForCausalLM, AutoTokenizer


MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"


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

Rules:
- Give only the final answer.
- Do not add notes, explanations about your reasoning, or extra questions.
- Do not repeat the user's question.
- If different sections contain different answers, you MUST mention each section separately.
- Do not choose one section and ignore the others.
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
        self.tokenizer = AutoTokenizer.from_pretrained(
            MODEL_NAME
        )

        self.model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME
        )

    def generate(self, prompt: str) -> str:
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt"
        )

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=100,
            do_sample=False
        )

        input_length = inputs["input_ids"].shape[1]

        generated_tokens = outputs[0][input_length:]

        generated_text = self.tokenizer.decode(
            generated_tokens,
            skip_special_tokens=True
        )

        return generated_text.strip()