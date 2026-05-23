// Dealix internal action client — server actions for Founder Console.
// Every action records intent; nothing is sent externally without trust gates.

const BASE = process.env.DEALIX_INTERNAL_BASE ?? "http://localhost:8000";
const TOKEN = process.env.DEALIX_INTERNAL_TOKEN ?? "";

export type ActionResult = {
  ok: boolean;
  audit_id?: string;
  message: string;
  source: "api" | "fallback";
};

async function post(path: string, body: unknown): Promise<ActionResult> {
  try {
    const res = await fetch(`${BASE}${path}`, {
      method: "POST",
      headers: {
        "content-type": "application/json",
        ...(TOKEN ? { "x-dealix-internal-token": TOKEN } : {}),
      },
      body: JSON.stringify(body ?? {}),
      cache: "no-store",
    });
    const data = (await res.json().catch(() => ({}))) as { audit_id?: string; message?: string };
    return {
      ok: res.ok,
      audit_id: data.audit_id,
      message: data.message ?? (res.ok ? "ok" : `HTTP ${res.status}`),
      source: "api",
    };
  } catch (err: unknown) {
    return {
      ok: false,
      message: err instanceof Error ? err.message : "unknown",
      source: "fallback",
    };
  }
}

export const approveApproval = (id: string, note?: string) =>
  post(`/api/v1/internal/approvals/${encodeURIComponent(id)}/approve`, { note });

export const rejectApproval = (id: string, note?: string) =>
  post(`/api/v1/internal/approvals/${encodeURIComponent(id)}/reject`, { note });

export const requestEditApproval = (id: string, instructions: string) =>
  post(`/api/v1/internal/approvals/${encodeURIComponent(id)}/request-edit`, { instructions });

export const escalateApproval = (id: string, escalate_to: string, reason: string) =>
  post(`/api/v1/internal/approvals/${encodeURIComponent(id)}/escalate`, { escalate_to, reason });

export const disableAgent = (id: string, reason: string) =>
  post(`/api/v1/internal/control/agents/${encodeURIComponent(id)}/disable`, { reason });

export const enableAgent = (id: string, reason: string) =>
  post(`/api/v1/internal/control/agents/${encodeURIComponent(id)}/enable`, { reason });

export const retryWorker = (id: string) =>
  post(`/api/v1/internal/workers/${encodeURIComponent(id)}/retry`, {});

export const markRiskAccepted = (risk_id: string, justification: string) =>
  post(`/api/v1/internal/control/risks/${encodeURIComponent(risk_id)}/accept`, { justification });

export const generateScorecard = () => post(`/api/v1/internal/control/scorecard/refresh`, {});

export const generateSovereignReadiness = () => post(`/api/v1/internal/sovereign/readiness/refresh`, {});

export const createExperimentDraft = (hypothesis: string, owner: string) =>
  post(`/api/v1/internal/experiments/backlog/draft`, { hypothesis, owner });

export const createCampaignDraft = (name: string, sector: string, owner: string) =>
  post(`/api/v1/internal/marketing/campaigns/draft`, { name, sector, owner });
