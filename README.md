# AI Document Assistant

A full-stack AI document assistant that allows users to upload PDF documents and ask questions about their content using a Retrieval-Augmented Generation (RAG) pipeline.

The application retrieves relevant parts of the document using semantic search and uses a large language model to generate answers grounded in the retrieved document context.

## Features

- PDF document upload
- Automatic text extraction from PDF files
- Text chunking with overlapping chunks
- Sentence-transformer embeddings
- FAISS vector search
- Retrieval-Augmented Generation (RAG)
- Gemini-based answer generation
- Conversation history for follow-up questions
- Chat reset functionality
- Loading and error states
- React-based chat interface
- FastAPI REST API

## How It Works

The document processing pipeline:

```text
PDF Upload
    ↓
Text Extraction
    ↓
Text Chunking
    ↓
Embedding Generation
    ↓
FAISS Vector Index
```

When the user asks a question:

```text
User Question
    ↓
Question Embedding
    ↓
FAISS Similarity Search
    ↓
Relevant Document Chunks
    ↓
Conversation History
    ↓
Prompt Construction
    ↓
Gemini
    ↓
Generated Answer
```

This approach allows the language model to answer questions using information retrieved from the uploaded document instead of relying only on its general knowledge.

## Tech Stack

### Backend

- Python
- FastAPI
- PyMuPDF
- Sentence Transformers
- FAISS
- Google Gemini API

### Frontend

- React
- JavaScript
- CSS
- Vite

## Project Structure

```text
ai-document-assistant/
├── backend/
│   └── main.py
│
├── frontend/
│   └── src/
│       ├── App.jsx
│       ├── App.css
│       └── index.css
│
├── src/
│   └── rag/
│       ├── embedder.py
│       ├── generator.py
│       ├── retriever.py
│       ├── service.py
│       └── vector_store.py
│
├── data/
├── requirements.txt
└── README.md
```

## RAG Pipeline

### 1. Document Processing

When a PDF is uploaded, the backend extracts its text using PyMuPDF.

The extracted text is split into smaller overlapping chunks so that relevant information can later be retrieved efficiently.

### 2. Embeddings

Each chunk is converted into a numerical vector representation using a Sentence Transformer embedding model.

### 3. Vector Search

The embeddings are stored in a FAISS index.

When a question is submitted, the question is also converted into an embedding and FAISS retrieves the document chunks that are semantically closest to the question.

### 4. Answer Generation

The retrieved chunks are added to the prompt as document context.

Recent conversation history is also included so that the assistant can understand follow-up questions.

The final prompt is sent to Gemini, which generates an answer based on the retrieved context.

## API Endpoints

### Upload a document

```http
POST /api/documents/upload
```

Processes a PDF document, creates its embeddings and builds the FAISS index.

### Ask a question

```http
POST /api/chat
```

Example request:

```json
{
  "question": "What university did Nejra attend?"
}
```

Example response:

```json
{
  "answer": "Istanbul Technical University."
}
```

### Reset conversation

```http
POST /api/chat/reset
```

Clears the current conversation history.

## Running the Project

### Backend

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file and add:

```text
GEMINI_API_KEY=your_api_key
```

Start the FastAPI server:

```bash
uvicorn backend.main:app --reload
```

The API will run locally on port `8000`.

FastAPI Swagger documentation is available at:

```text
http://127.0.0.1:8000/docs
```

### Frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

The React application will run locally through Vite.

## Current Status

The core RAG workflow is functional:

- document upload
- document processing
- embedding generation
- FAISS indexing
- semantic retrieval
- LLM answer generation
- conversation history
- React chat interface

The next development step is persistent storage using PostgreSQL for documents, conversations, and chat messages.

## Planned Improvements

- PostgreSQL persistence
- Persistent conversation history
- Multiple document support
- User authentication
- Improved document management
- Source references in generated answers
- Dockerized development environment
- Deployment

## Author

**Nejra Gutić**

Computer Engineering graduate interested in software engineering, AI, NLP, and full-stack development.