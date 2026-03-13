"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { fetchScenarios, startSession, type Scenario } from "@/lib/api-client";

const difficultyLabels: Record<string, { label: string; color: string }> = {
  beginner: { label: "初級", color: "bg-green-100 text-green-700" },
  intermediate: { label: "中級", color: "bg-yellow-100 text-yellow-700" },
  advanced: { label: "上級", color: "bg-red-100 text-red-700" },
};

const categoryLabels: Record<string, string> = {
  daily: "日常",
  travel: "旅行",
  business: "ビジネス",
};

export default function Home() {
  const router = useRouter();
  const [scenarios, setScenarios] = useState<Scenario[]>([]);
  const [loading, setLoading] = useState(true);
  const [starting, setStarting] = useState<number | null>(null);
  const [filter, setFilter] = useState<string>("all");

  useEffect(() => {
    fetchScenarios()
      .then(setScenarios)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const handleStart = async (scenarioId: number) => {
    setStarting(scenarioId);
    try {
      const result = await startSession(scenarioId);
      router.push(`/practice/${result.session_id}`);
    } catch (error) {
      console.error("Failed to start session:", error);
      setStarting(null);
    }
  };

  const filtered =
    filter === "all"
      ? scenarios
      : scenarios.filter((s) => s.category === filter);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="text-gray-500 text-lg">読み込み中...</div>
      </div>
    );
  }

  return (
    <div>
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          英語スピーキング練習
        </h1>
        <p className="text-gray-600">
          シナリオを選んで、AIと英会話の練習をしましょう
        </p>
      </div>

      {/* Category filter */}
      <div className="flex justify-center gap-2 mb-8">
        {[
          { key: "all", label: "すべて" },
          { key: "daily", label: "日常" },
          { key: "travel", label: "旅行" },
          { key: "business", label: "ビジネス" },
        ].map((cat) => (
          <button
            key={cat.key}
            onClick={() => setFilter(cat.key)}
            className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
              filter === cat.key
                ? "bg-blue-600 text-white"
                : "bg-white text-gray-600 border border-gray-300 hover:bg-gray-50"
            }`}
          >
            {cat.label}
          </button>
        ))}
      </div>

      {/* Scenario cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filtered.map((scenario) => {
          const diff = difficultyLabels[scenario.difficulty];
          return (
            <div
              key={scenario.id}
              className="bg-white rounded-xl border border-gray-200 p-6 hover:shadow-lg transition-shadow"
            >
              <div className="flex items-start justify-between mb-3">
                <span className="text-3xl">{scenario.icon}</span>
                <span
                  className={`px-2 py-1 rounded-full text-xs font-medium ${diff?.color}`}
                >
                  {diff?.label}
                </span>
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-1">
                {scenario.title_ja}
              </h3>
              <p className="text-sm text-gray-500 mb-1">{scenario.title}</p>
              <p className="text-sm text-gray-600 mb-4">
                {scenario.description_ja}
              </p>
              <div className="flex items-center justify-between">
                <span className="text-xs text-gray-400">
                  {categoryLabels[scenario.category]} /{" "}
                  {scenario.estimated_turns}ターン
                </span>
                <button
                  onClick={() => handleStart(scenario.id)}
                  disabled={starting !== null}
                  className="px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  {starting === scenario.id ? "開始中..." : "練習する"}
                </button>
              </div>
            </div>
          );
        })}
      </div>

      {filtered.length === 0 && (
        <div className="text-center py-12 text-gray-500">
          該当するシナリオがありません
        </div>
      )}
    </div>
  );
}
