import { useState } from "react";
import axios from "axios";

const BACKEND_URL = "http://127.0.0.1:8000";


function App() {
  const [file, setFile] = useState(null);
  const [summary, setSummary] = useState("");
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const uploadPDF = async () => {
    if (!file) {
      alert("Please select a PDF file");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    try {
      const res = await axios.post(
        `${BACKEND_URL}/upload_pdf`,
        formData,
        { headers: { "Content-Type": "multipart/form-data" } }
      );
      setSummary(res.data.summary);
    } catch (err) {
      alert("PDF upload failed");
    }
    setLoading(false);
  };

  const askQuestion = async () => {
    if (!question) {
      alert("Enter a question");
      return;
    }

    setLoading(true);
    try {
      const res = await axios.get(
        `${BACKEND_URL}/rag_chat`,
        { params: { question } }
      );
      setAnswer(res.data.answer);
    } catch (err) {
      alert("RAG chat failed");
    }
    setLoading(false);
  };

  return (
    <div style={{ padding: "40px", fontFamily: "Arial" }}>
      <h1>AI Research Companion</h1>

      <h3>Upload PDF</h3>
      <input type="file" accept=".pdf" onChange={(e) => setFile(e.target.files[0])} />
      <br /><br />
      <button onClick={uploadPDF}>Analyze PDF</button>

      {loading && <p>Loading...</p>}

      {summary && (
        <>
          <h3>Summary</h3>
          <p>{summary}</p>
        </>
      )}

      <hr />

      <h3>Ask Question (RAG)</h3>
      <input
        type="text"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask something from the document"
        style={{ width: "300px" }}
      />
      <br /><br />
      <button onClick={askQuestion}>Ask</button>

      {answer && (
        <>
          <h3>Answer</h3>
          <p>{answer}</p>
        </>
      )}
    </div>
  );
}

export default App;
