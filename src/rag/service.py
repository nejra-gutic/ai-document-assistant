from src.rag.retriever import Retriever
from src.rag.generator import build_prompt, Generator


class RAGService:
    def __init__(
        self,
        fixed_index_path: str,
        fixed_metadata_path: str,
        uploaded_index_path: str | None = None,
        uploaded_metadata_path: str | None = None
    ):
        self.fixed_retriever = Retriever(
            index_path=fixed_index_path,
            metadata_path=fixed_metadata_path
        )

        self.uploaded_retriever = None

        if uploaded_index_path and uploaded_metadata_path:
            self.uploaded_retriever = Retriever(
                index_path=uploaded_index_path,
                metadata_path=uploaded_metadata_path
            )

        self.generator = Generator()
        self.history = []

    def ask_question(
        self,
        query: str,
        k: int = 3
    ) -> str:

        fixed_results = self.fixed_retriever.retrieve(
            query,
            k=k
        )

        uploaded_results = []

        if self.uploaded_retriever:
            uploaded_results = self.uploaded_retriever.retrieve(
                query,
                k=k
            )

        results = fixed_results + uploaded_results

        results = sorted(
            results,
            key=lambda item: item["distance"]
        )[:k]

        prompt = build_prompt(
            query=query,
            retrieved_results=results,
            history=self.history
        )

        answer = self.generator.generate(
            prompt
        )

        self.history.append({
            "question": query,
            "answer": answer
        })

        return answer