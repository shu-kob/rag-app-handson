import { useState } from "react";

export function Welcome() {
  const [input, setInput] = useState("");

  const onSend = () => {
    fetch("http://localhost:8000/api/llm", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query: input }),
    })
  }

  return (
    <main className="flex items-center justify-center pt-16 pb-4">
      <div className="flex-1 flex flex-col items-center gap-16 min-h-0">
        <div>
          <div>
            <label htmlFor="message">メッセージ</label>
          </div>
          <div>
            <textarea
              id="message"
              rows={4}
              cols={50}
              style={{
                padding: "0.5rem",
                border: "1px solid #ccc",
                outline: "none",
                boxShadow: "none",
              }}
              value={input}
              onChange={(e) => setInput(e.target.value)}
            />
          </div>
          <div>
            <button
              type="button"
              style={{
                border: "1px solid #ccc",
                padding: "0.5rem 1rem",
              }}
              onClick={onSend}
            >
              送信
            </button>
          </div>
        </div>
      </div>
    </main>
  );
}
