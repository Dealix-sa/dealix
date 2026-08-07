import { NextResponse } from "next/server";

export const dynamic = "force-dynamic";

const ALLOWED_STAGES = [
  "new",
  "scored",
  "drafted",
  "outreach_sent",
  "qualified",
  "proposal_sent",
  "won",
  "lost",
];

export async function POST(request: Request, { params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  let payload: any;
  try {
    payload = await request.json();
  } catch {
    return NextResponse.json({ error: "invalid_json" }, { status: 400 });
  }
  const { stage, reviewer } = payload ?? {};
  if (!stage || !ALLOWED_STAGES.includes(stage)) {
    return NextResponse.json(
      { error: "invalid_stage", allowed: ALLOWED_STAGES },
      { status: 400 }
    );
  }
  if (!reviewer || typeof reviewer !== "string") {
    return NextResponse.json({ error: "reviewer_required" }, { status: 400 });
  }
  return NextResponse.json({
    accepted: true,
    id,
    stage,
    reviewer,
    notice: "Stage change recorded as a review request. Apply persistently via `scripts/mark_*` operators.",
  });
}
