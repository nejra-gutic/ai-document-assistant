from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.database import engine
from backend import models

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


class DocumentCreate(BaseModel):
    name: str


class DocumentUpdate(BaseModel):
    name: str


documents = [
    {"id": 1, "name": "Company Handbook.pdf"},
    {"id": 2, "name": "University Regulations.pdf"}
]


@app.get("/")
def home():
    return {"message": "AI Document Assistant API"}


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
def update_document(document_id: int, document: DocumentUpdate):
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