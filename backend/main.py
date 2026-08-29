import json

import pymupdf

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.database import engine
from backend import models

from src.rag.embedder import Embedder
from src.rag.generic_chunker import split_into_chunks
from src.rag.langchain_service import (
    LangChainRAGService,
    create_qa_documents,
    create_documents,
    create_vector_store,
    create_retriever
)


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


models.Base.metadata.create_all(
    bind=engine
)


# --------------------------------------------------
# Fixed RAG knowledge base
# --------------------------------------------------

with open(
    "data/metadata.json",
    "r",
    encoding="utf-8"
) as file:
    qa_items = json.load(file)


fixed_documents = create_qa_documents(
    qa_items
)


embedder = Embedder()


rag_service = LangChainRAGService(
    documents=fixed_documents,
    embedder=embedder
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
    {
        "id": 1,
        "name": "Company Handbook.pdf"
    },
    {
        "id": 2,
        "name": "University Regulations.pdf"
    }
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


@app.post(
    "/documents",
    status_code=201
)
def create_document(
    document: DocumentCreate
):
    new_document = {
        "id": len(documents) + 1,
        "name": document.name
    }

    documents.append(
        new_document
    )

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
def delete_document(
    document_id: int
):
    for document in documents:
        if document["id"] == document_id:
            documents.remove(
                document
            )

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
def chat(
    request: ChatRequest
):
    try:
        answer = rag_service.ask_question(
            request.question
        )

        return ChatResponse(
            answer=answer
        )

    except Exception as error:
        error_message = str(error)

        if (
            "429" in error_message
            or "too_many_requests" in error_message
        ):
            raise HTTPException(
                status_code=429,
                detail=(
                    "AI service rate limit reached. "
                    "Please try again shortly."
                )
            )

        raise HTTPException(
            status_code=500,
            detail=(
                "Something went wrong while "
                "generating the answer."
            )
        )


# --------------------------------------------------
# PDF Upload
# --------------------------------------------------

@app.post("/api/documents/upload")
async def upload_document(
    file: UploadFile = File(...)
):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    pdf_bytes = await file.read()

    pdf = pymupdf.open(
        stream=pdf_bytes,
        filetype="pdf"
    )

    text = ""

    for page in pdf:
        text += page.get_text()

    chunks = split_into_chunks(
        text
    )

    uploaded_documents = create_documents(
        chunks
    )

    uploaded_vector_store = create_vector_store(
        documents=uploaded_documents,
        embedder=embedder
    )

    rag_service.uploaded_vector_store = uploaded_vector_store

    rag_service.uploaded_retriever = create_retriever(
        uploaded_vector_store
    )

    rag_service.history = []
    
    return {
        "filename": file.filename,
        "number_of_chunks": len(chunks)
    }


# --------------------------------------------------
# Chat Reset
# --------------------------------------------------

@app.post("/api/chat/reset")
def reset_chat():
    rag_service.history = []

    return {
        "message": "Chat history cleared"
    }