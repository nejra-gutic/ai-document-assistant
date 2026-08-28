import random

from src.rag.pipeline import build_qa_dataset


PDF_PATH = "data/rag-example-qa.pdf"

all_qa = build_qa_dataset(PDF_PATH)

print("Ukupno Q&A:", len(all_qa))


random_qa = random.choice(all_qa)

print("\n--- RANDOM Q&A ---")

print("\nSECTION:")
print(random_qa["section"])

print("\nQUESTION:")
print(random_qa["question"])

print("\nANSWER:")
print(random_qa["answer"])