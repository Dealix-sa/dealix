import { NextResponse } from "next/server";
import { loadOutreachQueue, pendingReviewCount } from "@/lib/crm/crm";

export const dynamic = "force-dynamic";

export async function GET() {
  const drafts = loadOutreachQueue();
  return NextResponse.json({
    pending: pendingReviewCount(drafts),
    total: drafts.length,
    drafts,
    notice: "Drafts are read-only. Never auto-sent. Approve via founder scripts.",
  });
}
