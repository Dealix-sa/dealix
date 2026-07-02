// Contact identity — env-driven so no personal numbers live in the repo.
// All values must resolve safely with zero env vars set (CI builds env-less).

export const CONTACT_EMAIL =
  process.env.NEXT_PUBLIC_CONTACT_EMAIL || "hello@dealix.me";

// Digits only (international format without "+"), e.g. "9665XXXXXXXX".
// Empty string means "not configured" — callers fall back to mailto.
export const WHATSAPP_NUMBER = (
  process.env.NEXT_PUBLIC_WHATSAPP_NUMBER || ""
).replace(/\D/g, "");

export const BOOKING_URL =
  process.env.NEXT_PUBLIC_BOOKING_URL ||
  "https://calendly.com/sami-assiri11/dealix-demo";

export function waLink(message: string): string | null {
  if (!WHATSAPP_NUMBER) return null;
  return `https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(message)}`;
}

export function mailtoLink(subject: string, body?: string): string {
  const params = new URLSearchParams();
  params.set("subject", subject);
  if (body) params.set("body", body);
  return `mailto:${CONTACT_EMAIL}?${params.toString().replace(/\+/g, "%20")}`;
}
