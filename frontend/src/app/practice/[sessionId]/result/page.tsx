"use client";

import { useEffect, useState, use } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { fetchSession, type SessionData } from "@/lib/api-client";

function ScoreCircle({ score }: { score: number }) {
  const color =
    score >= 80
      ? "text-green-600"
      : score >= 60
        ? "text-yellow-600"
        : "text-red-600";
  const bgColor =
    score >= 80
      ? "bg-green-50 border-green-200"
      : score >= 60
        ? "bg-yellow-50 border-yellow-200"
        : "bg-red-50 border-red-200";

  return (
    <div
      className={`w-32 h-32 rounded-full ${bgColor} border-4 flex flex-col items-center justify-center`}
    >
      <span className={`text-4xl font-bold ${color}`}>{score}</span>
      <span className="text-xs text-gray-500 mt-1">/ 100</span>
    </div>
  );
}

export default function ResultPage({
  params,
}: {
  params: Promise<{ sessionId: string }>;
}) {
  const { sessionId } = use(params);
  const router = useRouter();
  const [session, setSession] = useState<SessionData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchSession(Number(sessionId))
      .then(setSession)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [sessionId]);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="text-gray-500">結果を読み込み中...</div>
      </div>
    );
  }

  if (!session) {
    return (
      <div className="text-center py-20">
        <p className="text-red-500 mb-4">セッションが見つかりません</p>
        <Link href="/" className="text-blue-600 hover:underline">
          ホームに戻る
        </Link>
      </div>
    );
  }

  // Parse feedback_summary to extract strengths and improvements
  const feedbackLines = (session.feedback_summary || "").split("\n");
  const summaryLines: string[] = [];
  const strengths: string[] = [];
  const improvements: string[] = [];
  let currentSection = "summary";

  for (const line of feedbackLines) {
    if (line.includes("良かった点")) {
      currentSection = "strengths";
      continue;
    }
    if (line.includes("改善点")) {
      currentSection = "improvements";
      continue;
    }
    const cleaned = line.replace(/^・/, "").trim();
    if (!cleaned) continue;

    if (currentSection === "summary") summaryLines.push(cleaned);
    else if (currentSection === "strengths") strengths.push(cleaned);
    else improvements.push(cleaned);
  }

  return (
    <div className="max-w-2xl mx-auto">
      <div className="text-center mb-8">
        <span className="text-4xl">{session.scenario.icon}</span>
        <h1 className="text-2xl font-bold text-gray-900 mt-2">
          練習結果
        </h1>
        <p className="text-gray-500 mt-1">{session.scenario.title_ja}</p>
      </div>

      {/* Score */}
      <div className="flex justify-center mb-8">
        <ScoreCircle score={session.score || 0} />
      </div>

      {/* Summary */}
      {summaryLines.length > 0 && (
        <div className="bg-white rounded-xl border border-gray-200 p-6 mb-4">
          <h2 className="font-semibold text-gray-900 mb-2">総合評価</h2>
          <p className="text-gray-700 text-sm leading-relaxed">
            {summaryLines.join(" ")}
          </p>
        </div>
      )}

      {/* Strengths */}
      {strengths.length > 0 && (
        <div className="bg-green-50 rounded-xl border border-green-200 p-6 mb-4">
          <h2 className="font-semibold text-green-800 mb-3">良かった点</h2>
          <ul className="space-y-2">
            {strengths.map((s, i) => (
              <li key={i} className="flex items-start gap-2 text-sm text-green-700">
                <span className="mt-0.5">&#10003;</span>
                <span>{s}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Improvements */}
      {improvements.length > 0 && (
        <div className="bg-amber-50 rounded-xl border border-amber-200 p-6 mb-4">
          <h2 className="font-semibold text-amber-800 mb-3">改善すべき点</h2>
          <ul className="space-y-2">
            {improvements.map((s, i) => (
              <li key={i} className="flex items-start gap-2 text-sm text-amber-700">
                <span className="mt-0.5">&#9679;</span>
                <span>{s}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Stats */}
      <div className="bg-white rounded-xl border border-gray-200 p-6 mb-8">
        <h2 className="font-semibold text-gray-900 mb-3">セッション情報</h2>
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div>
            <span className="text-gray-500">ターン数</span>
            <p className="font-medium text-gray-900">{session.total_turns}</p>
          </div>
          <div>
            <span className="text-gray-500">難易度</span>
            <p className="font-medium text-gray-900">
              {session.scenario.title}
            </p>
          </div>
        </div>
      </div>

      {/* Actions */}
      <div className="flex gap-3 justify-center">
        <Link
          href="/"
          className="px-6 py-3 bg-white border border-gray-300 text-gray-700 rounded-lg font-medium hover:bg-gray-50 transition-colors"
        >
          シナリオ選択に戻る
        </Link>
        <button
          onClick={() => router.push("/")}
          className="px-6 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors"
        >
          別のシナリオで練習する
        </button>
      </div>
    </div>
  );
}
