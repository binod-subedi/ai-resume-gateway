import { useState, useEffect, useRef } from "react";
import {
  Sparkles,
  User,
  SendHorizonal,
  Bot,
  Briefcase,
  AlertCircle
} from "lucide-react";

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { role: "user", content: input };
    const emptyAiMessage = { role: "ai", content: "" };

    setMessages((prev) => [...prev, userMessage, emptyAiMessage]);
    setInput("");

    try {
      const response = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: input }),
      });

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });

        setMessages((prev) => {
          const updated = [...prev];
          updated[updated.length - 1] = {
            ...updated[updated.length - 1],
            content: updated[updated.length - 1].content + chunk,
          };
          return updated;
        });
      }
    } catch (err) {
      console.error(err);
      setMessages((prev) => [
        ...prev,
        {
          role: "ai",
          content: "Could not connect to the backend server. Please check your connection.",
          isError: true
        },
      ]);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-[#111214] text-[#ececf1] font-sans antialiased">
      <header className="fixed top-4 left-0 right-0 z-50 flex justify-center pointer-events-none">
        <div className="flex items-center space-x-2 bg-[#17181c]/80 backdrop-blur-md border border-[#2d2f36] px-4 py-2 rounded-full shadow-xl pointer-events-auto">
          <Briefcase size={14} className="text-indigo-400" strokeWidth={2.5} />
          <h1 className="text-xs font-semibold tracking-wide text-white select-none">
            AI Recruiter
          </h1>
        </div>
      </header>

      {/* Main Chat Stream Container */}
      <main className="flex-1 overflow-y-auto px-4 py-8">
        <div className="max-w-3xl mx-auto space-y-6">
          {messages.length === 0 ? (
            /* Claude/ChatGPT Inspired Minimal Blank Slate */
            <div className="flex flex-col items-center justify-center h-[50vh] text-center space-y-4">
              <div className="w-12 h-12 rounded-2xl bg-[#1d1f24] border border-[#2d2f36] flex items-center justify-center text-indigo-400">
                <Sparkles size={24} />
              </div>
              <h3 className="text-xl font-medium text-white tracking-tight">How can I assist your hiring pipeline today?</h3>
              <p className="text-sm text-slate-400 max-w-sm leading-relaxed">
                Analyze candidate tech stacks, rewrite job specs, or build screen rubrics instantly.
              </p>
            </div>
          ) : (
            messages.map((msg, index) => {
              const isUser = msg.role === "user";
              return (
                <div
                  key={index}
                  className={`flex items-start space-x-4 max-w-3xl animate-fade-in ${isUser ? "ml-auto flex-row-reverse space-x-reverse" : "mr-auto"
                    }`}
                >
                  {/* Dynamic Lucide Avatar */}
                  <div
                    className={`flex-shrink-0 flex items-center justify-center w-8 h-8 rounded-lg text-sm border transition shadow-sm ${isUser
                      ? "bg-[#2d2f36] border-[#3e424b] text-slate-200"
                      : msg.isError
                        ? "bg-rose-950/40 border-rose-800/30 text-rose-400"
                        : "bg-indigo-600/10 border-indigo-500/20 text-indigo-400"
                      }`}
                  >
                    {isUser ? <User size={15} /> : msg.isError ? <AlertCircle size={15} /> : <Bot size={15} />}
                  </div>

                  {/* Bubble styling optimized for ultra-dark themes */}
                  <div
                    className={`px-4 py-3 rounded-xl text-[14px] leading-relaxed max-w-xl transition-all duration-150 ${isUser
                      ? "bg-[#202227] text-slate-100 border border-[#2d2f36]"
                      : msg.isError
                        ? "bg-rose-950/20 text-rose-300/90 border border-rose-900/30"
                        : "text-slate-200 md:px-1 bg-transparent border-none shadow-none"
                      /* Flat left-aligned transparent style for AI response (like Claude) */
                      }`}
                  >
                    {msg.content ? (
                      <p className="whitespace-pre-wrap">{msg.content}</p>
                    ) : (
                      /* ChatGPT Style Streaming Block Cursor */
                      <span className="inline-block w-1.5 h-4 bg-indigo-400 animate-pulse rounded-sm align-middle ml-1" />
                    )}
                  </div>
                </div>
              );
            })
          )}
          <div ref={messagesEndRef} />
        </div>
      </main>

      {/* Persistent Docked Input Bar */}
      <footer className="bg-gradient-to-t from-[#111214] via-[#111214] to-transparent px-4 pb-6 pt-2">
        <div className="max-w-3xl mx-auto">
          <div className="relative flex items-center bg-[#17181c] border border-[#2d2f36] focus-within:border-indigo-500/80 rounded-xl transition duration-200 shadow-xl">
            <input
              type="text"
              value={input}
              placeholder="Ask about candidates, screen profiles, review CVs..."
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && sendMessage()}
              className="w-full bg-transparent py-4 pl-5 pr-14 text-sm text-[#ececf1] placeholder-slate-500 focus:outline-none"
            />
            <button
              onClick={sendMessage}
              disabled={!input.trim()}
              className={`absolute right-2.5 p-1.5 rounded-lg transition-all duration-200 ${input.trim()
                ? "bg-indigo-600 text-white hover:bg-indigo-500 scale-100 shadow-md"
                : "bg-transparent text-slate-600 cursor-not-allowed scale-95"
                }`}
            >
              <SendHorizonal size={16} strokeWidth={2.5} />
            </button>
          </div>
          <p className="text-center text-[11px] text-slate-500 mt-3 tracking-wide">
            Powered by AI Recruiter Engine. Review key credentials independently.
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;