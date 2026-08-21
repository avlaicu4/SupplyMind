import { useState } from "react";

function AiChat({ apiUrl }) {
  const [message, setMessage] = useState("What should I reorder this week?");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  function handleSubmit(event) {
    event.preventDefault();

    setLoading(true);
    setAnswer("");

    fetch(`${apiUrl}/ai/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to ask AI assistant");
        }

        return response.json();
      })
      .then((data) => {
        setAnswer(data.answer);
        setLoading(false);
      })
      .catch(() => {
        setAnswer("Could not get an answer from the AI assistant.");
        setLoading(false);
      });
  }

  return (
    <section className="ai-chat-panel">
      <div className="section-header">
        <h2>AI Assistant</h2>
        <span>Ollama agent</span>
      </div>

      <form className="ai-chat-form" onSubmit={handleSubmit}>
        <textarea
          value={message}
          onChange={(event) => setMessage(event.target.value)}
          rows="3"
        />

        <button type="submit" disabled={loading}>
          {loading ? "Thinking..." : "Ask AI"}
        </button>
      </form>

      {answer && (
        <div className="ai-answer">
          <strong>Answer</strong>
          <p>{answer}</p>
        </div>
      )}
    </section>
  );
}

export default AiChat;