// Founder Console action client.
//
// Every action calls an INTERNAL endpoint only. No direct external
// action from the frontend. Server-side trust gates evaluate the
// action and write the audit record.

const RUNTIME_BASE_ENV = "NEXT_PUBLIC_DEALIX_INTERNAL_BASE";
const TOKEN_ENV = "NEXT_PUBLIC_DEALIX_INTERNAL_TOKEN";

function base(): string {
  if (typeof process !== "undefined" && process.env && process.env[RUNTIME_BASE_ENV]) {
    return process.env[RUNTIME_BASE_ENV] as string;
  }
  return "http://localhost:8000";
}

function headers(): Record<string, string> {
  const h: Record<string, string> = { "Content-Type": "application/json" };
  if (typeof process !== "undefined" && process.env && process.env[TOKEN_ENV]) {
    h["X-Dealix-Internal-Token"] = process.env[TOKEN_ENV] as string;
  }
  return h;
}

async function post(path: string, body: Record<string, unknown>): Promise<{ ok: boolean; data: unknown }> {
  try {
    const res = await fetch(`${base()}${path}`, {
      method: "POST",
      cache: "no-store",
      headers: headers(),
      body: JSON.stringify(body),
    });
    const data = await res.json().catch(() => ({}));
    return { ok: res.ok, data };
  } catch (err) {
    return { ok: false, data: { error: String(err) } };
  }
}

export async function approveApproval(id: string, reason?: string) {
  return post(`/api/v1/internal/approvals/${encodeURIComponent(id)}/approve`, { reason });
}

export async function rejectApproval(id: string, reason?: string) {
  return post(`/api/v1/internal/approvals/${encodeURIComponent(id)}/reject`, { reason });
}

export async function requestEditApproval(id: string, reason?: string) {
  return post(`/api/v1/internal/approvals/${encodeURIComponent(id)}/request-edit`, { reason });
}

export async function escalateApproval(id: string, reason?: string) {
  return post(`/api/v1/internal/approvals/${encodeURIComponent(id)}/escalate`, { reason });
}

export async function disableAgent(id: string, reason?: string) {
  return post(`/api/v1/internal/control/agents/${encodeURIComponent(id)}/disable`, { reason });
}

export async function enableAgent(id: string, reason?: string) {
  return post(`/api/v1/internal/control/agents/${encodeURIComponent(id)}/enable`, { reason });
}

export async function retryWorker(id: string, reason?: string) {
  return post(`/api/v1/internal/workers/${encodeURIComponent(id)}/retry`, { reason });
}
