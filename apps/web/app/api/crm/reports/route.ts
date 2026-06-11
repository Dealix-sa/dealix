import { NextResponse } from "next/server";
import { loadAccounts, summarize } from "@/lib/crm/crm";

export const dynamic = "force-dynamic";

export async function GET() {
  const accounts = loadAccounts();
  const s = summarize(accounts);
  const today = new Date().toISOString().slice(0, 10);
  const dueToday = accounts.filter((a) => a.nextActionDate <= today).length;
  return NextResponse.json({ asOf: today, summary: s, dueToday });
}
