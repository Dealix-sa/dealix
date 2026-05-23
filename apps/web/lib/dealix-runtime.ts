export type CEOSummary = {
  top_action: string;
  status: string;
  risk_flags: number;
  cash_collected_sar: number;
  approved_outreach: number;
  positive_replies: number;
  proposals_due: number;
  payment_followups_due: number;
  last_updated: string;
};

export type SalesFunnel = {
  lead_intelligence: number;
  a_leads: number;
  pending_approval: number;
  approved_outreach: number;
  sent: number;
  replies: number;
  positive_replies: number;
  samples: number;
  proposals: number;
  payment_capture: number;
};

export type ApprovalClass = "A0" | "A1" | "A2" | "A3";
export type ApprovalStatus =
  | "Pending"
  | "Approved"
  | "Rejected"
  | "Needs Edit"
  | "Escalated";
export type RiskLevel = "Low" | "Medium" | "High" | "Critical";

export type ApprovalItem = {
  id: string;
  type: string;
  company: string;
  approval_class: ApprovalClass;
  risk_level: RiskLevel;
  summary: string;
  evidence?: string | null;
  recommended_action?: string | null;
  status: ApprovalStatus;
};

export type WorkerHealth = {
  name: string;
  status: "running" | "idle" | "failed" | "stopped";
  last_run: string | null;
  backlog: number;
  failures_24h: number;
};

export type TrustFlag = {
  id: string;
  category:
    | "suppression"
    | "overclaim"
    | "approval_breach"
    | "ai_eval"
    | "incident";
  severity: RiskLevel;
  summary: string;
  opened_at: string;
};

export type FinanceSummary = {
  cash_collected_sar: number;
  mrr_sar: number;
  pipeline_sar: number;
  weighted_pipeline_sar: number;
  payment_followups_due: number;
};

export type DistributionSummary = {
  channels: number;
  active_sectors: number;
  experiments: number;
  double_down: string | null;
};

const DEFAULT_BASE = "http://localhost:8000";

function apiBase(): string {
  return (
    process.env.NEXT_PUBLIC_DEALIX_API ??
    process.env.DEALIX_API_BASE_URL ??
    DEFAULT_BASE
  );
}

export async function safeGet<T>(path: string, fallback: T): Promise<T> {
  try {
    const res = await fetch(`${apiBase()}${path}`, { cache: "no-store" });
    if (!res.ok) return fallback;
    return (await res.json()) as T;
  } catch {
    return fallback;
  }
}

export function getCEOSummary(): Promise<CEOSummary> {
  return safeGet<CEOSummary>("/api/v1/internal/founder/ceo/summary", {
    top_action: "Connect internal runtime API",
    status: "Frontend fallback",
    risk_flags: 0,
    cash_collected_sar: 0,
    approved_outreach: 0,
    positive_replies: 0,
    proposals_due: 0,
    payment_followups_due: 0,
    last_updated: new Date().toISOString(),
  });
}

export function getSalesFunnel(): Promise<SalesFunnel> {
  return safeGet<SalesFunnel>("/api/v1/internal/founder/sales/funnel", {
    lead_intelligence: 0,
    a_leads: 0,
    pending_approval: 0,
    approved_outreach: 0,
    sent: 0,
    replies: 0,
    positive_replies: 0,
    samples: 0,
    proposals: 0,
    payment_capture: 0,
  });
}

export function getApprovals(): Promise<ApprovalItem[]> {
  return safeGet<ApprovalItem[]>("/api/v1/internal/founder/approvals", []);
}

export function getWorkerHealth(): Promise<WorkerHealth[]> {
  return safeGet<WorkerHealth[]>(
    "/api/v1/internal/founder/workers/health",
    [],
  );
}

export function getTrustFlags(): Promise<TrustFlag[]> {
  return safeGet<TrustFlag[]>("/api/v1/internal/founder/trust/flags", []);
}

export function getFinanceSummary(): Promise<FinanceSummary> {
  return safeGet<FinanceSummary>("/api/v1/internal/founder/finance/summary", {
    cash_collected_sar: 0,
    mrr_sar: 0,
    pipeline_sar: 0,
    weighted_pipeline_sar: 0,
    payment_followups_due: 0,
  });
}

export function getDistributionSummary(): Promise<DistributionSummary> {
  return safeGet<DistributionSummary>(
    "/api/v1/internal/founder/distribution/summary",
    {
      channels: 0,
      active_sectors: 0,
      experiments: 0,
      double_down: null,
    },
  );
}
