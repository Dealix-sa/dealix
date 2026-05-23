// Founder Console runtime client.
// Every reader calls the internal API (`/api/v1/internal/...`) with
// `cache: "no-store"` so the console always reflects the latest private
// runtime state. When the API is unreachable or returns 401, we return
// a safe fallback marked `source: "fallback"` so the UI can clearly say
// "not wired up yet" instead of silently lying.

type Source = "private_runtime" | "computed" | "fallback" | "registry_yaml" | "policy_yaml" | "eval_yaml";

export type RuntimeEnvelope<T> = T & {
  source: Source;
  note?: string;
  generated_at?: string;
};

const DEFAULT_BASE = process.env.NEXT_PUBLIC_DEALIX_API_BASE ?? "";
const TOKEN = process.env.DEALIX_INTERNAL_TOKEN ?? "";

function url(path: string): string {
  return `${DEFAULT_BASE}${path}`;
}

async function fetchJson<T>(path: string, fallback: T): Promise<RuntimeEnvelope<T>> {
  try {
    const res = await fetch(url(path), {
      cache: "no-store",
      headers: TOKEN ? { "X-Dealix-Internal-Token": TOKEN } : undefined,
    });
    if (!res.ok) {
      return { ...fallback, source: "fallback", note: `http ${res.status}` };
    }
    const data = (await res.json()) as Partial<RuntimeEnvelope<T>> & T;
    return { source: "fallback", ...data } as RuntimeEnvelope<T>;
  } catch (err: unknown) {
    const note = err instanceof Error ? err.message : "fetch failed";
    return { ...fallback, source: "fallback", note };
  }
}

// ── readers ─────────────────────────────────────────────────────────────────

export function getCEOSummary() {
  return fetchJson("/api/v1/internal/ceo/summary", {
    leads_total: 0,
    approvals_open: 0,
    cash_total_sar: 0,
    incidents_open: 0,
  });
}

export function getSalesFunnel() {
  return fetchJson<{ stages: { name: string; count: number }[] }>(
    "/api/v1/internal/sales/funnel",
    { stages: [] },
  );
}

export function getApprovals() {
  return fetchJson<{ approvals: Record<string, string>[] }>(
    "/api/v1/internal/approvals",
    { approvals: [] },
  );
}

export function getWorkerHealth() {
  return fetchJson<{ workers: Record<string, string>[] }>(
    "/api/v1/internal/workers/health",
    { workers: [] },
  );
}

export function getTrustFlags() {
  return fetchJson<{ flags: Record<string, string>[] }>(
    "/api/v1/internal/trust/flags",
    { flags: [] },
  );
}

export function getFinanceSummary() {
  return fetchJson("/api/v1/internal/finance/summary", {
    cash_total_sar: 0,
    capture_open: 0,
    ai_unit_economics_rows: 0,
  });
}

export function getDistributionSummary() {
  return fetchJson<{
    by_channel: Record<string, string>[];
    by_sector: Record<string, string>[];
  }>("/api/v1/internal/distribution/summary", { by_channel: [], by_sector: [] });
}

export function getDeliveryQueue() {
  return fetchJson<{ items: Record<string, string>[] }>(
    "/api/v1/internal/delivery/queue",
    { items: [] },
  );
}

export function getRetentionQueue() {
  return fetchJson<{ items: Record<string, string>[] }>(
    "/api/v1/internal/retention/queue",
    { items: [] },
  );
}

export function getProofLibrary() {
  return fetchJson<{ items: Record<string, string>[] }>(
    "/api/v1/internal/proof/library",
    { items: [] },
  );
}

export function getAuditEvents() {
  return fetchJson<{ events: Record<string, string>[] }>(
    "/api/v1/internal/audit/events",
    { events: [] },
  );
}

export function getControlPlaneSummary() {
  return fetchJson<{
    policies: { classes_count: number; rules_count: number };
    agents: { count: number; agents: string[] };
    evals: { count: number; suites: string[] };
    scorecard: { scorecard_md: string | null };
    sovereign: { readiness_md: string | null };
    auth_mode: string;
  }>("/api/v1/internal/control/summary", {
    policies: { classes_count: 0, rules_count: 0 },
    agents: { count: 0, agents: [] },
    evals: { count: 0, suites: [] },
    scorecard: { scorecard_md: null },
    sovereign: { readiness_md: null },
    auth_mode: "unknown",
  });
}

export function getPolicies() {
  return fetchJson("/api/v1/internal/control/policies", {
    classes_count: 0,
    rules_count: 0,
  });
}

export function getAgentRegistry() {
  return fetchJson<{ agents: string[]; count: number }>(
    "/api/v1/internal/control/agents",
    { agents: [], count: 0 },
  );
}

export function getEvalStatus() {
  return fetchJson<{ suites: string[]; count: number }>(
    "/api/v1/internal/evals/status",
    { suites: [], count: 0 },
  );
}

export function getProductization() {
  return fetchJson<{ candidates: Record<string, string>[] }>(
    "/api/v1/internal/product/productization",
    { candidates: [] },
  );
}

export function getSecurityStatus() {
  return fetchJson<{ items: Record<string, string>[]; auth_mode?: string }>(
    "/api/v1/internal/security/status",
    { items: [] },
  );
}

export function getOperatingScorecard() {
  return fetchJson<{ scorecard_md: string | null }>(
    "/api/v1/internal/control/scorecard",
    { scorecard_md: null },
  );
}

export function getSovereignReadiness() {
  return fetchJson<{ readiness_md: string | null }>(
    "/api/v1/internal/sovereign/readiness",
    { readiness_md: null },
  );
}
