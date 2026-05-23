const API_BASE = process.env.DEALIX_API_BASE_URL || "http://localhost:8000";

async function postAction(path: string, body: unknown): Promise<unknown> {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(body),
    cache: "no-store"
  });
  if (!res.ok) {
    throw new Error(`Action failed: ${res.status}`);
  }
  return res.json();
}

export function approveApproval(id: string, reason?: string): Promise<unknown> {
  return postAction(`/api/v1/internal/approvals/${id}/approve`, {
    decision: "approve",
    reason,
    actor: "sami"
  });
}

export function rejectApproval(id: string, reason?: string): Promise<unknown> {
  return postAction(`/api/v1/internal/approvals/${id}/reject`, {
    decision: "reject",
    reason,
    actor: "sami"
  });
}

export function requestEditApproval(id: string, reason?: string): Promise<unknown> {
  return postAction(`/api/v1/internal/approvals/${id}/request-edit`, {
    decision: "needs_edit",
    reason,
    actor: "sami"
  });
}
