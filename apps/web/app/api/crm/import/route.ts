import { NextResponse } from "next/server";

export const dynamic = "force-dynamic";

export async function POST() {
  return NextResponse.json(
    {
      error: "import_disabled",
      message:
        "Bulk import via API is disabled. Use `python3 scripts/import_leads_csv.py --csv <path>` from the founder workstation. This prevents accidental ingestion of unverified lists.",
    },
    { status: 405 }
  );
}
