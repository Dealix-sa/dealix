// Founder Dashboard — generated data mirror for static pages

export interface FounderDashboard {
  generatedAt: string;
  mode: "demo" | "production";
  summary: {
    totalAccounts: number;
    reviewPending: number;
    followupsDue: number;
    proposalReady: number;
    pipelineValueSar: number;
    topSegment: string;
  };
  topAccounts: Array<{ id: string; name: string; segment: string; score: number; stage: string; reviewStatus: string }>;
  risks: string[];
  todayActions: string[];
  assetsToCreate: string[];
  nextCeoDecision: string;
}

export const FOUNDER_DASHBOARD_DEMO: FounderDashboard = {
  generatedAt: "2026-06-11T00:00:00.000Z",
  mode: "demo",
  summary: {
    totalAccounts: 4,
    reviewPending: 1,
    followupsDue: 3,
    proposalReady: 2,
    pipelineValueSar: 167500,
    topSegment: "marketing_agency",
  },
  topAccounts: [
    { id: "demo-acc-001", name: "Demo Marketing Agency 001", segment: "marketing_agency", score: 78, stage: "drafted", reviewStatus: "draft_pending_human_review" },
    { id: "demo-acc-003", name: "Demo Logistics Group 003", segment: "logistics", score: 71, stage: "meeting", reviewStatus: "approved" },
    { id: "demo-acc-002", name: "Demo Training Co 002", segment: "training", score: 64, stage: "qualified", reviewStatus: "not_started" },
    { id: "demo-acc-004", name: "Demo Clinic 004", segment: "clinic", score: 58, stage: "new", reviewStatus: "not_started" },
  ],
  risks: [
    "Review queue has 1 draft pending — clear before any new outreach.",
    "Pipeline value SAR 167,500 is concentrated in 2 accounts — diversify the top of funnel.",
    "Demo accounts should never be reported as real traction.",
  ],
  todayActions: [
    "Approve draft for Demo Marketing Agency 001",
    "Send proposal to Demo Logistics Group 003",
    "Generate Arabic opener for Demo Training Co 002",
    "Log 1 proof item from any active delivery",
  ],
  assetsToCreate: [
    "Daily CEO brief (export .txt)",
    "Outreach draft (Arabic) for top scored lead",
    "Proposal (EN) for Demo Logistics Group 003",
  ],
  nextCeoDecision: "Approve the review queue and ship the proposal to the highest-value demo account.",
};
