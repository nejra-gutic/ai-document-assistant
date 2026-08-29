from src.rag.service import RAGService


rag_service = RAGService(
    index_path="data/uploaded_faiss.index",
    metadata_path="data/uploaded_metadata.json"
)

query = "What university did Nejra attend?"

answer = rag_service.ask_question(
    query,
    k=3
)

print("QUESTION:")
print(query)

print("\nANSWER:")
print(answer)