"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { fetchSessions, type SessionListItem } from "@/lib/api-client";

const difficultyLabels: Record<string, { label: string; color: string }> = {
  beginner: { label: "初級", color: "bg-green-100 text-green-700" },
  intermediate: { label: "中級", color: "bg-yellow-100 text-yellow-700" },
  advanced: { label: "上級", color: "bg-red-100 text-red-700" },
};

function formatDate(dateStr: string | null): string {
  if (!dateStr) return "-";
  const date = new Date(dateStr);
  return date.toLocaleDateString("ja-JP", {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export default function HistoryPage() {
  const [sessions, setSessions] = useState<SessionListItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchSessions()
      .then(setSessions)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="text-gray-500">読み込み中...</div>
      </div>
    );
  }

  return (
    <div>
      <div className="text-center mb-8">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">練習履歴</h1>
        <p className="text-gray-600">過去の練習セッションを振り返りましょう</p>
      </div>

      {sessions.length === 0 ? (
        <div className="text-center py-16">
          <p className="text-gray-500 mb-4">
            まだ練習履歴がありません
          </p>
          <Link
            href="/"
            className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors"
          >
            練習を始める
          </Link>
        </div>
      ) : (
        <div className="space-y-3">
          {sessions.map((session) => {
            const diff = difficultyLabels[session.difficulty];
            return (
              <Link
                key={session.id}
                href={
                  session.status === "completed"
                    ? `/practice/${session.id}/result`
                    : `/practice/${session.id}`
                }
                className="block bg-white rounded-xl border border-gray-200 p-4 hover:shadow-md transition-shadow"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <span className="text-2xl">{session.scenario_icon}</span>
                    <div>
                      <h3 className="font-medium text-gray-900">
                        {session.scenario_title_ja}
                      </h3>
                      <p className="text-xs text-gray-500">
                        {formatDate(session.started_at)} /{" "}
                        {session.total_turns}ターン
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <span
                      className={`px-2 py-1 rounded-full text-xs font-medium ${diff?.color}`}
                    >
                      {diff?.label}
                    </span>
                    {session.score !== null ? (
                      <div className="text-right">
                        <span
                          className={`text-xl font-bold ${
                            session.score >= 80
                              ? "text-green-600"
                              : session.score >= 60
                                ? "text-yellow-600"
                                : "text-red-600"
                          }`}
                        >
                          {session.score}
                        </span>
                        <span className="text-xs text-gray-400">/100</span>
                      </div>
                    ) : (
                      <span className="text-xs text-gray-400 bg-gray-100 px-2 py-1 rounded">
                        {session.status === "active" ? "進行中" : "未評価"}
                      </span>
                    )}
                  </div>
                </div>
              </Link>
            );
          })}
        </div>
      )}
    </div>
  );
}
