import { NextResponse } from "next/server";
import { loadAccounts, loadOutreachQueue } from "@/lib/crm/crm";

export const dynamic = "force-dynamic";

export async function GET(_request: Request, { params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const a = loadAccounts().find((x) => x.id === id);
  if (!a) return NextResponse.json({ error: "not_found" }, { status: 404 });
  const drafts = loadOutreachQueue().filter((d) => d.accountId === id);
  return NextResponse.json({ account: a, drafts });
}
