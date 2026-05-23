/**
 * Founder Console action client.
 *
 * Every function POSTs to an internal API endpoint that writes to the
 * audit log. None of these functions performs direct external sending —
 * they only record the founder's decision and let downstream workers
 * pick up the approved item.
 */

const API_BASE = (process.env.NEXT_PUBLIC_DEALIX_API ?? "http://localhost:8000").replace(/\/$/, "");
const INTERNAL_TOKEN = process.env.NEXT_PUBLIC_DEALIX_INTERNAL_TOKEN ?? "";

export interface ApprovalDecisionPayload {
  reason?: string;
  evidence?: string;
  risk_level?: string;
}

export interface AgentStatePayload {
  reason?: string;
}

async function post<T>(path: string, body: unknown): Promise<T> {
  const headers: Record<string, string> = {
    Accept: "application/json",
    "Content-Type": "application/json"
  };
  if (INTERNAL_TOKEN) headers["X-Dealix-Internal-Token"] = INTERNAL_TOKEN;
  const resp = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers,
    body: JSON.stringify(body ?? {}),
    cache: "no-store"
  });
  if (!resp.ok) {
    const text = await resp.text().catch(() => "");
    throw new Error(`POST ${path} failed: ${resp.status} ${text}`);
  }
  return (await resp.json()) as T;
}

export function approveApproval(id: string, reason?: string, payload?: ApprovalDecisionPayload) {
  return post(`/api/v1/internal/approvals/${encodeURIComponent(id)}/approve`, {
    reason,
    ...payload
  });
}

export function rejectApproval(id: string, reason?: string, payload?: ApprovalDecisionPayload) {
  return post(`/api/v1/internal/approvals/${encodeURIComponent(id)}/reject`, {
    reason,
    ...payload
  });
}

export function requestEditApproval(id: string, reason?: string, payload?: ApprovalDecisionPayload) {
  return post(`/api/v1/internal/approvals/${encodeURIComponent(id)}/request-edit`, {
    reason,
    ...payload
  });
}

export function escalateApproval(id: string, reason?: string, payload?: ApprovalDecisionPayload) {
  return post(`/api/v1/internal/approvals/${encodeURIComponent(id)}/escalate`, {
    reason,
    ...payload
  });
}

export function disableAgent(id: string, reason?: string, payload?: AgentStatePayload) {
  return post(`/api/v1/internal/control/agents/${encodeURIComponent(id)}/disable`, {
    reason,
    ...payload
  });
}

export function enableAgent(id: string, reason?: string, payload?: AgentStatePayload) {
  return post(`/api/v1/internal/control/agents/${encodeURIComponent(id)}/enable`, {
    reason,
    ...payload
  });
}
