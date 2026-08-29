from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from backend.database import engine
from backend import models
from src.rag.service import RAGService

from fastapi.middleware.cors import CORSMiddleware

from fastapi import UploadFile, File
import fitz

from src.rag.generic_chunker import split_into_chunks

import json

from src.rag.embedder import Embedder
from src.rag.vector_store import VectorStore


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

rag_service = RAGService(
    fixed_index_path="data/faiss.index",
    fixed_metadata_path="data/metadata.json"
)

# --------------------------------------------------
# Pydantic models
# --------------------------------------------------

class DocumentCreate(BaseModel):
    name: str


class DocumentUpdate(BaseModel):
    name: str


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str


# --------------------------------------------------
# Temporary in-memory documents
# --------------------------------------------------

documents = [
    {"id": 1, "name": "Company Handbook.pdf"},
    {"id": 2, "name": "University Regulations.pdf"}
]


# --------------------------------------------------
# Home
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "AI Document Assistant API"
    }


# --------------------------------------------------
# Documents CRUD
# --------------------------------------------------

@app.get("/documents")
def get_documents():
    return documents


@app.get("/documents/{document_id}")
def get_document(document_id: int):
    for document in documents:
        if document["id"] == document_id:
            return document

    raise HTTPException(
        status_code=404,
        detail="Document not found"
    )


@app.post("/documents", status_code=201)
def create_document(document: DocumentCreate):
    new_document = {
        "id": len(documents) + 1,
        "name": document.name
    }

    documents.append(new_document)

    return new_document


@app.put("/documents/{document_id}")
def update_document(
    document_id: int,
    document: DocumentUpdate
):
    for existing_document in documents:
        if existing_document["id"] == document_id:
            existing_document["name"] = document.name
            return existing_document

    raise HTTPException(
        status_code=404,
        detail="Document not found"
    )


@app.patch("/documents/{document_id}")
def partially_update_document(
    document_id: int,
    document: DocumentUpdate
):
    for existing_document in documents:
        if existing_document["id"] == document_id:
            existing_document["name"] = document.name
            return existing_document

    raise HTTPException(
        status_code=404,
        detail="Document not found"
    )


@app.delete("/documents/{document_id}")
def delete_document(document_id: int):
    for document in documents:
        if document["id"] == document_id:
            documents.remove(document)

            return {
                "message": "Document deleted successfully"
            }

    raise HTTPException(
        status_code=404,
        detail="Document not found"
    )


# --------------------------------------------------
# RAG Chat
# --------------------------------------------------

@app.post(
    "/api/chat",
    response_model=ChatResponse
)
def chat(request: ChatRequest):
    try:
        answer = rag_service.ask_question(
            request.question,
            k=3
        )

        return ChatResponse(
            answer=answer
        )

    except Exception as error:
        error_message = str(error)

        if "429" in error_message or "too_many_requests" in error_message:
            raise HTTPException(
                status_code=429,
                detail="AI service rate limit reached. Please try again shortly."
            )

        raise HTTPException(
            status_code=500,
            detail="Something went wrong while generating the answer."
        )
    
@app.post("/api/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    global rag_service

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    pdf_bytes = await file.read()

    pdf = fitz.open(
        stream=pdf_bytes,
        filetype="pdf"
    )

    text = ""

    for page in pdf:
        text += page.get_text()

    chunks = split_into_chunks(text)

    embedder = Embedder()
    embeddings = embedder.embed_texts(chunks)

    vector_store = VectorStore(
        dimension=embeddings.shape[1]
    )

    vector_store.add(embeddings)

    vector_store.save(
        "data/uploaded_faiss.index"
    )

    metadata = []

    for chunk in chunks:
        metadata.append({
            "text": chunk
        })

    with open(
        "data/uploaded_metadata.json",
        "w",
        encoding="utf-8"
    ) as metadata_file:
        json.dump(
            metadata,
            metadata_file,
            ensure_ascii=False,
            indent=2
        )

    rag_service = RAGService(
        fixed_index_path="data/faiss.index",
        fixed_metadata_path="data/metadata.json",
        uploaded_index_path="data/uploaded_faiss.index",
        uploaded_metadata_path="data/uploaded_metadata.json"
    )

    return {
        "filename": file.filename,
        "number_of_chunks": len(chunks)
    }