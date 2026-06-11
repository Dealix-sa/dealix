// CRM — Pipeline data layer (demo + production ready)

export type Stage = "new" | "qualified" | "drafted" | "review" | "meeting" | "proposal" | "won" | "lost" | "retainer";

export interface Account {
  id: string;
  name: string;
  segment: string;
  city: string;
  sourceType: string;
  sourceNote: string;
  visibleSignal: string;
  weaknessHypothesis: string;
  recommendedOffer: string;
  score: number;
  stage: Stage;
  owner: string;
  reviewStatus: "draft_pending_human_review" | "approved" | "rejected" | "not_started";
  demo: boolean;
  createdAt: string;
  nextAction?: string;
  nextActionDate?: string;
  monthlyValue?: number;
  setupValue?: number;
}

export const DEMO_ACCOUNTS: Account[] = [
  {
    id: "demo-acc-001",
    name: "Demo Marketing Agency 001",
    segment: "marketing_agency",
    city: "Riyadh",
    sourceType: "manual_research",
    sourceNote: "Public campaigns + slow response window",
    visibleSignal: "Slow inbound response, multiple campaigns live",
    weaknessHypothesis: "Lead response time, no follow-up cadence",
    recommendedOffer: "Revenue OS",
    score: 78,
    stage: "drafted",
    owner: "Founder",
    reviewStatus: "draft_pending_human_review",
    demo: true,
    createdAt: "2026-06-05",
    nextAction: "Approve outreach draft",
    nextActionDate: "2026-06-12",
    monthlyValue: 5000,
    setupValue: 18000,
  },
  {
    id: "demo-acc-002",
    name: "Demo Training Co 002",
    segment: "training",
    city: "Jeddah",
    sourceType: "open_data",
    sourceNote: "Public training catalog",
    visibleSignal: "Strong courses, weak post-course follow-up",
    weaknessHypothesis: "Cohort renewal, NPS drop after cohort end",
    recommendedOffer: "Delivery OS",
    score: 64,
    stage: "qualified",
    owner: "Founder",
    reviewStatus: "not_started",
    demo: true,
    createdAt: "2026-06-07",
    nextAction: "Generate Arabic opener draft",
    nextActionDate: "2026-06-12",
    monthlyValue: 6000,
    setupValue: 25000,
  },
  {
    id: "demo-acc-003",
    name: "Demo Logistics Group 003",
    segment: "logistics",
    city: "Dammam",
    sourceType: "csv_import",
    sourceNote: "Founder-supplied B2B event list",
    visibleSignal: "Manual dispatch, no SLA dashboard",
    weaknessHypothesis: "Customer updates, dispatch visibility",
    recommendedOffer: "Command Center OS",
    score: 71,
    stage: "meeting",
    owner: "Founder",
    reviewStatus: "approved",
    demo: true,
    createdAt: "2026-05-28",
    nextAction: "Send proposal",
    nextActionDate: "2026-06-12",
    monthlyValue: 9000,
    setupValue: 35000,
  },
  {
    id: "demo-acc-004",
    name: "Demo Clinic 004",
    segment: "clinic",
    city: "Riyadh",
    sourceType: "manual_research",
    sourceNote: "Google reviews scan",
    visibleSignal: "Reviews on Google, no reply system",
    weaknessHypothesis: "Reputation response, recall cadence",
    recommendedOffer: "Review & Reputation OS",
    score: 58,
    stage: "new",
    owner: "Founder",
    reviewStatus: "not_started",
    demo: true,
    createdAt: "2026-06-09",
    monthlyValue: 3500,
    setupValue: 12000,
  },
];

export function pipelineSummary(accounts: Account[]) {
  const total = accounts.length;
  const reviewPending = accounts.filter((a) => a.reviewStatus === "draft_pending_human_review").length;
  const followupsDue = accounts.filter((a) => a.nextActionDate && new Date(a.nextActionDate) <= new Date()).length;
  const proposalReady = accounts.filter((a) => a.stage === "proposal" || a.stage === "meeting").length;
  const pipelineValueSar = accounts
    .filter((a) => a.stage !== "won" && a.stage !== "lost")
    .reduce((sum, a) => sum + (a.setupValue || 0) + (a.monthlyValue || 0) * 3, 0);
  const segmentCounts = accounts.reduce<Record<string, number>>((acc, a) => {
    acc[a.segment] = (acc[a.segment] || 0) + 1;
    return acc;
  }, {});
  const topSegment = Object.entries(segmentCounts).sort((a, b) => b[1] - a[1])[0]?.[0] || "—";
  return { total, reviewPending, followupsDue, proposalReady, pipelineValueSar, topSegment };
}
