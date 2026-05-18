// Admin-key helpers for the governed Founder Ops surfaces.
// Ops APIs require an admin key (header `X-Admin-API-Key`) unless the
// server-side ops proxy is enabled, in which case the key is injected
// downstream and the client may run without one.

const ADMIN_KEY_STORAGE = "dealix_admin_api_key";

// Returns the admin key, or "" when none is set. Empty string (not null)
// keeps callers that pass the result straight into `api.*(key, ...)` typed.
export function getAdminApiKey(): string {
  if (typeof window !== "undefined") {
    const stored = window.localStorage.getItem(ADMIN_KEY_STORAGE);
    if (stored && stored.trim()) return stored.trim();
  }
  const env = process.env.NEXT_PUBLIC_DEALIX_ADMIN_API_KEY;
  return env && env.trim() ? env.trim() : "";
}

export function setAdminApiKey(key: string | null): void {
  if (typeof window === "undefined") return;
  if (key && key.trim()) {
    window.localStorage.setItem(ADMIN_KEY_STORAGE, key.trim());
  } else {
    window.localStorage.removeItem(ADMIN_KEY_STORAGE);
  }
}

function opsProxyEnabled(): boolean {
  return process.env.NEXT_PUBLIC_USE_DEALIX_OPS_PROXY === "1";
}

export function isOpsConfigured(): boolean {
  return getAdminApiKey().length > 0 || opsProxyEnabled();
}

export function opsMissingKeyMessage(isAr: boolean): string {
  return isAr
    ? "تشغيل المؤسس غير مفعّل — عيّن مفتاح admin في NEXT_PUBLIC_DEALIX_ADMIN_API_KEY أو فعّل وكيل التشغيل (NEXT_PUBLIC_USE_DEALIX_OPS_PROXY=1)."
    : "Founder ops not configured — set NEXT_PUBLIC_DEALIX_ADMIN_API_KEY or enable the ops proxy (NEXT_PUBLIC_USE_DEALIX_OPS_PROXY=1).";
}
