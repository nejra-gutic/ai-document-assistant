from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_core.embeddings import Embeddings

from src.rag.embedder import Embedder
from src.rag.generator import Generator, build_prompt


class LangChainEmbeddings(Embeddings):
    def __init__(self, embedder: Embedder):
        self.embedder = embedder

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        embeddings = self.embedder.embed_texts(texts)

        return embeddings.tolist()

    def embed_query(self, text: str) -> list[float]:
        embedding = self.embedder.embed_text(text)

        return embedding.tolist()


def create_documents(chunks: list[str]) -> list[Document]:
    documents = []

    for chunk in chunks:
        documents.append(
            Document(
                page_content=chunk
            )
        )

    return documents

def create_qa_documents(
    qa_items: list[dict]
) -> list[Document]:
    documents = []

    for item in qa_items:
        documents.append(
            Document(
                page_content=item["text"],
                metadata={
                    "section": item.get("section", ""),
                    "question": item.get("question", ""),
                    "answer": item.get("answer", "")
                }
            )
        )

    return documents


def create_vector_store(
    documents: list[Document],
    embedder: Embedder
) -> FAISS:

    langchain_embeddings = LangChainEmbeddings(
        embedder=embedder
    )

    vector_store = FAISS.from_documents(
        documents=documents,
        embedding=langchain_embeddings
    )

    return vector_store


def create_retriever(vector_store: FAISS):
    retriever = vector_store.as_retriever(
        search_kwargs={"k": 3}
    )

    return retriever


class LangChainRAGService:
    def __init__(
        self,
        documents: list[Document],
        embedder: Embedder
    ):
        self.embedder = embedder

        self.vector_store = create_vector_store(
            documents=documents,
            embedder=embedder
        )

        self.retriever = create_retriever(
            self.vector_store
        )

        self.uploaded_vector_store = None
        self.uploaded_retriever = None

        self.generator = Generator()
        self.history = []

    def retrieve(
        self,
        query: str,
        k: int = 3
    ) -> list[Document]:

        results = []

        fixed_results = self.vector_store.similarity_search_with_score(
            query,
            k=k
        )

        for document, score in fixed_results:
            document.metadata["source"] = "fixed"
            results.append(
                (document, score)
            )

        if self.uploaded_vector_store:
            uploaded_results = (
                self.uploaded_vector_store.similarity_search_with_score(
                    query,
                    k=k
                )
            )

            for document, score in uploaded_results:
                document.metadata["source"] = "uploaded"
                results.append(
                    (document, score)
                )

        results.sort(
            key=lambda item: item[1]
        )

        top_results = results[:k]

        return [
            document
            for document, score in top_results
        ]

    def ask_question(
        self,
        query: str
    ) -> str:
        documents = self.retrieve(query)

        retrieved_results = []

        for document in documents:
            retrieved_results.append({
                "text": document.page_content,
                "section": document.metadata.get("section", ""),
                "question": document.metadata.get("question", ""),
                "answer": document.metadata.get("answer", "")
            })

        prompt = build_prompt(
            query=query,
            retrieved_results=retrieved_results,
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