from src.rag.retriever import Retriever


retriever = Retriever(
    index_path="data/faiss.index",
    metadata_path="data/metadata.json"
)

query = "Bir takım kaç kişiden oluşabilir?"

results = retriever.retrieve(
    query,
    k=3
)

print("QUERY:")
print(query)

print("\n--- TOP 3 RESULTS ---")

for result in results:
    print("\nDistance:", result["distance"])
    print("Section:", result["section"])
    print("Question:", result["question"])
    print("Answer:", result["answer"])