import { NextResponse } from "next/server";

export const dynamic = "force-dynamic";

export async function POST(request: Request, { params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  let payload: any;
  try {
    payload = await request.json();
  } catch {
    return NextResponse.json({ error: "invalid_json" }, { status: 400 });
  }
  const { reviewer, reason } = payload ?? {};
  if (!reviewer || typeof reviewer !== "string") {
    return NextResponse.json({ error: "reviewer_required" }, { status: 400 });
  }
  if (!reason || typeof reason !== "string" || reason.length < 5) {
    return NextResponse.json({ error: "reason_required" }, { status: 400 });
  }
  return NextResponse.json({
    accepted: true,
    draftId: id,
    reviewer,
    reason,
    decidedAt: new Date().toISOString(),
  });
}
