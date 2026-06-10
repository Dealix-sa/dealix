/**
 * Wave 3 free-tool scoring — pure, deterministic, no network.
 * Kept pure so it can be unit-tested and (later) mirrored server-side.
 */

export type Band = "low" | "med" | "high";
export type CtaRoute = "business-os-score" | "diagnostic" | "command-sprint";

export interface Bilingual {
  ar: string;
  en: string;
}

export interface ToolOption {
  labelAr: string;
  labelEn: string;
  /** 0..1 — share of this question's full credit. 1 = best, 0 = worst. */
  weight: number;
}

export interface ToolQuestion {
  id: string;
  promptAr: string;
  promptEn: string;
  options: ToolOption[];
  /** Shown as a "gap" when the chosen option is weak. */
  gapAr: string;
  gapEn: string;
}

export interface NextStep {
  labelAr: string;
  labelEn: string;
  route: CtaRoute;
}

export interface ToolResult {
  /** 0..100 */
  score: number;
  band: Band;
  /** Up to 3 weakest areas. */
  topGaps: Bilingual[];
  recommendedOsAr: string;
  recommendedOsEn: string;
  nextStep: NextStep;
}

export function bandFromScore(score: number): Band {
  if (score < 50) return "low";
  if (score < 75) return "med";
  return "high";
}

/**
 * Score a multiple-choice quiz.
 * @param questions question bank
 * @param answers   map of questionId -> chosen option index
 */
export function scoreQuiz(
  questions: ToolQuestion[],
  answers: Record<string, number>,
): { score: number; band: Band; gaps: Bilingual[] } {
  if (questions.length === 0) {
    return { score: 0, band: "low", gaps: [] };
  }

  let total = 0;
  const scored: { weight: number; gap: Bilingual }[] = [];

  for (const q of questions) {
    const idx = answers[q.id];
    const opt = q.options[idx];
    const weight = opt ? opt.weight : 0;
    total += weight;
    scored.push({ weight, gap: { ar: q.gapAr, en: q.gapEn } });
  }

  const score = Math.round((total / questions.length) * 100);
  const gaps = scored
    .filter((s) => s.weight < 1)
    .sort((a, b) => a.weight - b.weight)
    .slice(0, 3)
    .map((s) => s.gap);

  return { score, band: bandFromScore(score), gaps };
}

export interface LeakageInputs {
  monthlyLeads: number;
  avgDealValue: number;
  /** Current close rate, percent 0..100. */
  closeRatePct: number;
  /** Estimated share of leads with NO documented follow-up, percent 0..100. */
  followupGapPct: number;
}

export interface LeakageResult {
  /** Educational midpoint estimate of monthly value at risk (SAR). */
  estimateMid: number;
  estimateLow: number;
  estimateHigh: number;
  band: Band;
  gaps: Bilingual[];
}

/**
 * Educational estimate ONLY — never a guarantee. The UI must show the
 * educational disclaimer. Returns a ±30% range around the midpoint.
 */
export function calcRevenueLeakage(inputs: LeakageInputs): LeakageResult {
  const leads = Math.max(0, inputs.monthlyLeads);
  const value = Math.max(0, inputs.avgDealValue);
  const close = Math.min(100, Math.max(0, inputs.closeRatePct)) / 100;
  const gapShare = Math.min(100, Math.max(0, inputs.followupGapPct)) / 100;

  // Value at risk = leads that fall through the follow-up gap, at the current
  // close rate, times average deal value.
  const mid = Math.round(leads * gapShare * close * value);
  const low = Math.round(mid * 0.7);
  const high = Math.round(mid * 1.3);

  // Band reflects the SIZE of the follow-up gap, not a revenue promise.
  const band: Band = gapShare >= 0.5 ? "low" : gapShare >= 0.25 ? "med" : "high";

  const gaps: Bilingual[] = [];
  if (gapShare >= 0.25) {
    gaps.push({
      ar: "نسبة من الفرص بلا متابعة موثّقة.",
      en: "A share of opportunities has no documented follow-up.",
    });
  }
  if (close < 0.2) {
    gaps.push({
      ar: "معدل الإغلاق منخفض مقارنة بحجم الفرص.",
      en: "Close rate is low relative to opportunity volume.",
    });
  }
  if (leads > 0 && value > 0) {
    gaps.push({
      ar: "لا يوجد سجل إثبات يربط كل فرصة بخطوتها التالية.",
      en: "No proof register links each opportunity to its next step.",
    });
  }

  return { estimateMid: mid, estimateLow: low, estimateHigh: high, band, gaps: gaps.slice(0, 3) };
}
