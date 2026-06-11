import { NextResponse } from "next/server";

export async function GET() {
  const data = {
    generated_at: new Date().toISOString(),
    mode: "demo",
    summary: {
      total_accounts: 12,
      review_pending: 4,
      followups_due: 2,
      proposal_ready: 1,
      pipeline_value_sar: 0,
      top_segment: "B2B Services",
    },
    top_accounts: [
      { id: "demo-001", name: "Acme Saudi", score: 87, stage: "proposal_ready", value_sar: 0, next_action: "Review proposal draft" },
      { id: "demo-002", name: "Beta Clinic", score: 72, stage: "qualified", value_sar: 0, next_action: "Schedule diagnostic call" },
    ],
    risks: [
      { level: "medium", area: "pipeline", note: "No closed-won deals this week." },
      { level: "low", area: "governance", note: "All drafts pending review. No auto-send risk." },
    ],
    today_actions: [
      "Review 4 outreach drafts before EOD",
      "Approve or edit proposal for demo-001",
    ],
    assets_to_create: [
      "Industry weakness one-pager for Healthcare",
    ],
    next_ceo_decision: "Approve pricing for Managed OS Retainer pilot.",
    disclaimer: "Demo data. Populate with real data in production.",
  };

  return NextResponse.json(data, { status: 200 });
}
