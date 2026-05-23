// Founder action client.
// Every action posts to the internal API, which only writes to the
// private audit log. NOTHING here performs real external sending; that
// is enforced server-side by the policy adapter and the never-auto-execute
// list in CLAUDE.md.

const DEFAULT_BASE = process.env.NEXT_PUBLIC_DEALIX_API_BASE ?? "";
const TOKEN = process.env.DEALIX_INTERNAL_TOKEN ?? "";

type ActionResult =
  | { ok: true; data: unknown }
  | { ok: false; error: string };

async function post(path: string, body: Record<string, unknown> | null = null): Promise<ActionResult> {
  try {
    const res = await fetch(`${DEFAULT_BASE}${path}`, {
      method: "POST",
      cache: "no-store",
      headers: {
        "Content-Type": "application/json",
        ...(TOKEN ? { "X-Dealix-Internal-Token": TOKEN } : {}),
      },
      body: body ? JSON.stringify(body) : null,
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
      return { ok: false, error: `http ${res.status}` };
    }
    return { ok: true, data };
  } catch (err: unknown) {
    return { ok: false, error: err instanceof Error ? err.message : "request failed" };
  }
}

export function approveApproval(id: string, reason?: string) {
  return post(`/api/v1/internal/approvals/${encodeURIComponent(id)}/approve`, reason ? { reason } : null);
}

export function rejectApproval(id: string, reason?: string) {
  return post(`/api/v1/internal/approvals/${encodeURIComponent(id)}/reject`, reason ? { reason } : null);
}

export function requestEditApproval(id: string, reason?: string) {
  return post(
    `/api/v1/internal/approvals/${encodeURIComponent(id)}/request-edit`,
    reason ? { reason } : null,
  );
}

export function escalateApproval(id: string, reason?: string) {
  return post(`/api/v1/internal/approvals/${encodeURIComponent(id)}/escalate`, reason ? { reason } : null);
}

export function disableAgent(id: string, reason?: string) {
  return post(
    `/api/v1/internal/control/agents/${encodeURIComponent(id)}/disable`,
    reason ? { reason } : null,
  );
}

export function enableAgent(id: string, reason?: string) {
  return post(
    `/api/v1/internal/control/agents/${encodeURIComponent(id)}/enable`,
    reason ? { reason } : null,
  );
}

export function retryWorker(id: string, reason?: string) {
  return post(
    `/api/v1/internal/workers/${encodeURIComponent(id)}/retry`,
    reason ? { reason } : null,
  );
}

export function markRiskAccepted(id: string, reason?: string) {
  // Risk acceptance is recorded as an "escalate" decision against the
  // matching approval entry. Same audit footprint, no external impact.
  return post(
    `/api/v1/internal/approvals/${encodeURIComponent(id)}/escalate`,
    { reason: reason ?? "risk accepted by founder" },
  );
}

export function generateScorecard() {
  // The scorecard is computed by a worker script, not by the API. The
  // console kicks the worker via the retry endpoint to keep one
  // approval-style audit trail for all founder-initiated runs.
  return post(`/api/v1/internal/workers/${encodeURIComponent("operating_scorecard")}/retry`, {
    reason: "manual scorecard generation",
  });
}
