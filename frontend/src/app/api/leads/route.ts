import { NextRequest, NextResponse } from "next/server";

type LeadPayload = {
  company?: string;
  name?: string;
  email?: string;
  phone?: string;
  sector?: string;
  pain?: string;
  budget?: string;
  source?: string;
  utm_source?: string;
  utm_medium?: string;
  utm_campaign?: string;
};

function scoreLead(body: LeadPayload): number {
  let score = 0;
  if (body.company) score += 15;
  if (body.email || body.phone) score += 15;
  if (body.sector) score += 10;
  if (body.pain && body.pain.length >= 20) score += 30;
  if (body.budget) score += 15;
  if (body.utm_campaign || body.source) score += 15;
  return Math.min(score, 100);
}

function validateLead(body: LeadPayload): string[] {
  const errors: string[] = [];
  if (!body.company || body.company.trim().length < 2) errors.push("company is required");
  if (!body.email && !body.phone) errors.push("email or phone is required");
  if (body.email && !/^\S+@\S+\.\S+$/.test(body.email)) errors.push("email is invalid");
  if (!body.pain || body.pain.trim().length < 10) errors.push("business pain is required");
  return errors;
}

export async function POST(req: NextRequest) {
  try {
    const body = (await req.json()) as LeadPayload;
    const errors = validateLead(body);
    if (errors.length) {
      return NextResponse.json({ ok: false, errors }, { status: 400 });
    }

    const lead = {
      id: `lead_${Date.now()}`,
      created_at: new Date().toISOString(),
      status: "new",
      score: scoreLead(body),
      ...body,
    };

    // Production note:
    // Replace this placeholder with DB insert or secure backend event.
    // Do not log sensitive data in public runtime logs.
    return NextResponse.json({ ok: true, lead });
  } catch {
    return NextResponse.json({ ok: false, errors: ["invalid json"] }, { status: 400 });
  }
}
