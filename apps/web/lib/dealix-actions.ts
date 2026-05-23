"use server";

/**
 * Server actions for the Dealix Founder Console.
 *
 * Every action posts to the internal API; the API only writes to the
 * private ops CSVs (approvals/decisions queue) — no external execution
 * happens here.
 */

const DEFAULT_BASE = "http://127.0.0.1:8000";

interface ActionResult {
  ok: boolean;
  error?: string;
}

async function postInternal(path: string, body: Record<string, unknown> = {}): Promise<ActionResult> {
  const url = `${process.env.DEALIX_INTERNAL_API_BASE || DEFAULT_BASE}${path}`;
  const token = process.env.DEALIX_INTERNAL_TOKEN || "";
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    Accept: "application/json",
  };
  if (token) headers["X-Dealix-Internal-Token"] = token;

  try {
    const resp = await fetch(url, {
      method: "POST",
      headers,
      body: JSON.stringify(body),
      cache: "no-store",
    });
    if (!resp.ok) {
      return { ok: false, error: `http_${resp.status}` };
    }
    return { ok: true };
  } catch (err) {
    return { ok: false, error: err instanceof Error ? err.message : "unknown_error" };
  }
}

export async function approveApproval(id: string): Promise<ActionResult> {
  return postInternal(`/api/v1/internal/approvals/${encodeURIComponent(id)}/approve`);
}

export async function rejectApproval(id: string, reason: string): Promise<ActionResult> {
  return postInternal(`/api/v1/internal/approvals/${encodeURIComponent(id)}/reject`, { reason });
}

export async function requestEditApproval(id: string, note: string): Promise<ActionResult> {
  return postInternal(`/api/v1/internal/approvals/${encodeURIComponent(id)}/request-edit`, { note });
}

export async function escalateApproval(id: string, reason: string): Promise<ActionResult> {
  return postInternal(`/api/v1/internal/approvals/${encodeURIComponent(id)}/escalate`, { reason });
}

export async function disableAgent(id: string): Promise<ActionResult> {
  return postInternal(`/api/v1/internal/control/agents/${encodeURIComponent(id)}/disable`);
}

export async function enableAgent(id: string): Promise<ActionResult> {
  return postInternal(`/api/v1/internal/control/agents/${encodeURIComponent(id)}/enable`);
}

export async function retryWorker(id: string): Promise<ActionResult> {
  return postInternal(`/api/v1/internal/workers/${encodeURIComponent(id)}/retry`);
}

export async function markRiskAccepted(id: string, note: string): Promise<ActionResult> {
  return postInternal(`/api/v1/internal/control/risks/${encodeURIComponent(id)}/accept`, { note });
}

export async function generateScorecard(): Promise<ActionResult> {
  return postInternal(`/api/v1/internal/control/scorecard/generate`);
}

export async function generateSovereignReadiness(): Promise<ActionResult> {
  return postInternal(`/api/v1/internal/sovereign/readiness/generate`);
}
