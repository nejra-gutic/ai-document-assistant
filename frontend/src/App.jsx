import { useEffect, useRef, useState } from "react";
import "./App.css";

function App() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [file, setFile] = useState(null);
  const [uploadMessage, setUploadMessage] = useState("");
  const [uploading, setUploading] = useState(false);
  const [currentDocument, setCurrentDocument] = useState(null);
  const messagesEndRef = useRef(null);
  const [conversationId, setConversationId] = useState(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  const handleUpload = async () => {
    if (!file) {
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    setUploading(true);
    setUploadMessage("");

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/api/documents/upload",
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      setUploadMessage(
        `${data.filename} uploaded successfully.`
      );

      setCurrentDocument(data.filename);
      setMessages([]);

    } catch (error) {
      console.error(error);
      setUploadMessage("Upload failed.");
    }finally {
      setUploading(false);
    }
  };

const createConversation = async () => {
  const response = await fetch(
    "http://127.0.0.1:8000/api/conversations",
    {
      method: "POST",
    }
  );

  const data = await response.json();

  setConversationId(data.id);

  return data.id;
};


  const handleSubmit = async (event) => {
  event.preventDefault();

  if (!question.trim()) {
    return;
  }

  const currentQuestion = question;

  setMessages((previousMessages) => [
    ...previousMessages,
    {
      role: "user",
      content: currentQuestion,
    },
  ]);

  setQuestion("");
  setLoading(true);

  try {

    let id = conversationId;

    if (!id) {
      id = await createConversation();
    }

    const response = await fetch(
      "http://127.0.0.1:8000/api/chat",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          conversation_id: id,
          question: currentQuestion,
        }),
      }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Something went wrong.");
    }

    setMessages((previousMessages) => [
      ...previousMessages,
      {
        role: "assistant",
        content: data.answer,
      },
    ]);
  } catch (error) {
    console.error(error);

    setMessages((previousMessages) => [
      ...previousMessages,
      {
        role: "assistant",
        content: error.message,
      },
    ]);
  } finally {
    setLoading(false);
  }
};

const handleNewChat = async () => {
  try {
    await fetch(
      "http://127.0.0.1:8000/api/chat/reset",
      {
        method: "POST",
      }
    );

    setMessages([]);
    setQuestion("");
    setConversationId(null);
  } catch (error) {
    console.error(error);
  }
};

  return (
    <main className="app">
      <div className="chat-card">
        <div className="header">
          <h1>AI Document Assistant</h1>
          <p>
            Ask questions about your document and get answers based on its
            content.
          </p>
        </div>

        <div className="document-bar">
          {currentDocument && (
            <div className="current-document">
              <span>Current document: </span>
              <strong>{currentDocument}</strong>
            </div>
          )}

          <button
            type="button"
            onClick={handleNewChat}
          >
            New chat
          </button>
        </div>

        <div className="upload-section">
          <div className="file-row">
            <label className="file-picker">
              <span>Choose PDF</span>

              <input
                type="file"
                accept="application/pdf"
                onChange={(event) => setFile(event.target.files[0])}
              />
            </label>

            {file && (
              <span className="selected-file">
                {file.name}
              </span>
            )}
          </div>

          <button
            type="button"
            onClick={handleUpload}
            disabled={!file || uploading}
          >
            {uploading ? "Processing document..." : "Upload PDF"}
          </button>

          {uploadMessage && (
            <p>{uploadMessage}</p>
          )}
        </div>


        <div className="messages">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`message ${message.role}`}
            >
              <span className="message-label">
                {message.role === "user" ? "You" : "Assistant"}
              </span>

              <p>{message.content}</p>
            </div>
          ))}

          {loading && (
            <div className="message assistant">
              <span className="message-label">
                Assistant
              </span>

              <p>Thinking...</p>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        <form className="question-form" onSubmit={handleSubmit}>
          <textarea
            value={question}
            onChange={(event) => setQuestion(event.target.value)}
            placeholder="Ask a question about the document..."
            rows="3"
          />

          <button
            type="submit"
            disabled={loading || !question.trim()}
          >
            {loading ? "Thinking..." : "Ask"}
          </button>
        </form>
      </div>
    </main>
  );
}

export default App;