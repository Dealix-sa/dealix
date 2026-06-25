import { NextResponse } from "next/server";

export const dynamic = "force-static";

const payload = {
  mode: "draft_only",
  ownerReviewRequired: true,
  source: "reports/commercial/sales_agent_company_brain/latest.json",
  metrics: [
    ["targets_loaded", "Targets loaded from lead pipeline"],
    ["packs_generated", "Sales Agent + Company Brain packs"],
    ["priority_queue", "Prioritized founder review queue"],
  ],
  lanes: [
    "Pain Signal Review",
    "Sales Agent Pack",
    "Company Brain Decision",
    "Negotiation Notes",
    "Scoped Proposal",
    "Proof Pack",
  ],
  safety: [
    "Draft mode by default",
    "Owner review required",
    "No production communication from this route",
    "No payment capture from this route",
  ],
};

export async function GET() {
  return NextResponse.json(payload);
}
