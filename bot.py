import { useState, useRef, useEffect } from "react";

const SYSTEM_PROMPT = `Ту психологи профессионалӣ ҳастӣ, ки дар Маркази психологии Мотив кор мекунӣ. Номат Мотив аст.
Равиши кориат дар асоси гештальт-терапия ва психологияи гуманистӣ аст: "ҳозир ва инҷо", тамоси эмотсионалӣ, саволҳои кушода.

Қоидаҳои муошират:
- БА ЗАБОНИ ТОҶИКӢ сухбат кун
- Ба кӯдакон ва наврасон бо забони содда ва гарм гап зан
- Аввал эҳсоси инсонро пурсон шав, на мушкилашро
- Ҳеҷ гоҳ маслиҳат надеҳ, агар напурсанд
- Саволи якто бипурс, на якчанд
- Ҷавобҳоят кӯтоҳ бошанд (2-4 ҷумла)
- Истилоҳоти техникии психологӣ истифода набар
- Агар хатар ба ҷон дар миён бошад, ба мутахассис муроҷиат карданро тавсия деҳ

Ибтидои сессия: худатро муаррифӣ кун ва бипурс имрӯз чӣ ба дилашон дорад.`;

const WELCOME = {
  role: "assistant",
  content: "Салом! Ман Мотив ҳастам — психологи рақамии Маркази психологии Мотив. 🌱\n\nДар ин ҷо метавонӣ озодона ҳарф занӣ — ҳама чиз байни мо мемонад.\n\nИмрӯз чӣ ба дилат дорӣ?"
};

const TypingDots = () => (
  <div style={{ display: "flex", gap: "5px", padding: "4px 0", alignItems: "center" }}>
    {[0,1,2].map(i => (
      <div key={i} style={{
        width: 8, height: 8, borderRadius: "50%",
        background: "#6BAF92",
        animation: "bounce 1.2s infinite",
        animationDelay: `${i * 0.2}s`
      }} />
    ))}
  </div>
);

export default function PsyMotivBot() {
  const [messages, setMessages] = useState([WELCOME]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [sessionStart] = useState(new Date());
  const bottomRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const formatTime = (date) => date.toLocaleTimeString("tg-TJ", { hour: "2-digit", minute: "2-digit" });

  const sendMessage = async () => {
    const text = input.trim();
    if (!text || loading) return;

    const userMsg = { role: "user", content: text };
    const newMessages = [...messages, userMsg];
    setMessages(newMessages);
    setInput("");
    setLoading(true);

    try {
      const apiMessages = newMessages.map(m => ({ role: m.role, content: m.content }));

      const response = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          model: "claude-sonnet-4-20250514",
          max_tokens: 1000,
          system: SYSTEM_PROMPT,
          messages: apiMessages
        })
      });

      const data = await response.json();
      const reply = data.content?.[0]?.text || "Бубахш, хато рӯй дод. Лутфан дубора кӯшиш кун.";
      setMessages(prev => [...prev, { role: "assistant", content: reply }]);
    } catch {
      setMessages(prev => [...prev, { role: "assistant", content: "Пайвастшавӣ қатъ шуд. Лутфан дубора кӯшиш кун." }]);
    } finally {
      setLoading(false);
      setTimeout(() => inputRef.current?.focus(), 100);
    }
  };

  const handleKey = (e) => {
    if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); sendMessage(); }
  };

  const resetChat = () => {
    setMessages([WELCOME]);
    setInput("");
  };

  return (
    <div style={{
      minHeight: "100vh",
      background: "linear-gradient(135deg, #E8F5EE 0%, #F0EBF8 50%, #EBF3F8 100%)",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      fontFamily: "'Georgia', 'Times New Roman', serif",
      padding: "16px"
    }}>
      <style>{`
        @keyframes bounce {
          0%, 60%, 100% { transform: translateY(0); }
          30% { transform: translateY(-6px); }
        }
        @keyframes fadeUp {
          from { opacity: 0; transform: translateY(12px); }
          to { opacity: 1; transform: translateY(0); }
        }
        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.6; }
        }
        .msg-bubble { animation: fadeUp 0.3s ease forwards; }
        textarea:focus { outline: none; }
        textarea { resize: none; }
        ::-webkit-scrollbar { width: 4px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: #C5DDD2; border-radius: 4px; }
        .send-btn:hover { background: #4A9470 !important; transform: scale(1.05); }
        .send-btn:active { transform: scale(0.97); }
        .reset-btn:hover { background: #e8e0f0 !important; }
        .quick-btn:hover { background: #d4eadf !important; border-color: #6BAF92 !important; }
      `}</style>

      <div style={{
        width: "100%", maxWidth: 440,
        background: "white",
        borderRadius: 24,
        boxShadow: "0 20px 60px rgba(107,175,146,0.15), 0 4px 20px rgba(0,0,0,0.08)",
        overflow: "hidden",
        display: "flex",
        flexDirection: "column",
        height: "calc(100vh - 32px)",
        maxHeight: 720
      }}>

        {/* Header */}
        <div style={{
          background: "linear-gradient(135deg, #2D7A56 0%, #1A5C3E 100%)",
          padding: "20px 20px 16px",
          position: "relative",
          overflow: "hidden"
        }}>
          <div style={{
            position: "absolute", top: -20, right: -20,
            width: 100, height: 100,
            background: "rgba(255,255,255,0.05)",
            borderRadius: "50%"
          }} />
          <div style={{
            position: "absolute", bottom: -30, left: -10,
            width: 80, height: 80,
            background: "rgba(255,255,255,0.04)",
            borderRadius: "50%"
          }} />
          <div style={{ display: "flex", alignItems: "center", gap: 14, position: "relative" }}>
            <div style={{
              width: 52, height: 52,
              background: "rgba(255,255,255,0.15)",
              borderRadius: "50%",
              display: "flex", alignItems: "center", justifyContent: "center",
              fontSize: 26,
              border: "2px solid rgba(255,255,255,0.25)"
            }}>🧠</div>
            <div>
              <div style={{ color: "white", fontWeight: 700, fontSize: 18, letterSpacing: 0.3 }}>Мотив</div>
              <div style={{ color: "rgba(255,255,255,0.75)", fontSize: 12, marginTop: 2 }}>
                Маркази психологии Мотив
              </div>
              <div style={{ display: "flex", alignItems: "center", gap: 5, marginTop: 4 }}>
                <div style={{
                  width: 7, height: 7, borderRadius: "50%",
                  background: "#7FFFB0",
                  animation: "pulse 2s infinite"
                }} />
                <span style={{ color: "rgba(255,255,255,0.65)", fontSize: 11 }}>Онлайн</span>
              </div>
            </div>
            <button onClick={resetChat} className="reset-btn" style={{
              marginLeft: "auto",
              background: "rgba(255,255,255,0.12)",
              border: "1px solid rgba(255,255,255,0.2)",
              borderRadius: 10,
              color: "rgba(255,255,255,0.8)",
              fontSize: 11,
              padding: "5px 10px",
              cursor: "pointer",
              transition: "background 0.2s"
            }}>↺ Нав</button>
          </div>
          <div style={{
            marginTop: 12,
            background: "rgba(255,255,255,0.08)",
            borderRadius: 10,
            padding: "7px 12px",
            color: "rgba(255,255,255,0.7)",
            fontSize: 11,
            display: "flex", alignItems: "center", gap: 6
          }}>
            🔒 Сӯҳбати шумо маҳфуз аст
          </div>
        </div>

        {/* Messages */}
        <div style={{
          flex: 1,
          overflowY: "auto",
          padding: "20px 16px 8px",
          display: "flex",
          flexDirection: "column",
          gap: 12
        }}>
          {/* Session info */}
          <div style={{
            textAlign: "center",
            color: "#B0B8C0",
            fontSize: 11,
            padding: "4px 12px",
            background: "#F7F9FA",
            borderRadius: 20,
            alignSelf: "center"
          }}>
            Сессия оғоз шуд · {formatTime(sessionStart)}
          </div>

          {messages.map((msg, i) => (
            <div key={i} className="msg-bubble" style={{
              display: "flex",
              flexDirection: msg.role === "user" ? "row-reverse" : "row",
              alignItems: "flex-end",
              gap: 8
            }}>
              {msg.role === "assistant" && (
                <div style={{
                  width: 32, height: 32,
                  background: "linear-gradient(135deg, #2D7A56, #1A5C3E)",
                  borderRadius: "50%",
                  display: "flex", alignItems: "center", justifyContent: "center",
                  fontSize: 15, flexShrink: 0
                }}>🧠</div>
              )}
              <div style={{
                maxWidth: "78%",
                background: msg.role === "user"
                  ? "linear-gradient(135deg, #2D7A56, #1A5C3E)"
                  : "#F2F7F4",
                color: msg.role === "user" ? "white" : "#2A3C33",
                borderRadius: msg.role === "user" ? "18px 4px 18px 18px" : "4px 18px 18px 18px",
                padding: "12px 15px",
                fontSize: 14.5,
                lineHeight: 1.6,
                whiteSpace: "pre-wrap",
                boxShadow: msg.role === "user"
                  ? "0 3px 12px rgba(45,122,86,0.25)"
                  : "0 2px 8px rgba(0,0,0,0.06)"
              }}>
                {msg.content}
              </div>
            </div>
          ))}

          {loading && (
            <div className="msg-bubble" style={{ display: "flex", alignItems: "flex-end", gap: 8 }}>
              <div style={{
                width: 32, height: 32,
                background: "linear-gradient(135deg, #2D7A56, #1A5C3E)",
                borderRadius: "50%",
                display: "flex", alignItems: "center", justifyContent: "center",
                fontSize: 15
              }}>🧠</div>
              <div style={{
                background: "#F2F7F4",
                borderRadius: "4px 18px 18px 18px",
                padding: "12px 16px",
                boxShadow: "0 2px 8px rgba(0,0,0,0.06)"
              }}>
                <TypingDots />
              </div>
            </div>
          )}
          <div ref={bottomRef} />
        </div>

        {/* Quick replies - show only at start */}
        {messages.length <= 2 && !loading && (
          <div style={{ padding: "0 16px 8px", display: "flex", gap: 8, flexWrap: "wrap" }}>
            {["😔 Ғам дорам", "😰 Изтироб дорам", "😤 Асаб дорам", "🤷 Намедонам..."].map(q => (
              <button key={q} className="quick-btn" onClick={() => { setInput(q); setTimeout(sendMessage, 0); }}
                style={{
                  background: "#F2F7F4", border: "1px solid #C5DDD2",
                  borderRadius: 20, padding: "6px 12px",
                  fontSize: 12.5, color: "#2D7A56",
                  cursor: "pointer", transition: "all 0.2s"
                }}>
                {q}
              </button>
            ))}
          </div>
        )}

        {/* Input */}
        <div style={{
          padding: "12px 16px 16px",
          borderTop: "1px solid #EBF3EF",
          background: "white"
        }}>
          <div style={{
            display: "flex", gap: 10, alignItems: "flex-end",
            background: "#F4F8F6",
            borderRadius: 16,
            padding: "8px 8px 8px 14px",
            border: "1.5px solid #D8EDE4",
            transition: "border-color 0.2s"
          }}>
            <textarea
              ref={inputRef}
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={handleKey}
              placeholder="Нависед..."
              rows={1}
              style={{
                flex: 1, border: "none", background: "transparent",
                fontSize: 14.5, color: "#2A3C33",
                lineHeight: 1.5, maxHeight: 100,
                fontFamily: "inherit", paddingTop: 2
              }}
              onInput={e => {
                e.target.style.height = "auto";
                e.target.style.height = e.target.scrollHeight + "px";
              }}
            />
            <button
              className="send-btn"
              onClick={sendMessage}
              disabled={loading || !input.trim()}
              style={{
                width: 40, height: 40,
                borderRadius: 12,
                background: loading || !input.trim() ? "#C5DDD2" : "#2D7A56",
                border: "none", cursor: loading || !input.trim() ? "default" : "pointer",
                display: "flex", alignItems: "center", justifyContent: "center",
                fontSize: 18, transition: "all 0.2s", flexShrink: 0
              }}>
              ➤
            </button>
          </div>
          <div style={{ textAlign: "center", color: "#C0CCC5", fontSize: 10.5, marginTop: 8 }}>
            Маркази психологии Мотив · AI-психолог
          </div>
        </div>
      </div>
    </div>
  );
}
