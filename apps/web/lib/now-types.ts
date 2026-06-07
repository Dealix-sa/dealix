// TypeScript interfaces for the Dealix "DailyNowPack" served at
//   GET ${NEXT_PUBLIC_API_URL}/api/v1/now/pack   (live backend)
//   /now-pack.json                                (static fallback)
//
// Shape is FROZEN — these interfaces mirror public/now-pack.json exactly,
// including the Arabic-named fields (sector_ar, why_fit_ar, note_ar, ...).

export type TierColor = "green" | "yellow" | "orange" | "red";

export interface NowDoctrine {
  no_auto_send: boolean;
  no_scraping: boolean;
  public_data_only: boolean;
  approval_first: boolean;
  tagline_ar: string;
}

export interface PriceRangeSar {
  min: number;
  max: number;
  typical?: number;
  note?: string;
}

export interface PipelineValueSar {
  low: number;
  typical: number;
  high: number;
}

export interface FounderDailyTargets {
  company_briefs: number;
  drafts: number;
  follow_ups: number;
  proposals: number;
}

export interface NowMetrics {
  leads_total: number;
  priority_high: number;
  priority_medium: number;
  nurture: number;
  disqualified: number;
  drafts_ready: number;
  avg_fit_score: number;
  founder_daily_targets: FounderDailyTargets;
  pipeline_value_sar: PipelineValueSar;
}

export interface NowPipeline {
  new_leads_24h: number;
  drafts_awaiting: number;
  replies_to_handle: number;
  calls_today: number;
  proposals_pending: number;
  deals_at_risk: number;
}

export interface DimensionScore {
  id: string;
  score: number;
  level: string;
}

export interface RecommendedOffer {
  id: string;
  name: string;
  name_ar: string;
  why_fit_ar: string;
  entry_price_sar: PriceRangeSar;
}

export interface LeadBrief {
  what_they_do_ar: string;
  operations_complexity: string;
  public_signals: string[];
  confidence: number;
}

export interface NowLead {
  id: string;
  company_name: string;
  sector: string;
  sector_ar: string;
  city: string;
  website: string;
  source: string;
  relationship_status: string;
  fit_score: number;
  tier: string;
  tier_color: TierColor;
  tier_action_ar: string;
  dimension_scores: DimensionScore[];
  top_strengths: string[];
  top_weaknesses: string[];
  best_buyer_title: string;
  pain_points: string[];
  recommended_offer: RecommendedOffer;
  next_action: string;
  brief: LeadBrief;
}

export interface DraftSafetyChecks {
  mentions_company: boolean;
  single_pain: boolean;
  single_cta: boolean;
  no_pricing: boolean;
  within_length: boolean;
  no_overclaim: boolean;
}

export interface DraftSafety {
  safety_score: number;
  personalization_score: number;
  issues: string[];
  approved_for_review: boolean;
  checks: DraftSafetyChecks;
}

export interface DraftContact {
  to: string;
  note_ar: string;
}

export interface NowDraft {
  id: string;
  lead_id: string;
  company_name: string;
  channel: string;
  lang: string;
  offer_id: string;
  subject: string;
  body: string;
  word_count: number;
  status: string;
  safety: DraftSafety;
  contact: DraftContact;
}

export interface NowPriority {
  rank: number;
  what_ar: string;
  why_now_ar: string;
  est_minutes: number;
  linked_lead_id: string;
}

export interface NowPack {
  $schema_version: string;
  generated_at: string;
  date: string;
  tz: string;
  is_sample: boolean;
  note_ar: string;
  doctrine: NowDoctrine;
  metrics: NowMetrics;
  pipeline: NowPipeline;
  leads: NowLead[];
  drafts: NowDraft[];
  priorities: NowPriority[];
  intelligence_alerts: string[];
}

// Returned by approve/reject actions. The live API may return its own shape;
// the offline stub below is what we fall back to so the UI never blocks.
export interface DraftActionResult {
  ok: boolean;
  status: string;
  offline?: boolean;
}
