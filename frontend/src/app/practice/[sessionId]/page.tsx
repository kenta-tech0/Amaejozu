"use client";

import { useEffect, useState, useRef, use } from "react";
import { useRouter } from "next/navigation";
import {
  fetchSession,
  sendMessage,
  endSession,
  type MessageData,
} from "@/lib/api-client";
import { useSpeechRecognition, speak } from "@/lib/speech";

export default function PracticePage({
  params,
}: {
  params: Promise<{ sessionId: string }>;
}) {
  const { sessionId } = use(params);
  const router = useRouter();
  const [messages, setMessages] = useState<MessageData[]>([]);
  const [scenarioTitle, setScenarioTitle] = useState("");
  const [scenarioIcon, setScenarioIcon] = useState("");
  const [sending, setSending] = useState(false);
  const [ending, setEnding] = useState(false);
  const [sessionStatus, setSessionStatus] = useState("active");
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const {
    isListening,
    transcript,
    startListening,
    stopListening,
    resetTranscript,
    isSupported,
  } = useSpeechRecognition();

  // Load session data
  useEffect(() => {
    fetchSession(Number(sessionId))
      .then((session) => {
        setMessages(session.messages);
        setScenarioTitle(session.scenario.title_ja);
        setScenarioIcon(session.scenario.icon);
        setSessionStatus(session.status);
        // Speak the last AI message
        const lastAi = session.messages
          .filter((m) => m.role === "assistant")
          .pop();
        if (lastAi) speak(lastAi.content);
      })
      .catch(() => setError("セッションの読み込みに失敗しました"));
  }, [sessionId]);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async () => {
    if (!transcript.trim() || sending) return;

    const userText = transcript.trim();
    stopListening();
    resetTranscript();
    setSending(true);
    setError(null);

    try {
      const result = await sendMessage(Number(sessionId), userText);
      setMessages((prev) => [
        ...prev,
        result.user_message,
        result.ai_message,
      ]);
      setSessionStatus(result.session_status);

      // Speak AI response
      await speak(result.ai_message.content);
    } catch {
      setError("メッセージの送信に失敗しました");
    } finally {
      setSending(false);
    }
  };

  const handleEnd = async () => {
    setEnding(true);
    try {
      await endSession(Number(sessionId));
      router.push(`/practice/${sessionId}/result`);
    } catch {
      setError("セッションの終了に失敗しました");
      setEnding(false);
    }
  };

  const handleMicToggle = () => {
    if (isListening) {
      stopListening();
    } else {
      resetTranscript();
      startListening();
    }
  };

  if (error && messages.length === 0) {
    return (
      <div className="text-center py-20">
        <p className="text-red-500 mb-4">{error}</p>
        <button
          onClick={() => router.push("/")}
          className="px-4 py-2 bg-gray-200 rounded-lg"
        >
          ホームに戻る
        </button>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-[calc(100vh-5rem)]">
      {/* Session header */}
      <div className="flex items-center justify-between bg-white rounded-xl border border-gray-200 px-4 py-3 mb-4">
        <div className="flex items-center gap-2">
          <span className="text-xl">{scenarioIcon}</span>
          <span className="font-medium text-gray-900">{scenarioTitle}</span>
        </div>
        <button
          onClick={handleEnd}
          disabled={ending || sessionStatus !== "active"}
          className="px-4 py-2 bg-red-50 text-red-600 text-sm font-medium rounded-lg hover:bg-red-100 disabled:opacity-50 transition-colors"
        >
          {ending ? "終了中..." : "練習を終了する"}
        </button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto space-y-4 pb-4">
        {messages.map((msg, i) => (
          <div key={i}>
            {/* Message bubble */}
            <div
              className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
            >
              <div
                className={`max-w-[80%] rounded-2xl px-4 py-3 ${
                  msg.role === "user"
                    ? "bg-blue-600 text-white"
                    : "bg-white border border-gray-200 text-gray-900"
                }`}
              >
                <p className="text-sm leading-relaxed">{msg.content}</p>
              </div>
            </div>

            {/* Feedback panel for user messages */}
            {msg.role === "user" && (msg.correction || msg.feedback) && (
              <div className="mt-2 ml-auto max-w-[80%]">
                <div className="bg-amber-50 border border-amber-200 rounded-xl px-4 py-3 text-sm">
                  {msg.correction && (
                    <div className="mb-2">
                      <span className="font-medium text-amber-800">
                        修正:
                      </span>
                      <p className="text-amber-700 mt-1">{msg.correction}</p>
                    </div>
                  )}
                  {msg.feedback && (
                    <div>
                      <span className="font-medium text-amber-800">
                        アドバイス:
                      </span>
                      <p className="text-amber-700 mt-1">{msg.feedback}</p>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        ))}

        {sending && (
          <div className="flex justify-start">
            <div className="bg-white border border-gray-200 rounded-2xl px-4 py-3">
              <div className="flex gap-1">
                <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
                <span
                  className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                  style={{ animationDelay: "0.1s" }}
                />
                <span
                  className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                  style={{ animationDelay: "0.2s" }}
                />
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input area */}
      {sessionStatus === "active" && (
        <div className="bg-white rounded-xl border border-gray-200 p-4">
          {error && (
            <p className="text-red-500 text-sm mb-2">{error}</p>
          )}

          {/* Transcript display */}
          {(transcript || isListening) && (
            <div className="mb-3 p-3 bg-gray-50 rounded-lg min-h-[3rem]">
              <p className="text-sm text-gray-700">
                {transcript || (
                  <span className="text-gray-400 italic">
                    話してください...
                  </span>
                )}
              </p>
            </div>
          )}

          <div className="flex items-center gap-3">
            {!isSupported ? (
              <p className="text-sm text-red-500 flex-1">
                お使いのブラウザは音声認識に対応していません。Chrome
                をお使いください。
              </p>
            ) : (
              <>
                {/* Mic button */}
                <button
                  onClick={handleMicToggle}
                  disabled={sending}
                  className={`relative w-14 h-14 rounded-full flex items-center justify-center transition-all ${
                    isListening
                      ? "bg-red-500 text-white shadow-lg"
                      : "bg-blue-600 text-white hover:bg-blue-700"
                  } disabled:opacity-50`}
                >
                  {isListening && (
                    <span className="absolute inset-0 rounded-full bg-red-400 animate-pulse-ring" />
                  )}
                  <svg
                    className="w-6 h-6 relative z-10"
                    fill="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3zm-1-9c0-.55.45-1 1-1s1 .45 1 1v6c0 .55-.45 1-1 1s-1-.45-1-1V5z" />
                    <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z" />
                  </svg>
                </button>

                <div className="flex-1 text-sm text-gray-500">
                  {isListening
                    ? "録音中... マイクボタンを押して停止"
                    : "マイクボタンを押して話してください"}
                </div>

                {/* Send button */}
                {transcript && !isListening && (
                  <button
                    onClick={handleSend}
                    disabled={sending}
                    className="px-5 py-2.5 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
                  >
                    送信
                  </button>
                )}
              </>
            )}
          </div>
        </div>
      )}

      {sessionStatus === "completed" && (
        <div className="bg-green-50 border border-green-200 rounded-xl p-4 text-center">
          <p className="text-green-700 font-medium">会話が完了しました</p>
          <button
            onClick={() => router.push(`/practice/${sessionId}/result`)}
            className="mt-2 px-4 py-2 bg-green-600 text-white rounded-lg text-sm hover:bg-green-700 transition-colors"
          >
            結果を見る
          </button>
        </div>
      )}
    </div>
  );
}
