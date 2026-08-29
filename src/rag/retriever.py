import json

from src.rag.embedder import Embedder
from src.rag.vector_store import VectorStore


class Retriever:
    def __init__(
        self,
        index_path: str,
        metadata_path: str,
        embedder: Embedder
    ):
        # 1. Load metadata
        with open(
            metadata_path,
            "r",
            encoding="utf-8"
        ) as file:
            self.metadata = json.load(file)

        # 2. Load embedding model
        self.embedder = embedder

        # 3. Load FAISS index
        self.vector_store = VectorStore(dimension=384)
        self.vector_store.load(index_path)

    def retrieve(self, query: str, k: int = 3) -> list[dict]:
        query_embedding = self.embedder.embed_text(query)

        distances, indices = self.vector_store.search(
            query_embedding,
            k=k
        )

        results = []

        for distance, index in zip(distances, indices):
            item = self.metadata[index]

            results.append({
                "distance": float(distance),
                "section": item.get("section", ""),
                "question": item.get("question", ""),
                "answer": item.get("answer", ""),
                "text": item["text"]
            })

        return results
    