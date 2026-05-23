const API_BASE =
  process.env.DEALIX_API_BASE_URL || "http://localhost:8000";

export type CeoSummary = {
  top_action: string;
  status: string;
  risk_flags: number;
  cash_collected_sar: number;
  approved_outreach: number;
  positive_replies: number;
  proposals_due: number;
  payment_followups_due: number;
  last_updated: string;
  source?: string;
  trust_class?: string;
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
  last_updated?: string;
  source?: string;
  trust_class?: string;
};

export type ApprovalItem = {
  id: string;
  company: string;
  type: string;
  approval_class: string;
  risk_level: string;
  summary: string;
};

export type WorkerHealth = {
  worker: string;
  status: string;
  last_heartbeat: string;
  notes?: string;
};

export type TrustFlag = {
  id: string;
  severity: string;
  reason: string;
  raised_at: string;
};

export type FinanceSummary = {
  cash_collected_sar: number;
  mrr_sar: number;
  pipeline_sar: number;
  weighted_pipeline_sar: number;
  payment_followups_due: number;
  last_updated?: string;
  source?: string;
  trust_class?: string;
};

export type DistributionSummary = {
  channels: number;
  active_sectors: number;
  experiments: number;
  double_down: string | null;
  last_updated?: string;
  source?: string;
  trust_class?: string;
};

export type DeliveryItem = {
  id: string;
  customer: string;
  offer: string;
  due_date: string;
  status: string;
};

export type RetentionItem = {
  id: string;
  customer: string;
  renewal_due: string;
  risk: string;
};

export type ProofItem = {
  id: string;
  title: string;
  customer: string;
  outcome: string;
};

async function getJson<T>(path: string, fallback: T): Promise<T> {
  try {
    const res = await fetch(`${API_BASE}${path}`, { cache: "no-store" });
    if (!res.ok) return fallback;
    return (await res.json()) as T;
  } catch {
    return fallback;
  }
}

export function getCeoSummary() {
  return getJson<CeoSummary>("/api/v1/internal/ceo/summary", {
    top_action: "API unreachable — start the FastAPI server.",
    status: "Unknown",
    risk_flags: 0,
    cash_collected_sar: 0,
    approved_outreach: 0,
    positive_replies: 0,
    proposals_due: 0,
    payment_followups_due: 0,
    last_updated: "",
    source: "fallback",
    trust_class: "A1",
  });
}

export function getSalesFunnel() {
  return getJson<SalesFunnel>("/api/v1/internal/sales/funnel", {
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
    source: "fallback",
  });
}

export function getApprovals() {
  return getJson<ApprovalItem[]>("/api/v1/internal/approvals", []);
}

export function getWorkersHealth() {
  return getJson<WorkerHealth[]>("/api/v1/internal/workers/health", []);
}

export function getTrustFlags() {
  return getJson<TrustFlag[]>("/api/v1/internal/trust/flags", []);
}

export function getFinanceSummary() {
  return getJson<FinanceSummary>("/api/v1/internal/finance/summary", {
    cash_collected_sar: 0,
    mrr_sar: 0,
    pipeline_sar: 0,
    weighted_pipeline_sar: 0,
    payment_followups_due: 0,
    source: "fallback",
  });
}

export function getDistributionSummary() {
  return getJson<DistributionSummary>(
    "/api/v1/internal/distribution/summary",
    {
      channels: 0,
      active_sectors: 0,
      experiments: 0,
      double_down: null,
      source: "fallback",
    },
  );
}

export function getDeliveryQueue() {
  return getJson<DeliveryItem[]>("/api/v1/internal/delivery/queue", []);
}

export function getRetentionQueue() {
  return getJson<RetentionItem[]>("/api/v1/internal/retention/queue", []);
}

export function getProofLibrary() {
  return getJson<ProofItem[]>("/api/v1/internal/proof/library", []);
}
