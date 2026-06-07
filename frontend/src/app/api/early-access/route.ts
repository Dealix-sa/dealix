/**
 * Same-origin email capture for the hero / footer CTA forms.
 * Forwards to the backend public early-access endpoint and degrades
 * gracefully (confirm + Calendly) when the API is not yet wired.
 */
import { NextRequest, NextResponse } from "next/server";

const API_BASE = (
  process.env.DEALIX_API_URL ||
  process.env.NEXT_PUBLIC_API_URL ||
  "http://localhost:8000"
).replace(/\/$/, "");

const CALENDLY_FALLBACK =
  process.env.NEXT_PUBLIC_CALENDLY_URL ||
  "https://calendly.com/sami-assiri11/dealix-demo";

export async function POST(req: NextRequest) {
  let body: Record<string, unknown>;
  try {
    body = await req.json();
  } catch {
    return NextResponse.json({ ok: false, detail: "invalid_json" }, { status: 400 });
  }

  if (body.website) {
    return NextResponse.json({ ok: true, calendly_url: CALENDLY_FALLBACK });
  }

  const email = String(body.email || "").trim();
  if (!email.includes("@") || email.length < 5) {
    return NextResponse.json({ ok: false, detail: "invalid_email" }, { status: 422 });
  }

  try {
    const upstream = await fetch(`${API_BASE}/api/v1/public/early-access`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
      cache: "no-store",
    });
    const data = await upstream.json().catch(() => ({}));
    if (upstream.ok) {
      return NextResponse.json({ ...data, ok: true, delivery: "captured" });
    }
    return NextResponse.json(
      { ok: false, detail: data.detail || "rejected" },
      { status: upstream.status },
    );
  } catch {
    return NextResponse.json({
      ok: true,
      delivery: "pending",
      calendly_url: CALENDLY_FALLBACK,
      message: "تم الاستلام · Received",
    });
  }
}
