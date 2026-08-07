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
  const { dueDate, action } = payload ?? {};
  if (!dueDate || !/^\d{4}-\d{2}-\d{2}$/.test(dueDate)) {
    return NextResponse.json({ error: "invalid_due_date" }, { status: 400 });
  }
  if (!action || typeof action !== "string") {
    return NextResponse.json({ error: "action_required" }, { status: 400 });
  }
  return NextResponse.json({
    accepted: true,
    accountId: id,
    followup: { dueDate, action, queuedAt: new Date().toISOString() },
    notice: "Follow-ups echo in demo mode; written via `scripts/generate_followup_queue.py`.",
  });
}
