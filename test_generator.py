from src.rag.retriever import Retriever
from src.rag.generator import build_prompt, Generator


retriever = Retriever(
    index_path="data/faiss.index",
    metadata_path="data/metadata.json"
)

query = "Bir takım kaç kişiden oluşabilir?"

results = retriever.retrieve(
    query,
    k=3
)

prompt = build_prompt(
    query,
    results
)

generator = Generator()

answer = generator.generate(prompt)

print("\nANSWER:")
print(answer)