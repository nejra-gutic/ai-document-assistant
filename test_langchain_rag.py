import json

from src.rag.embedder import Embedder
from src.rag.langchain_service import (
    LangChainRAGService,
    create_qa_documents
)


with open(
    "data/metadata.json",
    "r",
    encoding="utf-8"
) as file:
    qa_items = json.load(file)


documents = create_qa_documents(
    qa_items
)

embedder = Embedder()

service = LangChainRAGService(
    documents=documents,
    embedder=embedder
)


question = "Bir takım kaç kişiden oluşabilir?"

answer = service.ask_question(
    question
)

print("QUESTION:")
print(question)

print("\nANSWER:")
print(answer)