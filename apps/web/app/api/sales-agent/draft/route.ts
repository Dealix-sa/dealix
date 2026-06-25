import { NextRequest, NextResponse } from "next/server";
import { buildSalesAgentDraft } from "@/lib/sales-agent-draft";

export async function POST(request: NextRequest) {
  let body: unknown;

  try {
    body = await request.json();
  } catch {
    return NextResponse.json({ error: "Invalid JSON body" }, { status: 400 });
  }

  if (!body || typeof body !== "object") {
    return NextResponse.json({ error: "Body must be an object" }, { status: 400 });
  }

  const payload = body as Record<string, unknown>;
  const company = typeof payload.company === "string" ? payload.company : "";

  if (!company.trim()) {
    return NextResponse.json({ error: "company is required" }, { status: 400 });
  }

  const result = buildSalesAgentDraft({
    company,
    sector: typeof payload.sector === "string" ? payload.sector : undefined,
    city: typeof payload.city === "string" ? payload.city : undefined,
    sourceUrl: typeof payload.sourceUrl === "string" ? payload.sourceUrl : undefined,
    senderIdentity: typeof payload.senderIdentity === "string" ? payload.senderIdentity : undefined,
  });

  return NextResponse.json(result);
}
