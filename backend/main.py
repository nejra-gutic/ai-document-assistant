from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"message": "AI Document Assistant API"}

@app.get("/documents")
def get_documents():
    return [
        {"id": 1, "name": "Company Handbook.pdf"},
        {"id": 2, "name": "University Regulations.pdf"}
    ]


@app.get("/documents/{document_id}")
def get_document(document_id: int):
    return {
        "id": document_id,
        "name": "Example Document.pdf"
    }