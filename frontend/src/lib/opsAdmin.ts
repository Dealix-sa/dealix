// Ops admin helpers — used by founder cockpit and ops UI components.
// When NEXT_PUBLIC_USE_DEALIX_OPS_PROXY=1, browser calls go through the
// Next.js proxy in /api/dealix-proxy and the server-side DEALIX_ADMIN_API_KEY
// is injected — so the client doesn't need to know the key.
// Otherwise the operator can set NEXT_PUBLIC_DEALIX_ADMIN_API_KEY locally.

export function getAdminApiKey(): string {
  return process.env.NEXT_PUBLIC_DEALIX_ADMIN_API_KEY || "";
}

export function isOpsConfigured(): boolean {
  if (process.env.NEXT_PUBLIC_USE_DEALIX_OPS_PROXY === "1") {
    return true;
  }
  return Boolean(getAdminApiKey());
}

export function opsMissingKeyMessage(isAr: boolean): string {
  return isAr
    ? "مفتاح المشغّل غير مضبوط — حدّد NEXT_PUBLIC_DEALIX_ADMIN_API_KEY محليًا أو فعّل NEXT_PUBLIC_USE_DEALIX_OPS_PROXY=1."
    : "Ops admin key is not configured — set NEXT_PUBLIC_DEALIX_ADMIN_API_KEY locally or enable NEXT_PUBLIC_USE_DEALIX_OPS_PROXY=1.";
}
