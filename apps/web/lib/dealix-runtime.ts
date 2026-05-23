// Dealix internal runtime client — server-side fetch helpers.
// Reads from /api/v1/internal/* with a soft fallback so the Founder Console
// always renders even when the backend is offline.

const BASE = process.env.DEALIX_INTERNAL_BASE ?? "http://localhost:8000";
const TOKEN = process.env.DEALIX_INTERNAL_TOKEN ?? "";

export type RuntimeResult<T> = {
  data: T;
  source: "api" | "fallback";
  fetched_at: string;
  error?: string;
};

async function call<T>(path: string, fallback: T): Promise<RuntimeResult<T>> {
  const fetched_at = new Date().toISOString();
  try {
    const res = await fetch(`${BASE}${path}`, {
      headers: TOKEN ? { "x-dealix-internal-token": TOKEN } : {},
      cache: "no-store",
    });
    if (!res.ok) {
      return { data: fallback, source: "fallback", fetched_at, error: `HTTP ${res.status}` };
    }
    const data = (await res.json()) as T;
    return { data, source: "api", fetched_at };
  } catch (err: unknown) {
    return {
      data: fallback,
      source: "fallback",
      fetched_at,
      error: err instanceof Error ? err.message : "unknown",
    };
  }
}

export const getCEOSummary = () =>
  call("/api/v1/internal/ceo/summary", {
    pipeline_value_sar: 0,
    pipeline_count: 0,
    deals_won_this_quarter: 0,
    cash_collected_30d_sar: 0,
    open_approvals: 0,
    incidents_open: 0,
    runway_months: null,
    note: "Connect runtime worker to populate live CEO summary.",
  });

export const getSalesFunnel = () =>
  call("/api/v1/internal/sales/funnel", {
    stages: [
      { stage: "lead", count: 0 },
      { stage: "engaged", count: 0 },
      { stage: "qualified", count: 0 },
      { stage: "proposal_sent", count: 0 },
      { stage: "negotiation", count: 0 },
      { stage: "won", count: 0 },
    ],
  });

export const getApprovals = () =>
  call<{ items: Array<{ id: string; type: string; risk: string; summary: string; created_at: string }> }>(
    "/api/v1/internal/approvals",
    { items: [] },
  );

export const getWorkerHealth = () =>
  call<{ workers: Array<{ id: string; name: string; status: string; last_run: string | null; failure_count: number }> }>(
    "/api/v1/internal/workers/health",
    { workers: [] },
  );

export const getTrustFlags = () =>
  call<{ flags: Array<{ id: string; severity: string; description: string }> }>(
    "/api/v1/internal/trust/flags",
    { flags: [] },
  );

export const getFinanceSummary = () =>
  call("/api/v1/internal/finance/summary", {
    cash_collected_30d_sar: 0,
    pipeline_value_sar: 0,
    arr_estimate_sar: 0,
    invoices_outstanding: 0,
    ai_cost_30d_usd: 0,
    margin_health: "unknown",
  });

export const getDistributionSummary = () =>
  call("/api/v1/internal/distribution/summary", {
    channels: [],
    sectors: [],
    experiments_open: 0,
  });

export const getDeliveryQueue = () =>
  call<{ items: Array<{ id: string; client: string; sprint: string; status: string }> }>(
    "/api/v1/internal/delivery/queue",
    { items: [] },
  );

export const getRetentionQueue = () =>
  call<{ items: Array<{ client: string; health: string; next_action: string; due: string }> }>(
    "/api/v1/internal/retention/queue",
    { items: [] },
  );

export const getProofLibrary = () =>
  call<{ items: Array<{ id: string; sector: string; title: string; approval_state: string }> }>(
    "/api/v1/internal/proof/library",
    { items: [] },
  );

export const getAuditEvents = () =>
  call<{ items: Array<{ id: string; actor: string; action: string; ts: string; risk: string }> }>(
    "/api/v1/internal/audit/events",
    { items: [] },
  );

export const getControlPlaneSummary = () =>
  call("/api/v1/internal/control/summary", {
    agents_total: 0,
    agents_enabled: 0,
    policies_active: 0,
    kill_switches_open: 0,
    last_eval_gate: null,
  });

export const getPolicies = () =>
  call<{ policies: Array<{ id: string; rule: string; severity: string }> }>(
    "/api/v1/internal/control/policies",
    { policies: [] },
  );

export const getAgentRegistry = () =>
  call<{ agents: Array<{ id: string; name: string; approval_class_max: string; enabled: boolean }> }>(
    "/api/v1/internal/control/agents",
    { agents: [] },
  );

export const getEvalStatus = () =>
  call("/api/v1/internal/evals/status", {
    last_run: null,
    suites: [],
    pass_rate: null,
    blocking_failures: 0,
  });

export const getProductization = () =>
  call<{ candidates: Array<{ id: string; offer: string; rung: string; readiness: string }>; ladder: Array<{ rung: string; name: string }> }>(
    "/api/v1/internal/product/productization",
    { candidates: [], ladder: [] },
  );

export const getSecurityStatus = () =>
  call("/api/v1/internal/security/status", {
    secrets_scan: "unknown",
    dependency_scan: "unknown",
    pdpl_review: "unknown",
    incident_open: 0,
  });

export const getOperatingScorecard = () =>
  call("/api/v1/internal/control/scorecard", {
    revenue_pillar: { score: null, status: "unknown" },
    trust_pillar: { score: null, status: "unknown" },
    delivery_pillar: { score: null, status: "unknown" },
    growth_pillar: { score: null, status: "unknown" },
    last_refresh: null,
  });

export const getSovereignReadiness = () =>
  call("/api/v1/internal/sovereign/readiness", {
    saudi_data_residency: "unknown",
    pdpl_alignment: "unknown",
    nca_alignment: "unknown",
    arabic_quality: "unknown",
    last_review: null,
  });

export const getBrandSummary = () =>
  call("/api/v1/internal/brand/summary", {
    wordmark: "DEALIX",
    tagline: "INTELLIGENT DEALS. REAL GROWTH.",
    assets_registered: 0,
    last_audit: null,
  });

export const getGrowthTargeting = () =>
  call<{ segments: Array<{ sector: string; priority: string; accounts: number; score: number }> }>(
    "/api/v1/internal/growth/targeting",
    { segments: [] },
  );

export const getMarketingSummary = () =>
  call<{ campaigns: number; content_in_pipeline: number; calendar_next_7_days: Array<{ day: string; topic: string }> }>(
    "/api/v1/internal/marketing/summary",
    { campaigns: 0, content_in_pipeline: 0, calendar_next_7_days: [] },
  );

export const getProductDistribution = () =>
  call<{ offers: Array<{ rung: string; offer: string; channel: string; status: string }> }>(
    "/api/v1/internal/product/distribution",
    { offers: [] },
  );

export const getCustomerSuccessSummary = () =>
  call("/api/v1/internal/customer-success/summary", {
    clients_active: 0,
    clients_at_risk: 0,
    referrals_open: 0,
    nps: null,
  });

export const getFinanceOpsSummary = () =>
  call("/api/v1/internal/finance-ops/summary", {
    invoices_open: 0,
    invoices_overdue: 0,
    cash_in_30d_sar: 0,
    ai_unit_cost_per_deal_usd: null,
  });

export const getDataPlatformSummary = () =>
  call("/api/v1/internal/data/summary", {
    primary_store: "unknown",
    dq_score: null,
    pipelines_failed_24h: 0,
    last_dq_run: null,
  });

export const getExperimentBacklog = () =>
  call<{ items: Array<{ id: string; hypothesis: string; status: string; owner: string }> }>(
    "/api/v1/internal/experiments/backlog",
    { items: [] },
  );
