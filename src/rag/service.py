from src.rag.retriever import Retriever
from src.rag.generator import build_prompt, Generator


class RAGService:
    def __init__(
        self,
        index_path: str,
        metadata_path: str
    ):
        self.retriever = Retriever(
            index_path=index_path,
            metadata_path=metadata_path
        )

        self.generator = Generator()

        self.history = []


    def ask_question(
        self,
        query: str,
        k: int = 3
    ) -> str:

        # R = Retrieval
        results = self.retriever.retrieve(
            query,
            k=k
        )

        # A = Augmentation
        prompt = build_prompt(
            query=query,
            retrieved_results=results,
            history=self.history
        )

        # G = Generation
        answer = self.generator.generate(
            prompt
        )

        self.history.append({
            "question": query,
            "answer": answer
        })

        return answer