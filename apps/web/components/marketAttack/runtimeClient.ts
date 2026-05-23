// Dealix Market Attack Layer — runtime client.
//
// Reads internal API endpoints when reachable; falls back to deterministic
// stub data with `source: "fallback"` so the page always builds and
// renders. Never triggers external sends.

export type MarketAttackSummary = {
  source: "api" | "fallback";
  generatedAt: string;
  beachhead: {
    sector: string;
    totalScore: number;
    priority: "P0" | "P1" | "P2" | "hold" | "kill";
  } | null;
  p0Count: number;
  p1Count: number;
  openObjections: number;
  highFrequencyObjections: number;
  activeT0AndT1Accounts: number;
};

export type CampaignSummary = {
  source: "api" | "fallback";
  generatedAt: string;
  campaignsByStatus: Record<string, number>;
  queueByStatus: Record<string, number>;
  assetsPendingApproval: number;
  results: {
    impressions: number;
    clicks: number;
    replies: number;
    positiveReplies: number;
    samples: number;
    proposals: number;
    payments: number;
  };
};

export type PartnerPipelineSummary = {
  source: "api" | "fallback";
  generatedAt: string;
  byType: Record<string, number>;
  byStatus: Record<string, number>;
  highReferralPartners: number;
  whiteLabelCandidates: number;
};

export type SalesAssetSummary = {
  source: "api" | "fallback";
  generatedAt: string;
  total: number;
  byType: Record<string, number>;
  byApprovalStatus: Record<string, number>;
  championAssets: number;
};

export type AuthorityQueueSummary = {
  source: "api" | "fallback";
  generatedAt: string;
  postsPending: number;
  postsApproved: number;
  insightsValidated: number;
  reportIdeas: number;
};

const FALLBACK_TIMESTAMP = "1970-01-01T00:00:00Z";

const FALLBACK_MARKET_ATTACK: MarketAttackSummary = {
  source: "fallback",
  generatedAt: FALLBACK_TIMESTAMP,
  beachhead: { sector: "construction", totalScore: 38, priority: "P0" },
  p0Count: 1,
  p1Count: 4,
  openObjections: 4,
  highFrequencyObjections: 0,
  activeT0AndT1Accounts: 3
};

const FALLBACK_CAMPAIGNS: CampaignSummary = {
  source: "fallback",
  generatedAt: FALLBACK_TIMESTAMP,
  campaignsByStatus: { draft: 3, live: 0, complete: 0 },
  queueByStatus: { queued: 3, approved: 0, sent: 0 },
  assetsPendingApproval: 4,
  results: {
    impressions: 0,
    clicks: 0,
    replies: 0,
    positiveReplies: 0,
    samples: 0,
    proposals: 0,
    payments: 0
  }
};

const FALLBACK_PARTNERS: PartnerPipelineSummary = {
  source: "fallback",
  generatedAt: FALLBACK_TIMESTAMP,
  byType: { agency: 1, erp_crm: 1, cybersecurity_grc: 1 },
  byStatus: { prospect: 3 },
  highReferralPartners: 2,
  whiteLabelCandidates: 0
};

const FALLBACK_SALES_ASSETS: SalesAssetSummary = {
  source: "fallback",
  generatedAt: FALLBACK_TIMESTAMP,
  total: 5,
  byType: { one_pager: 1, proposal: 1, sample: 1, objection: 1, proof_safe: 1 },
  byApprovalStatus: { pending: 5 },
  championAssets: 0
};

const FALLBACK_AUTHORITY: AuthorityQueueSummary = {
  source: "fallback",
  generatedAt: FALLBACK_TIMESTAMP,
  postsPending: 3,
  postsApproved: 0,
  insightsValidated: 1,
  reportIdeas: 3
};

function apiBase(): string {
  if (typeof process !== "undefined" && process.env?.DEALIX_INTERNAL_API_BASE) {
    return process.env.DEALIX_INTERNAL_API_BASE;
  }
  return "";
}

async function tryFetch<T>(path: string, fallback: T): Promise<T> {
  const base = apiBase();
  if (!base) {
    return fallback;
  }
  try {
    const res = await fetch(`${base}${path}`, {
      headers: { Accept: "application/json" },
      cache: "no-store"
    });
    if (!res.ok) {
      return fallback;
    }
    return (await res.json()) as T;
  } catch {
    return fallback;
  }
}

export async function getMarketAttackSummary(): Promise<MarketAttackSummary> {
  return tryFetch<MarketAttackSummary>(
    "/api/v1/internal/market-attack/summary",
    FALLBACK_MARKET_ATTACK
  );
}

export async function getCampaignSummary(): Promise<CampaignSummary> {
  return tryFetch<CampaignSummary>(
    "/api/v1/internal/campaigns/summary",
    FALLBACK_CAMPAIGNS
  );
}

export async function getPartnerPipeline(): Promise<PartnerPipelineSummary> {
  return tryFetch<PartnerPipelineSummary>(
    "/api/v1/internal/partners/pipeline",
    FALLBACK_PARTNERS
  );
}

export async function getSalesAssetSummary(): Promise<SalesAssetSummary> {
  return tryFetch<SalesAssetSummary>(
    "/api/v1/internal/sales-assets/summary",
    FALLBACK_SALES_ASSETS
  );
}

export async function getAuthorityQueue(): Promise<AuthorityQueueSummary> {
  return tryFetch<AuthorityQueueSummary>(
    "/api/v1/internal/authority/queue",
    FALLBACK_AUTHORITY
  );
}
