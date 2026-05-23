// Founder Console v4 — runtime read client.
// Server-side fetcher that pulls live runtime from the internal API.
// All pages must surface `source` + `last_updated` so the founder can
// see freshness instead of guessing.

const RAW_BASE =
  process.env.DEALIX_INTERNAL_API_BASE ??
  process.env.NEXT_PUBLIC_DEALIX_INTERNAL_API_BASE ??
  "http://localhost:8000";

export const INTERNAL_API_BASE = RAW_BASE.replace(/\/+$/, "");

export type Freshness = {
  source: string;
  last_updated: string;
};

export type SalesFunnel = Freshness & {
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

export type ApprovalItem = {
  id: string;
  type: string;
  company: string;
  approval_class: string;
  risk_level: string;
  summary: string;
  evidence: string;
  recommended_action: string;
  status: string;
};

export type FinanceSummary = Freshness & {
  cash_collected_sar: number;
  mrr_sar: number;
  pipeline_sar: number;
  weighted_pipeline_sar: number;
  payment_followups_due: number;
};

export type CeoSummary = Freshness & {
  top_action: string;
  status: string;
  risk_flags: number;
  cash_collected_sar: number;
  approved_outreach: number;
  positive_replies: number;
  proposals_due: number;
  payment_followups_due: number;
};

export type LoadResult<T> =
  | { ok: true; data: T }
  | { ok: false; error: string };

async function fetchInternal<T>(path: string): Promise<LoadResult<T>> {
  try {
    const res = await fetch(`${INTERNAL_API_BASE}${path}`, {
      cache: "no-store",
      headers: { accept: "application/json" }
    });
    if (!res.ok) {
      return { ok: false, error: `HTTP ${res.status} from ${path}` };
    }
    const data = (await res.json()) as T;
    return { ok: true, data };
  } catch (err) {
    return {
      ok: false,
      error: err instanceof Error ? err.message : String(err)
    };
  }
}

export function loadCeoSummary() {
  return fetchInternal<CeoSummary>("/api/v1/internal/ceo/summary");
}

export function loadSalesFunnel() {
  return fetchInternal<SalesFunnel>("/api/v1/internal/sales/funnel");
}

export function loadApprovals() {
  return fetchInternal<ApprovalItem[]>("/api/v1/internal/approvals");
}

export function loadFinanceSummary() {
  return fetchInternal<FinanceSummary>("/api/v1/internal/finance/summary");
}
