/**
 * Heuristic AI scoring (0..100) for leads / risk.
 * No external AI call — fast, deterministic, transparent.
 */

interface LeadScoreInputs {
  estimatedValue?: number | string | null;
  industry?: string | null;
  contactEmail?: string | null;
  contactPhone?: string | null;
  city?: string | null;
  notes?: string | null;
  engagementScore?: number | null;
  source?: string | null;
}

const HIGH_VALUE_INDUSTRIES = new Set([
  "oil_gas",
  "petrochemical",
  "banking",
  "finance",
  "telecom",
  "government",
  "healthcare",
  "energy",
  "construction",
  "real_estate",
]);

const STRONG_SOURCES = new Set([
  "referral",
  "demo_booked",
  "warm_intro",
  "trade_show",
  "partner",
]);

export function scoreLead(input: LeadScoreInputs): number {
  let score = 40;

  const v = typeof input.estimatedValue === "string"
    ? parseFloat(input.estimatedValue)
    : input.estimatedValue || 0;
  if (v >= 500_000) score += 25;
  else if (v >= 100_000) score += 18;
  else if (v >= 25_000) score += 10;
  else if (v >= 5_000) score += 4;

  const ind = (input.industry || "").toLowerCase();
  if (HIGH_VALUE_INDUSTRIES.has(ind)) score += 10;

  if (input.contactEmail && /@/.test(input.contactEmail)) score += 6;
  if (input.contactPhone) score += 4;
  if (input.notes && input.notes.length > 40) score += 4;

  const src = (input.source || "").toLowerCase();
  if (STRONG_SOURCES.has(src)) score += 8;

  const eng = input.engagementScore || 0;
  score += Math.min(15, Math.max(0, Math.round(eng / 7)));

  return Math.max(0, Math.min(100, Math.round(score)));
}

export function scoreRisk(input: {
  industry?: string;
  monthlyRevenue?: number;
  yearsActive?: number;
  hasFinanceTeam?: boolean;
  usesCRM?: boolean;
  hasSubscriptions?: boolean;
}): {
  score: number;
  level: "low" | "medium" | "high";
  factors: string[];
} {
  let score = 50;
  const factors: string[] = [];

  if (input.usesCRM === false) {
    score += 12;
    factors.push("no_crm");
  }
  if (input.hasFinanceTeam === false) {
    score += 8;
    factors.push("no_finance_team");
  }
  if (input.hasSubscriptions === true) {
    score += 6;
    factors.push("recurring_revenue_complexity");
  }
  if ((input.yearsActive ?? 5) < 2) {
    score += 10;
    factors.push("young_company");
  }
  if ((input.monthlyRevenue ?? 0) > 1_000_000) {
    score -= 5;
    factors.push("scale_dampens_risk");
  }
  if (HIGH_VALUE_INDUSTRIES.has((input.industry || "").toLowerCase())) {
    score -= 4;
    factors.push("regulated_industry_signal");
  }

  score = Math.max(0, Math.min(100, score));
  const level = score >= 70 ? "high" : score >= 45 ? "medium" : "low";
  return { score, level, factors };
}
