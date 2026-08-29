from src.rag.service import RAGService


rag_service = RAGService(
    index_path="data/faiss.index",
    metadata_path="data/metadata.json"
)

query = "Türkiye'nin başkenti neresidir?"

answer = rag_service.ask_question(
    query,
    k=3
)

print("QUESTION:")
print(query)

print("\nANSWER:")
print(answer)