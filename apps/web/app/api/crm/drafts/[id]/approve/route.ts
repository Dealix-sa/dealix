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
  const { reviewer } = payload ?? {};
  if (!reviewer || typeof reviewer !== "string") {
    return NextResponse.json({ error: "reviewer_required" }, { status: 400 });
  }
  return NextResponse.json({
    accepted: true,
    draftId: id,
    reviewer,
    decidedAt: new Date().toISOString(),
    notice:
      "Approval recorded. The outbound message is NOT sent automatically. Use the customer's own WhatsApp/email channel after manual review.",
  });
}
