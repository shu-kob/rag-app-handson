import logoDark from "./logo-dark.svg";
import logoLight from "./logo-light.svg";

export function Welcome() {
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
            />
          </div>
          <div>
            <button
              type="button"
              style={{
                border: "1px solid #ccc",
                padding: "0.5rem 1rem",
              }}
            >
              送信
            </button>
          </div>
        </div>
      </div>
    </main>
  );
}
