const BASE = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';
async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json', ...init?.headers },
    ...init,
  });
  if (!res.ok) throw new Error(`API ${path} → ${res.status}`);
  return res.json();
}
export const api = {
  health: () => apiFetch<{ status: string; timestamp: string }>('/health'),
  cases: {
    list: (status?: string) => apiFetch<{ total: number; items: Case[] }>(`/api/v1/cases${status ? `?status=${status}` : ''}`),
    get: (id: string) => apiFetch<Case>(`/api/v1/cases/${id}`),
    create: (body: { title: string; description?: string; research_question?: string }) =>
      apiFetch<Case>('/api/v1/cases', { method: 'POST', body: JSON.stringify(body) }),
    update: (id: string, body: Partial<Case>) =>
      apiFetch<Case>(`/api/v1/cases/${id}`, { method: 'PATCH', body: JSON.stringify(body) }),
    timeline: (id: string) => apiFetch<{ events: YEvent[] }>(`/api/v1/cases/${id}/timeline`),
    entities: (id: string) => apiFetch<{ entities: Entity[] }>(`/api/v1/cases/${id}/entities`),
    evidence: (id: string) => apiFetch<{ evidence: Evidence[] }>(`/api/v1/cases/${id}/evidence`),
    events: (id: string) => apiFetch<{ events: YEvent[] }>(`/api/v1/cases/${id}/events`),
    narratives: (id: string) => apiFetch<{ narratives: unknown[] }>(`/api/v1/cases/${id}/narratives`),
  },
  research: {
    submit: (body: { question: string; case_id?: string; sources?: string[] }) =>
      apiFetch<{ mission_id: string; status: string }>('/api/v1/research', { method: 'POST', body: JSON.stringify(body) }),
    factCheck: (body: { claim: string; case_id?: string }) =>
      apiFetch<{ mission_id: string }>('/api/v1/fact-check', { method: 'POST', body: JSON.stringify(body) }),
  },
  missions: {
    list: () => apiFetch<{ total: number; items: Mission[] }>('/api/v1/missions'),
    get: (id: string) => apiFetch<Mission>(`/api/v1/missions/${id}`),
  },
  reports: {
    list: (case_id?: string) =>
      apiFetch<{ total: number; items: Report[] }>(`/api/v1/reports${case_id ? `?case_id=${case_id}` : ''}`),
    get: (id: string) => apiFetch<Report>(`/api/v1/reports/${id}`),
  },
  graph: {
    get: () => apiFetch<{ nodes: GraphNode[]; edges: GraphEdge[]; total_nodes: number; total_edges: number }>('/api/v1/graph'),
  },
  entities: {
    list: () => apiFetch<{ total: number; items: Entity[] }>('/api/v1/entities'),
    get: (id: string) => apiFetch<Entity>(`/api/v1/entities/${id}`),
  },
};
export interface Case { case_id: string; title: string; description?: string; research_question?: string; status: string; created_at: string; updated_at: string; }
export interface YEvent { event_id: string; event_type: string; occurred_at: string; payload: Record<string, unknown>; confidence?: { score: number; label: string }; evidence?: Evidence[]; }
export interface Entity { entity_id: string; type: string; name: string; confidence: number; properties: Record<string, unknown>; }
export interface Evidence { evidence_id: string; type: string; source_id: string; excerpt?: string; locator?: string; }
export interface Mission { mission_id: string; objective: string; status: string; created_at: string; result?: unknown; }
export interface Report { report_id: string; case_id: string; title: string; content: string; confidence: { score: number; label: string }; generated_at: string; editorial_note?: string; }
export interface GraphNode { node_id: string; name: string; type: string; confidence: number; }
export interface GraphEdge { edge_id: string; source_entity_id: string; target_entity_id: string; type: string; }