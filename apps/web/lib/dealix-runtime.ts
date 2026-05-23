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
  source: "api" | "fallback";
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
  source: "api" | "fallback";
};

export type ApprovalItem = {
  id: string;
  type: string;
  company: string;
  approval_class: "A0" | "A1" | "A2" | "A3";
  risk_level: "Low" | "Medium" | "High" | "Critical";
  summary: string;
  evidence?: string;
  recommended_action?: string;
  status: "Pending" | "Approved" | "Rejected" | "Needs Edit" | "Escalated";
};

export type WorkerHealth = {
  name: string;
  last_run: string | null;
  status: "ok" | "warning" | "failing" | "stale";
  backlog: number;
  error?: string;
};

export type TrustFlag = {
  id: string;
  category: string;
  severity: "Low" | "Medium" | "High" | "Critical";
  summary: string;
  opened_at: string;
};

export type FinanceSummary = {
  cash_collected_sar: number;
  mrr_sar: number;
  pipeline_sar: number;
  weighted_pipeline_sar: number;
  payment_followups_due: number;
  source: "api" | "fallback";
};

export type DistributionSummary = {
  channels: number;
  active_sectors: number;
  experiments: number;
  double_down: string | null;
  source: "api" | "fallback";
};

const API_BASE = process.env.DEALIX_API_BASE_URL || "http://localhost:8000";

async function safeGet<T>(path: string, fallback: T): Promise<T> {
  try {
    const res = await fetch(`${API_BASE}${path}`, { cache: "no-store" });
    if (!res.ok) return fallback;
    return (await res.json()) as T;
  } catch {
    return fallback;
  }
}

export function getCEOSummary(): Promise<CEOSummary> {
  return safeGet<CEOSummary>("/api/v1/internal/ceo/summary", {
    top_action: "Connect internal runtime API",
    status: "Frontend fallback",
    risk_flags: 0,
    cash_collected_sar: 0,
    approved_outreach: 0,
    positive_replies: 0,
    proposals_due: 0,
    payment_followups_due: 0,
    last_updated: new Date().toISOString(),
    source: "fallback"
  });
}

export function getSalesFunnel(): Promise<SalesFunnel> {
  return safeGet<SalesFunnel>("/api/v1/internal/sales/funnel", {
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
    source: "fallback"
  });
}

export function getApprovals(): Promise<ApprovalItem[]> {
  return safeGet<ApprovalItem[]>("/api/v1/internal/approvals", []);
}

export function getWorkers(): Promise<WorkerHealth[]> {
  return safeGet<WorkerHealth[]>("/api/v1/internal/workers/health", []);
}

export function getTrustFlags(): Promise<TrustFlag[]> {
  return safeGet<TrustFlag[]>("/api/v1/internal/trust/flags", []);
}

export function getFinanceSummary(): Promise<FinanceSummary> {
  return safeGet<FinanceSummary>("/api/v1/internal/finance/summary", {
    cash_collected_sar: 0,
    mrr_sar: 0,
    pipeline_sar: 0,
    weighted_pipeline_sar: 0,
    payment_followups_due: 0,
    source: "fallback"
  });
}

export function getDistributionSummary(): Promise<DistributionSummary> {
  return safeGet<DistributionSummary>("/api/v1/internal/distribution/summary", {
    channels: 0,
    active_sectors: 0,
    experiments: 0,
    double_down: null,
    source: "fallback"
  });
}

export function getDeliveryQueue(): Promise<Array<Record<string, unknown>>> {
  return safeGet<Array<Record<string, unknown>>>("/api/v1/internal/delivery/queue", []);
}

export function getRetentionQueue(): Promise<Array<Record<string, unknown>>> {
  return safeGet<Array<Record<string, unknown>>>("/api/v1/internal/retention/queue", []);
}

export function getProofLibrary(): Promise<Array<Record<string, unknown>>> {
  return safeGet<Array<Record<string, unknown>>>("/api/v1/internal/proof/library", []);
}
