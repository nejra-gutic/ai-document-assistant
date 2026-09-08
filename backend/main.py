import json

import pymupdf

from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.rag.generator import Generator

from backend.database import engine
from backend import models

from src.rag.embedder import Embedder
from src.rag.generic_chunker import split_into_chunks
from src.rag.langchain_service import (
    LangChainRAGService,
    create_qa_documents,
    create_documents,
    create_vector_store,
    create_retriever,
    create_image_documents,
    create_page_documents,
)

from sqlalchemy.orm import Session

from backend.database import SessionLocal



app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
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
    conversation_id: int
    question: str


class ChatResponse(BaseModel):
    answer: str

class ConversationResponse(BaseModel):
    id: int

# --------------------------------------------------
# Database Connection
# --------------------------------------------------


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

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
def get_documents(
    db: Session = Depends(get_db)
):
    documents = db.query(models.Document).all()

    return documents


@app.get("/documents/{document_id}")
def get_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    document = db.query(models.Document).filter(
        models.Document.id == document_id
    ).first()

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return document


@app.post(
    "/documents",
    status_code=201
)
def create_document(
    document: DocumentCreate,
    db: Session = Depends(get_db)
):
    new_document = models.Document(
        name=document.name
    )

    db.add(new_document)
    db.commit()
    db.refresh(new_document)

    return new_document


@app.put("/documents/{document_id}")
def update_document(
    document_id: int,
    document: DocumentUpdate,
    db: Session = Depends(get_db)
):
    existing_document = db.query(models.Document).filter(
        models.Document.id == document_id
    ).first()

    if not existing_document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    existing_document.name = document.name

    db.commit()
    db.refresh(existing_document)

    return existing_document


@app.patch("/documents/{document_id}")
def partially_update_document(
    document_id: int,
    document: DocumentUpdate,
    db: Session = Depends(get_db)
):
    existing_document = db.query(models.Document).filter(
        models.Document.id == document_id
    ).first()

    if not existing_document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    if document.name is not None:
        existing_document.name = document.name

    db.commit()
    db.refresh(existing_document)

    return existing_document


@app.delete("/documents/{document_id}")
def delete_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    existing_document = db.query(models.Document).filter(
        models.Document.id == document_id
    ).first()

    if not existing_document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    db.delete(existing_document)
    db.commit()

    return {
        "message": "Document deleted successfully"
    }


# --------------------------------------------------
# RAG Chat
# --------------------------------------------------
@app.post(
    "/api/conversations",
    response_model=ConversationResponse,
    status_code=201
)
def create_conversation(
    db: Session = Depends(get_db)
):
    conversation = models.Conversation()

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return ConversationResponse(
        id=conversation.id
    )


@app.post(
    "/api/chat",
    response_model=ChatResponse
)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    try:
        conversation = db.query(
            models.Conversation
        ).filter(
            models.Conversation.id == request.conversation_id
        ).first()

        if not conversation:
            raise HTTPException(
                status_code=404,
                detail="Conversation not found"
            )

        user_message = models.Message(
            conversation_id=request.conversation_id,
            role="user",
            content=request.question
        )

        db.add(user_message)
        db.commit()

        answer = rag_service.ask_question(
            request.question
        )

        assistant_message = models.Message(
            conversation_id=request.conversation_id,
            role="assistant",
            content=answer
        )

        db.add(assistant_message)
        db.commit()

        return ChatResponse(
            answer=answer
        )

    except HTTPException:
        raise

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
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
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

    page_texts = []

    image_descriptions = []

    for page_number, page in enumerate(pdf):
        page_texts.append({
            "text": page.get_text(),
            "page": page_number + 1
        })

        images = page.get_images(full=True)

        print(
            f"Page {page_number + 1}: {len(images)} images"
        )

        for image_number, image in enumerate(images):
            xref = image[0]

            image_info = pdf.extract_image(xref)
            image_bytes = image_info["image"]
            image_extension = image_info["ext"]

            filename = (
                f"page_{page_number + 1}_"
                f"image_{image_number + 1}.{image_extension}"
            )

            with open(filename, "wb") as image_file:
                image_file.write(image_bytes)

            generator = Generator()

            description = generator.describe_image(
                filename
            )

            image_descriptions.append({
                "description": description,
                "page": page_number + 1
            })

            print("IMAGE DESCRIPTION:")
            print(description)

    text_documents = create_page_documents(
        page_texts
    )

    image_documents = create_image_documents(
        image_descriptions
    )

    uploaded_documents = (
        text_documents
        + image_documents
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

    new_document = models.Document(
        name=file.filename
    )

    db.add(new_document)
    db.commit()
    db.refresh(new_document)

    return {
        "filename": file.filename,
        "text_chunks": len(text_documents),
        "image_chunks": len(image_documents),
        "total_chunks": len(uploaded_documents)
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

