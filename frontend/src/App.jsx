import { useState } from "react";
import "./App.css";

function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [file, setFile] = useState(null);
  const [uploadMessage, setUploadMessage] = useState("");

  const handleUpload = async () => {
    if (!file) {
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

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
    } catch (error) {
      console.error(error);
      setUploadMessage("Upload failed.");
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!question.trim()) {
      return;
    }

    setLoading(true);
    setAnswer("");

    try {
      const response = await fetch("http://127.0.0.1:8000/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: question,
        }),
      });

      const data = await response.json();

      setAnswer(data.answer);
    } catch (error) {
      console.error(error);
      setAnswer("Something went wrong.");
    } finally {
      setLoading(false);
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

        <div className="upload-section">
          <input
            type="file"
            accept="application/pdf"
            onChange={(event) => setFile(event.target.files[0])}
          />

          <button
            type="button"
            onClick={handleUpload}
            disabled={!file}
          >
            Upload PDF
          </button>

          {uploadMessage && (
            <p>{uploadMessage}</p>
          )}
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

        {answer && (
          <div className="answer-card">
            <span className="answer-label">Answer</span>
            <p>{answer}</p>
          </div>
        )}
      </div>
    </main>
  );
}

export default App;