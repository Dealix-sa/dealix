// Dealix Founder Console runtime client.
//
// Every getter calls the internal API (`/api/v1/internal/...`) with
// cache disabled. On any error it returns a safe fallback envelope
// marked `source: "fallback"` so pages can render even if the backend
// is down. Pages MUST surface the source so we never claim live data
// when we are serving a default.

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

async function fetchJson<T>(path: string, fallback: T): Promise<T & { source: string }> {
  try {
    const res = await fetch(`${base()}${path}`, {
      cache: "no-store",
      headers: headers(),
    });
    if (!res.ok) {
      return { ...(fallback as object), source: "fallback" } as T & { source: string };
    }
    const data = await res.json();
    return { source: "private_ops", ...data } as T & { source: string };
  } catch {
    return { ...(fallback as object), source: "fallback" } as T & { source: string };
  }
}

export type Envelope<T> = T & { source: string; as_of?: string };

export async function getCEOSummary() {
  return fetchJson("/api/v1/internal/ceo/summary", {
    top_action: "Bootstrap private ops runtime",
    status: "fallback",
    leads: 0,
    approved_outreach: 0,
    positive_replies: 0,
    proposals_due: 0,
    payment_followups: 0,
    worker_failures: 0,
    cash_collected: 0,
    risk_flags: ["private_ops_empty"],
  });
}

export async function getSalesFunnel() {
  return fetchJson("/api/v1/internal/sales/funnel", { stages: [] });
}

export async function getApprovals() {
  return fetchJson("/api/v1/internal/approvals", { items: [] });
}

export async function getWorkerHealth() {
  return fetchJson("/api/v1/internal/workers/health", { workers: [] });
}

export async function getTrustFlags() {
  return fetchJson("/api/v1/internal/trust/flags", { flags: [] });
}

export async function getFinanceSummary() {
  return fetchJson("/api/v1/internal/finance/summary", {
    cash_total: 0,
    mrr: 0,
    pipeline: 0,
    weighted_pipeline: 0,
    payment_followups: 0,
  });
}

export async function getDistributionSummary() {
  return fetchJson("/api/v1/internal/distribution/summary", {
    channels: [],
    sectors: [],
    double_down: null,
  });
}

export async function getDeliveryQueue() {
  return fetchJson("/api/v1/internal/delivery/queue", { items: [] });
}

export async function getRetentionQueue() {
  return fetchJson("/api/v1/internal/retention/queue", { items: [] });
}

export async function getProofLibrary() {
  return fetchJson("/api/v1/internal/proof/library", { items: [] });
}

export async function getAuditEvents() {
  return fetchJson("/api/v1/internal/audit/events", { events: [] });
}

export async function getControlPlaneSummary() {
  return fetchJson("/api/v1/internal/control/summary", {
    policies: 0,
    agents: 0,
    eval_suites: 0,
    scorecard: { source: "fallback" },
  });
}

export async function getPolicies() {
  return fetchJson("/api/v1/internal/control/policies", {
    version: null,
    classes: [],
    rules: [],
    trust_gates: [],
  });
}

export async function getAgentRegistry() {
  return fetchJson("/api/v1/internal/control/agents", { agents: [] });
}

export async function getEvalStatus() {
  return fetchJson("/api/v1/internal/evals/status", { suites: [], results: [] });
}

export async function getProductization() {
  return fetchJson("/api/v1/internal/product/productization", { candidates: [] });
}

export async function getSecurityStatus() {
  return fetchJson("/api/v1/internal/security/status", {
    internal_token_set: false,
    private_ops_env_set: false,
    private_ops_path: "",
    checks: [],
  });
}

export async function getOperatingScorecard() {
  return fetchJson("/api/v1/internal/control/scorecard", {
    revenue_score: null,
    trust_score: null,
    runtime_score: null,
    founder_leverage_score: null,
    productization_score: null,
    top_bottleneck: "Run: make operating-scorecard",
    next_best_action: "make operating-scorecard PRIVATE_OPS=$DEALIX_PRIVATE_OPS",
  });
}
