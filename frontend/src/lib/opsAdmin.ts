// Ops admin-key helpers — shared by the founder/ops UI surfaces.
// Mirrors the auth convention in `api.ts`: ops endpoints authenticate either
// with NEXT_PUBLIC_DEALIX_ADMIN_API_KEY (sent as X-Admin-API-Key) or, when
// NEXT_PUBLIC_USE_DEALIX_OPS_PROXY=1, via the server-side `/api/dealix-proxy`
// which injects the key — so no public key is needed in proxy mode.

export function getAdminApiKey(): string {
  return process.env.NEXT_PUBLIC_DEALIX_ADMIN_API_KEY || "";
}

function useOpsProxy(): boolean {
  return process.env.NEXT_PUBLIC_USE_DEALIX_OPS_PROXY === "1";
}

export function isOpsConfigured(): boolean {
  return getAdminApiKey().length > 0 || useOpsProxy();
}

export function opsMissingKeyMessage(isAr: boolean): string {
  return isAr
    ? "أسطح التشغيل غير مهيأة: اضبط NEXT_PUBLIC_DEALIX_ADMIN_API_KEY أو فعّل وضع الوكيل NEXT_PUBLIC_USE_DEALIX_OPS_PROXY=1."
    : "Ops surfaces are not configured: set NEXT_PUBLIC_DEALIX_ADMIN_API_KEY, or enable proxy mode with NEXT_PUBLIC_USE_DEALIX_OPS_PROXY=1.";
}
