import { NextResponse } from "next/server";
import { CONTACT_EMAIL, WHATSAPP_NUMBER } from "@/lib/contact";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

// Server-side base takes priority; falls back to the public API URL.
// Empty means "backend not configured" — we degrade gracefully (202)
// instead of dropping the lead with an error.
const API_BASE = process.env.DEALIX_API_BASE || process.env.NEXT_PUBLIC_API_URL || "";

interface LeadPayload {
  company: string;
  sector: string;
  email: string;
  name: string;
  message: string;
  language_pref: string;
}

function parseLead(body: Record<string, unknown>): LeadPayload | null {
  const str = (v: unknown) => (typeof v === "string" ? v.trim() : "");
  const company = str(body.company);
  const sector = str(body.sector);
  const email = str(body.email);
  if (!company || !sector || !email || !email.includes("@")) return null;
  return {
    company: company.slice(0, 300),
    sector: sector.slice(0, 300),
    email: email.slice(0, 300),
    name: str(body.name).slice(0, 300),
    message: str(body.message).slice(0, 4000),
    language_pref: str(body.language_pref) || "ar",
  };
}

function fallbackResponse() {
  return NextResponse.json(
    {
      accepted: true,
      forwarded: false,
      next_step_ar:
        "استلمنا طلبك — للتأكيد السريع تواصل معنا مباشرة عبر واتساب أو البريد.",
      contact: { email: CONTACT_EMAIL, whatsapp: WHATSAPP_NUMBER || null },
    },
    { status: 202 },
  );
}

export async function POST(req: Request) {
  let body: Record<string, unknown>;
  try {
    body = await req.json();
  } catch {
    return NextResponse.json({ detail: "Invalid JSON body" }, { status: 400 });
  }

  const lead = parseLead(body);
  if (!lead) {
    return NextResponse.json(
      { detail: "company, sector, and a valid email are required" },
      { status: 400 },
    );
  }

  if (!API_BASE) return fallbackResponse();

  try {
    const upstream = await fetch(`${API_BASE}/api/v1/leads/website-inquiry`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(lead),
      signal: AbortSignal.timeout(6000),
    });
    if (!upstream.ok) return fallbackResponse();

    const data = await upstream.json();
    return NextResponse.json({ ...data, accepted: true, forwarded: true });
  } catch {
    return fallbackResponse();
  }
}
