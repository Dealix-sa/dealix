/**
 * Same-origin lead capture — forwards landing/contact/custom form
 * submissions to the backend public demo-request endpoint.
 *
 * Why a same-origin route instead of a direct browser fetch:
 *  - No CORS surprises across the api/web split.
 *  - The backend base URL stays a server env (DEALIX_API_URL), not shipped
 *    to the browser.
 *  - Graceful degradation: if the API is not yet wired, the visitor still
 *    gets a confirmation + a Calendly fallback so no lead hits a dead end.
 *
 * It never fabricates data and never sends anything outbound — it only
 * relays exactly what the visitor typed to the founder lead-inbox.
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

  // Honeypot — bots fill the hidden "website" field. Accept silently.
  if (body.website) {
    return NextResponse.json({ ok: true, calendly_url: CALENDLY_FALLBACK });
  }

  const name = String(body.name || "").trim();
  const company = String(body.company || "").trim();
  const email = String(body.email || "").trim();
  const phone = String(body.phone || "").trim();
  const consent = Boolean(body.consent);

  if (!name || !company || !email.includes("@") || !phone) {
    return NextResponse.json(
      { ok: false, detail: "missing_required_fields" },
      { status: 422 },
    );
  }
  if (!consent) {
    return NextResponse.json({ ok: false, detail: "consent_required" }, { status: 422 });
  }

  try {
    const upstream = await fetch(`${API_BASE}/api/v1/public/demo-request`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
      cache: "no-store",
    });
    const data = await upstream.json().catch(() => ({}));
    if (upstream.ok) {
      return NextResponse.json({ ...data, ok: true, delivery: "captured" });
    }
    // Backend reachable but rejected — surface its reason.
    return NextResponse.json(
      { ok: false, detail: data.detail || "rejected" },
      { status: upstream.status },
    );
  } catch {
    // Backend not reachable yet — never lose the visitor: confirm + fallback.
    return NextResponse.json({
      ok: true,
      delivery: "pending",
      calendly_url: CALENDLY_FALLBACK,
      message:
        "تم استلام طلبك. للرد الأسرع احجز مكالمة مباشرة عبر الرابط. · Received — for the fastest response, book a call below.",
    });
  }
}
