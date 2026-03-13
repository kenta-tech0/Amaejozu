const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface Scenario {
  id: number;
  title: string;
  title_ja: string;
  description: string;
  description_ja: string;
  difficulty: string;
  category: string;
  icon: string;
  estimated_turns: number;
  first_message?: string;
}

export interface MessageData {
  role: "user" | "assistant";
  content: string;
  correction?: string | null;
  feedback?: string | null;
  turn_number: number;
}

export interface SessionData {
  id: number;
  scenario: {
    id: number;
    title: string;
    title_ja: string;
    icon: string;
    estimated_turns: number;
  };
  status: string;
  total_turns: number;
  score: number | null;
  feedback_summary: string | null;
  started_at: string | null;
  ended_at: string | null;
  messages: MessageData[];
}

export interface SessionListItem {
  id: number;
  scenario_title: string;
  scenario_title_ja: string;
  scenario_icon: string;
  difficulty: string;
  started_at: string | null;
  ended_at: string | null;
  total_turns: number;
  score: number | null;
  status: string;
}

export interface SendMessageResponse {
  user_message: MessageData;
  ai_message: MessageData;
  should_end: boolean;
  session_status: string;
}

export interface EndSessionResponse {
  session_id: number;
  score: number;
  feedback_summary: string;
  summary: {
    score: number;
    summary: string;
    strengths: string[];
    improvements: string[];
  };
}

async function apiFetch<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    throw new Error(`API error: ${res.status} ${res.statusText}`);
  }
  return res.json();
}

export async function fetchScenarios(
  category?: string,
  difficulty?: string
): Promise<Scenario[]> {
  const params = new URLSearchParams();
  if (category) params.set("category", category);
  if (difficulty) params.set("difficulty", difficulty);
  const query = params.toString();
  return apiFetch(`/api/scenarios${query ? `?${query}` : ""}`);
}

export async function fetchScenario(id: number): Promise<Scenario> {
  return apiFetch(`/api/scenarios/${id}`);
}

export async function startSession(scenarioId: number) {
  return apiFetch<{
    session_id: number;
    scenario: Scenario;
    first_message: MessageData;
  }>("/api/sessions", {
    method: "POST",
    body: JSON.stringify({ scenario_id: scenarioId }),
  });
}

export async function fetchSession(sessionId: number): Promise<SessionData> {
  return apiFetch(`/api/sessions/${sessionId}`);
}

export async function fetchSessions(): Promise<SessionListItem[]> {
  return apiFetch("/api/sessions");
}

export async function sendMessage(
  sessionId: number,
  content: string
): Promise<SendMessageResponse> {
  return apiFetch(`/api/sessions/${sessionId}/messages`, {
    method: "POST",
    body: JSON.stringify({ content }),
  });
}

export async function endSession(
  sessionId: number
): Promise<EndSessionResponse> {
  return apiFetch(`/api/sessions/${sessionId}/end`, {
    method: "POST",
  });
}
