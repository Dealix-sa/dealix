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
  const { body, author } = payload ?? {};
  if (!body || typeof body !== "string") return NextResponse.json({ error: "body_required" }, { status: 400 });
  if (!author || typeof author !== "string") return NextResponse.json({ error: "author_required" }, { status: 400 });
  if (body.length > 5000) return NextResponse.json({ error: "body_too_long" }, { status: 400 });
  return NextResponse.json({
    accepted: true,
    accountId: id,
    note: { body, author, createdAt: new Date().toISOString() },
    notice: "Notes are echoed in demo mode. Persist with `scripts/add_account_note.py` once implemented.",
  });
}
