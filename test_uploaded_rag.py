from src.rag.retriever import Retriever


retriever = Retriever(
    index_path="data/uploaded_faiss.index",
    metadata_path="data/uploaded_metadata.json"
)

query = "Bir takım kaç kişiden oluşabilir?"

results = retriever.retrieve(
    query,
    k=5
)

for i, result in enumerate(results, start=1):
    print(f"\n--- RESULT {i} ---")
    print("Distance:", result["distance"])
    print(result["text"])