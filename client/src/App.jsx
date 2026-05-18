import { useEffect, useRef, useState } from "react";

const initialMessages = [
  {
    id: "welcome",
    role: "assistant",
    text: "Hi Bhargav. Press Start Voice Mode, then say 'Lilly' to activate me.",
  },
];

const SpeechRecognition =
  window.SpeechRecognition || window.webkitSpeechRecognition;
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "";

export default function App() {
  const [messages, setMessages] = useState(initialMessages);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [voiceEnabled, setVoiceEnabled] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [awaitingCommand, setAwaitingCommand] = useState(false);
  const [status, setStatus] = useState("Voice mode off");
  const messagesEndRef = useRef(null);
  const recognitionRef = useRef(null);
  const preferredVoiceRef = useRef(null);
  const voiceEnabledRef = useRef(false);
  const awaitingCommandRef = useRef(false);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  useEffect(() => {
    voiceEnabledRef.current = voiceEnabled;
  }, [voiceEnabled]);

  useEffect(() => {
    awaitingCommandRef.current = awaitingCommand;
  }, [awaitingCommand]);

  useEffect(() => {
    if (!("speechSynthesis" in window)) return;

    const chooseVoice = () => {
      const voices = speechSynthesis.getVoices();
      preferredVoiceRef.current =
        voices.find((voice) =>
          /female|zira|samantha|victoria|karen|moira|tessa|veena/i.test(voice.name),
        ) ||
        voices.find((voice) => voice.lang === "en-IN") ||
        voices.find((voice) => voice.lang.startsWith("en-")) ||
        null;
    };

    chooseVoice();
    speechSynthesis.onvoiceschanged = chooseVoice;
  }, []);

  useEffect(() => {
    if (!SpeechRecognition) return;

    const recognition = new SpeechRecognition();
    recognition.lang = "en-IN";
    recognition.interimResults = false;
    recognition.continuous = false;

    recognition.onstart = () => setIsListening(true);
    recognition.onend = () => {
      setIsListening(false);
      if (voiceEnabledRef.current && !speechSynthesis.speaking) {
        window.setTimeout(() => {
          try {
            recognition.start();
          } catch {
            // Browser may still be settling from the previous session.
          }
        }, 350);
      }
    };
    recognition.onerror = () => {
      setStatus("Listening paused. Try again.");
    };
    recognition.onresult = async (event) => {
      const transcript = event.results[0][0].transcript.trim();
      const lower = transcript.toLowerCase();

      if (!awaitingCommandRef.current) {
        setStatus(`Heard: ${transcript}`);

        if (lower.includes("lilly") || lower.includes("lily")) {
          setAwaitingCommand(true);
          awaitingCommandRef.current = true;
          setStatus("Lilly activated. Waiting for command...");
          speak("Yes Bhargav?");
        }
        return;
      }

      setAwaitingCommand(false);
      awaitingCommandRef.current = false;
      setStatus(`Command: ${transcript}`);
      await sendTextMessage(transcript);
    };

    recognitionRef.current = recognition;

    return () => recognition.abort();
  }, []);

  function speak(text, onEnd) {
    if (!("speechSynthesis" in window)) return;

    recognitionRef.current?.abort();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1;
    utterance.pitch = 1.15;
    if (preferredVoiceRef.current) {
      utterance.voice = preferredVoiceRef.current;
    }
    utterance.onend = () => {
      onEnd?.();
      if (voiceEnabledRef.current) {
        window.setTimeout(() => {
          try {
            recognitionRef.current?.start();
          } catch {
            // Ignore duplicate starts.
          }
        }, 250);
      }
    };
    speechSynthesis.cancel();
    speechSynthesis.speak(utterance);
  }

  async function sendTextMessage(text) {
    const trimmed = text.trim();
    if (!trimmed || isLoading) return;

    const userMessage = {
      id: crypto.randomUUID(),
      role: "user",
      text: trimmed,
    };

    setMessages((current) => [...current, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: trimmed }),
      });
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Request failed");
      }

      setMessages((current) => [
        ...current,
        { id: crypto.randomUUID(), role: "assistant", text: data.reply },
      ]);
      if (data.action?.type === "open_url" && data.action.url) {
        window.open(data.action.url, "lilly-music");
      }
      speak(data.reply, () => {
        if (trimmed.toLowerCase().includes("goodbye") || trimmed.toLowerCase().includes("bye")) {
          stopVoiceMode();
        } else {
          setStatus("Listening for wake word...");
        }
      });
    } catch (error) {
      const reply = `Signal lost: ${error.message}`;
      setMessages((current) => [
        ...current,
        { id: crypto.randomUUID(), role: "assistant", text: reply },
      ]);
      speak(reply);
    } finally {
      setIsLoading(false);
    }
  }

  async function sendMessage(event) {
    event.preventDefault();
    await sendTextMessage(input);
  }

  function startVoiceMode() {
    if (!SpeechRecognition) {
      setStatus("This browser does not support speech recognition.");
      return;
    }

    setVoiceEnabled(true);
    voiceEnabledRef.current = true;
    setStatus("Listening for wake word...");
    speak("Hi Bhargav. Say Lilly to activate me.");
  }

  function stopVoiceMode() {
    setVoiceEnabled(false);
    voiceEnabledRef.current = false;
    setAwaitingCommand(false);
    awaitingCommandRef.current = false;
    setStatus("Voice mode off");
    recognitionRef.current?.abort();
  }

  return (
    <main className="app-shell">
      <section className="agent-panel">
        <div className="scanlines" />
        <div className="avatar-wrap" aria-hidden="true">
          <div className="orbit orbit-one">
            <span />
          </div>
          <div className="orbit orbit-two">
            <span />
          </div>
          <div className="orbit orbit-three">
            <span />
          </div>
          <div className={`core-orb ${isListening ? "listening" : ""}`} />
        </div>
        <h1>LILLY</h1>
        <p>AI VOICE ASSISTANT</p>
        <div className="voice-controls">
          {!voiceEnabled ? (
            <button onClick={startVoiceMode}>Start Voice Mode</button>
          ) : (
            <button onClick={stopVoiceMode}>Stop Voice Mode</button>
          )}
        </div>
      </section>

      <section className="chat-panel">
        <header className="chat-header">
          <span className={`status-dot ${isListening ? "active" : ""}`} />
          <div>
            <h2>Lilly Console</h2>
            <p>{status}</p>
          </div>
        </header>

        <div className="messages">
          {messages.map((message) => (
            <article
              key={message.id}
              className={`message ${message.role === "user" ? "user" : "assistant"}`}
            >
              {message.text}
            </article>
          ))}

          {isLoading && (
            <article className="message assistant loading" aria-label="Lilly is typing">
              <span />
              <span />
              <span />
            </article>
          )}

          <div ref={messagesEndRef} />
        </div>

        <form className="composer" onSubmit={sendMessage}>
          <input
            value={input}
            onChange={(event) => setInput(event.target.value)}
            placeholder="Speak or type to Lilly..."
            aria-label="Message Lilly"
          />
          <button type="submit" disabled={!input.trim() || isLoading}>
            Send
          </button>
        </form>
      </section>
    </main>
  );
}
