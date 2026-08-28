import json

from src.rag.embedder import Embedder
from src.rag.vector_store import VectorStore


class Retriever:
    def __init__(
        self,
        index_path: str,
        metadata_path: str
    ):
        # 1. Učitaj metadata
        with open(
            metadata_path,
            "r",
            encoding="utf-8"
        ) as file:
            self.metadata = json.load(file)

        # 2. Učitaj embedding model
        self.embedder = Embedder()

        # 3. Učitaj već napravljeni FAISS index
        self.vector_store = VectorStore(dimension=384)
        self.vector_store.load(index_path)

    def retrieve(self, query: str, k: int = 3) -> list[dict]:
        # 4. Napravi embedding korisničkog pitanja
        query_embedding = self.embedder.embed_text(query)

        # 5. Nađi k najsličnijih vektora
        distances, indices = self.vector_store.search(
            query_embedding,
            k=k
        )

        results = []

        # 6. Preko FAISS indexa pronađi originalni Q&A
        for distance, index in zip(distances, indices):
            qa = self.metadata[index]

            results.append({
                "distance": float(distance),
                "section": qa["section"],
                "question": qa["question"],
                "answer": qa["answer"],
                "text": qa["text"]
            })

        return results
    