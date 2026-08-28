import faiss
import numpy as np


class VectorStore:
    def __init__(self, dimension: int):
        self.index = faiss.IndexFlatL2(dimension)

    def add(self, embeddings):
        embeddings = np.asarray(
            embeddings,
            dtype="float32"
        )

        self.index.add(embeddings)

    def search(self, query_embedding, k: int = 3):
        query_embedding = np.asarray(
            [query_embedding],
            dtype="float32"
        )

        distances, indices = self.index.search(
            query_embedding,
            k
        )

        return distances[0], indices[0]