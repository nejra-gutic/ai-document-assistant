# 🤖 AI Document Assistant

A full-stack AI document assistant that allows users to upload PDF documents and ask questions about their content using **Retrieval-Augmented Generation (RAG)**.

The application uses semantic search to retrieve relevant parts of a document and provides them as context to a large language model, enabling answers grounded in the uploaded document.

![AI Document Assistant](docs/app-screenshot.png)

## ✨ Features

- Upload and process PDF documents
- Extract text automatically from uploaded PDFs
- Split documents into overlapping text chunks
- Generate semantic embeddings using Sentence Transformers
- Store and search embeddings with FAISS
- Retrieve document sections relevant to a user's question
- Generate document-grounded answers using Google Gemini
- Maintain conversation history for follow-up questions
- Start a new conversation without reloading the application
- Handle AI API rate limits and errors
- Interactive React chat interface
- REST API built with FastAPI

## 🧠 How It Works

The application uses a Retrieval-Augmented Generation pipeline.

### Document Processing

When a PDF is uploaded:

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

The document text is extracted and divided into smaller overlapping chunks. Each chunk is converted into a numerical embedding and stored in a FAISS vector index.

### Question Answering

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
Google Gemini
      ↓
Generated Answer
```

The user's question is converted into an embedding and compared with the document embeddings.

The most relevant chunks are retrieved and included in the prompt together with recent conversation history. This allows the assistant to answer questions based on the document while also understanding follow-up questions.

## 🛠️ Tech Stack

### Backend

- **Python**
- **FastAPI** — REST API
- **PyMuPDF** — PDF text extraction
- **Sentence Transformers** — semantic embeddings
- **FAISS** — vector similarity search
- **Google Gemini API** — answer generation

### Frontend

- **React**
- **JavaScript**
- **CSS**
- **Vite**

## 📁 Project Structure

```text
ai-document-assistant/
│
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
├── docs/
│   └── app-screenshot.png
│
├── requirements.txt
└── README.md
```

## 🔎 RAG Pipeline

### 1. PDF Text Extraction

Uploaded PDF documents are processed with PyMuPDF and their textual content is extracted.

### 2. Text Chunking

The extracted text is divided into smaller overlapping chunks.

Using smaller chunks makes it possible to retrieve only the parts of the document that are relevant to a particular question, while overlap helps preserve context between neighboring chunks.

### 3. Embedding Generation

Each text chunk is converted into a dense vector representation using a Sentence Transformer model.

Semantically similar pieces of text therefore have embeddings that are close to each other in vector space.

### 4. Vector Search

Document embeddings are stored in a FAISS index.

When a user submits a question, the question is embedded using the same embedding model and FAISS searches for the closest document vectors.

### 5. Context Retrieval

The most relevant document chunks are retrieved and used as context for the language model.

This is the **retrieval** part of the RAG pipeline.

### 6. Answer Generation

The retrieved context, current user question, and recent conversation history are combined into a prompt.

The prompt is sent to Google Gemini, which generates the final answer using the retrieved document information.

## 🔌 API Endpoints

### Upload Document

```http
POST /api/documents/upload
```

Uploads and processes a PDF document.

The backend:

1. extracts the document text,
2. creates text chunks,
3. generates embeddings,
4. creates a FAISS index,
5. stores metadata required for retrieval.

Example response:

```json
{
  "filename": "example.pdf",
  "number_of_chunks": 12
}
```

### Ask Question

```http
POST /api/chat
```

Example request:

```json
{
  "question": "What are the main requirements?"
}
```

Example response:

```json
{
  "answer": "The main requirements are..."
}
```

### Reset Conversation

```http
POST /api/chat/reset
```

Clears the current conversation history and starts a new chat.

## 💬 Conversation History

The assistant keeps recent question-answer pairs as conversation history.

This allows follow-up questions such as:

```text
User:
Where did she study?

Assistant:
She studied at Istanbul Technical University.

User:
What did she study there?
```

The second question can be interpreted using the previous conversation instead of being treated as a completely independent query.

Conversation history is currently stored in application memory.

Persistent conversation storage with PostgreSQL is planned as the next development step.

## 🚀 Running the Project

### 1. Clone the Repository

```bash
git clone <repository-url>
cd ai-document-assistant
```

### 2. Create a Python Virtual Environment

```bash
python -m venv .venv
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Install Backend Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```text
GEMINI_API_KEY=your_api_key
```

Do not commit the `.env` file to Git.

### 5. Start the Backend

```bash
uvicorn backend.main:app --reload
```

The backend will be available locally on port `8000`.

FastAPI automatically provides interactive Swagger documentation at:

```text
http://127.0.0.1:8000/docs
```

### 6. Start the Frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Vite will start the React development server.

Open the address displayed in the terminal, typically:

```text
http://localhost:5173
```

## 📌 Current Status

The core application workflow is functional.

Currently implemented:

- PDF upload
- PDF text extraction
- Generic text chunking
- Semantic embedding generation
- FAISS vector indexing
- Semantic document retrieval
- RAG-based question answering
- Gemini integration
- Conversation history
- Follow-up question support
- Chat reset
- API error handling
- Loading states
- React chat interface

## 🗺️ Planned Improvements

Future development will focus on:

- PostgreSQL database integration
- Persistent conversations and messages
- Persistent document metadata
- Multiple document support
- User authentication
- Document management
- Source references for generated answers
- Improved retrieval and chunking strategies
- Dockerized development environment
- Application deployment

## 👩‍💻 Author

**Nejra Gutić**

Computer Engineering graduate interested in software engineering, artificial intelligence, NLP, and full-stack development.