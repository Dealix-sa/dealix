import { NextResponse } from "next/server";
import { loadAccounts, summarize } from "@/lib/crm/crm";

export const dynamic = "force-dynamic";

export async function GET(request: Request) {
  const url = new URL(request.url);
  const segment = url.searchParams.get("segment");
  const stage = url.searchParams.get("stage");
  let accounts = loadAccounts();
  if (segment) accounts = accounts.filter((a) => a.segment === segment);
  if (stage) accounts = accounts.filter((a) => a.stage === stage);
  return NextResponse.json({
    summary: summarize(accounts),
    accounts,
    notice: "Read-only. Mutations go through founder scripts.",
  });
}

export async function POST() {
  return NextResponse.json(
    {
      error: "create_disabled",
      message: "Account creation runs through `scripts/score_leads.py` or `scripts/import_leads_csv.py`. The CRM does not accept ad-hoc POSTs in demo mode.",
    },
    { status: 405 }
  );
}
