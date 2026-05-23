/**
 * Founder Console runtime client.
 *
 * Every function calls the internal API and falls back to a small,
 * obviously-tagged fallback payload so the UI always renders even when
 * the backend is unreachable. Fallback responses have `source: "fallback"`
 * and must never be presented as production data.
 */

export type DealixSource = "runtime" | "fallback" | "mixed";

export interface CEOSummary {
  top_action: string;
  status: string;
  risk_flags: number;
  cash_collected_sar: number;
  approved_outreach: number;
  sent_outreach: number;
  positive_replies: number;
  proposals_due: number;
  payment_follow_ups: number;
  source: DealixSource;
  generated_at?: string;
}

export interface SalesFunnel {
  lead_intelligence_count: number;
  a_leads: number;
  pending_approval: number;
  approved_outreach: number;
  sent: number;
  replies: number;
  positive_replies: number;
  samples: number;
  proposals: number;
  payment_capture: number;
  source: DealixSource;
}

export interface ApprovalItem {
  approval_id: string;
  type: string;
  approval_class: string;
  risk_level: string;
  summary: string;
  evidence: string;
  recommended_action: string;
  created_at: string;
  [key: string]: string;
}

export interface WorkerRow {
  worker: string;
  last_run: string;
  status: string;
  failures_24h: string;
  next_run: string;
  notes: string;
  [key: string]: string;
}

export interface TrustFlag {
  flag_id: string;
  category: string;
  severity: string;
  summary: string;
  evidence: string;
  status: string;
  created_at: string;
  [key: string]: string;
}

export interface FinanceSummary {
  cash_collected_sar: number;
  pipeline_sar: number;
  weighted_pipeline_sar: number;
  payment_follow_ups: number;
  mrr_sar: number;
  source: DealixSource;
}

export interface DistributionSummary {
  sectors: Array<Record<string, string>>;
  channels: Array<Record<string, string>>;
  experiments: Array<Record<string, string>>;
  double_down: string | null;
  source: DealixSource;
}

export interface AuditEvent {
  approval_id: string;
  type: string;
  actor: string;
  decision: string;
  reason: string;
  approval_class: string;
  risk_level: string;
  policy_result: string;
  source_endpoint: string;
  timestamp: string;
  external_action_allowed: string;
  [key: string]: string;
}

export interface ControlSummary {
  policies: {
    version: number | string;
    approval_classes: string[];
    rules: string[];
    source: DealixSource;
  };
  agents: {
    version: number | string;
    agent_count: number;
    kill_switch_required: boolean;
    eval_required: boolean;
    source: DealixSource;
  };
  open_risks: number;
  eval_gate: { blocking_failures: number; suites: number };
  operating_scorecard: OperatingScorecard;
  production_token_set: boolean;
  source: DealixSource;
}

export interface AgentRegistryItem {
  id: string;
  name: string;
  purpose: string;
  approval_class_max: string;
  external_action_allowed: boolean;
  kill_switch: boolean;
  eval_required: boolean;
  enabled: boolean;
  last_change_reason?: string | null;
  last_changed_at?: string | null;
}

export interface OperatingScorecard {
  revenue_score: number;
  trust_score: number;
  runtime_score: number;
  founder_leverage_score: number;
  productization_score: number;
  top_bottleneck: string;
  next_best_action: string;
  source: DealixSource;
  generated_at?: string;
}

const API_BASE = (process.env.NEXT_PUBLIC_DEALIX_API ?? "http://localhost:8000").replace(/\/$/, "");
const INTERNAL_TOKEN = process.env.NEXT_PUBLIC_DEALIX_INTERNAL_TOKEN ?? "";

const FALLBACK_NOTE = "fallback (API unreachable or not deployed)";

async function call<T>(path: string, fallback: T): Promise<T> {
  try {
    const headers: Record<string, string> = { Accept: "application/json" };
    if (INTERNAL_TOKEN) headers["X-Dealix-Internal-Token"] = INTERNAL_TOKEN;
    const resp = await fetch(`${API_BASE}${path}`, {
      headers,
      cache: "no-store",
      next: { revalidate: 0 }
    });
    if (!resp.ok) return fallback;
    return (await resp.json()) as T;
  } catch {
    return fallback;
  }
}

export function getCEOSummary(): Promise<CEOSummary> {
  return call<CEOSummary>("/api/v1/internal/ceo/summary", {
    top_action: FALLBACK_NOTE,
    status: "unknown",
    risk_flags: 0,
    cash_collected_sar: 0,
    approved_outreach: 0,
    sent_outreach: 0,
    positive_replies: 0,
    proposals_due: 0,
    payment_follow_ups: 0,
    source: "fallback"
  });
}

export function getSalesFunnel(): Promise<SalesFunnel> {
  return call<SalesFunnel>("/api/v1/internal/sales/funnel", {
    lead_intelligence_count: 0,
    a_leads: 0,
    pending_approval: 0,
    approved_outreach: 0,
    sent: 0,
    replies: 0,
    positive_replies: 0,
    samples: 0,
    proposals: 0,
    payment_capture: 0,
    source: "fallback"
  });
}

export function getApprovals(): Promise<{ items: ApprovalItem[]; count: number; source: DealixSource }> {
  return call("/api/v1/internal/approvals", {
    items: [] as ApprovalItem[],
    count: 0,
    source: "fallback" as DealixSource
  });
}

export function getWorkerHealth(): Promise<{ workers: WorkerRow[]; count: number; source: DealixSource }> {
  return call("/api/v1/internal/workers/health", {
    workers: [] as WorkerRow[],
    count: 0,
    source: "fallback" as DealixSource
  });
}

export function getTrustFlags(): Promise<{
  flags: TrustFlag[];
  count: number;
  suppression_count: number;
  a3_attempts: number;
  source: DealixSource;
}> {
  return call("/api/v1/internal/trust/flags", {
    flags: [],
    count: 0,
    suppression_count: 0,
    a3_attempts: 0,
    source: "fallback" as DealixSource
  });
}

export function getFinanceSummary(): Promise<FinanceSummary> {
  return call<FinanceSummary>("/api/v1/internal/finance/summary", {
    cash_collected_sar: 0,
    pipeline_sar: 0,
    weighted_pipeline_sar: 0,
    payment_follow_ups: 0,
    mrr_sar: 0,
    source: "fallback"
  });
}

export function getDistributionSummary(): Promise<DistributionSummary> {
  return call<DistributionSummary>("/api/v1/internal/distribution/summary", {
    sectors: [],
    channels: [],
    experiments: [],
    double_down: null,
    source: "fallback"
  });
}

export function getDeliveryQueue() {
  return call<{ items: Array<Record<string, string>>; count: number; source: DealixSource }>(
    "/api/v1/internal/delivery/queue",
    { items: [], count: 0, source: "fallback" }
  );
}

export function getRetentionQueue() {
  return call<{ items: Array<Record<string, string>>; count: number; source: DealixSource }>(
    "/api/v1/internal/retention/queue",
    { items: [], count: 0, source: "fallback" }
  );
}

export function getProofLibrary() {
  return call<{ items: Array<Record<string, string>>; count: number; source: DealixSource }>(
    "/api/v1/internal/proof/library",
    { items: [], count: 0, source: "fallback" }
  );
}

export function getAuditEvents(): Promise<{ events: AuditEvent[]; count: number; source: DealixSource }> {
  return call("/api/v1/internal/audit/events", {
    events: [] as AuditEvent[],
    count: 0,
    source: "fallback" as DealixSource
  });
}

export function getEvalStatus() {
  return call<{
    suites: Array<Record<string, string>>;
    blocking_failures: number;
    source: DealixSource;
  }>("/api/v1/internal/evals/status", {
    suites: [],
    blocking_failures: 0,
    source: "fallback"
  });
}

export function getProductization() {
  return call<{
    candidates: Array<Record<string, string>>;
    count: number;
    source: DealixSource;
  }>("/api/v1/internal/product/productization", {
    candidates: [],
    count: 0,
    source: "fallback"
  });
}

export function getSecurityStatus() {
  return call<{
    controls: Array<Record<string, string>>;
    count: number;
    production_token_set?: boolean;
    source: DealixSource;
  }>("/api/v1/internal/security/status", {
    controls: [],
    count: 0,
    production_token_set: false,
    source: "fallback"
  });
}

export function getControlPlaneSummary(): Promise<ControlSummary> {
  return call<ControlSummary>("/api/v1/internal/control/summary", {
    policies: { version: 0, approval_classes: [], rules: [], source: "fallback" },
    agents: { version: 0, agent_count: 0, kill_switch_required: true, eval_required: true, source: "fallback" },
    open_risks: 0,
    eval_gate: { blocking_failures: 0, suites: 0 },
    operating_scorecard: {
      revenue_score: 0,
      trust_score: 0,
      runtime_score: 0,
      founder_leverage_score: 0,
      productization_score: 0,
      top_bottleneck: "no_data",
      next_best_action: FALLBACK_NOTE,
      source: "fallback"
    },
    production_token_set: false,
    source: "fallback"
  });
}

export function getAgentRegistry(): Promise<{
  agents: AgentRegistryItem[];
  agent_count: number;
  source: DealixSource;
}> {
  return call("/api/v1/internal/control/agents", {
    agents: [] as AgentRegistryItem[],
    agent_count: 0,
    source: "fallback" as DealixSource
  });
}

export function getOperatingScorecard(): Promise<OperatingScorecard> {
  return call<OperatingScorecard>("/api/v1/internal/control/scorecard", {
    revenue_score: 0,
    trust_score: 0,
    runtime_score: 0,
    founder_leverage_score: 0,
    productization_score: 0,
    top_bottleneck: "no_data",
    next_best_action: FALLBACK_NOTE,
    source: "fallback"
  });
}
