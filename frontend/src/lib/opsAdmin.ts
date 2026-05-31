// Operational console admin-key helpers.
//
// The founder ops dashboards (components/gtm/*, components/business/*) call
// privileged /api/v1 endpoints. Those require an admin API key, OR they are
// routed through the server-side ops proxy (NEXT_PUBLIC_USE_DEALIX_OPS_PROXY=1)
// which injects the key server-side (see src/lib/api.ts request interceptor).
// These helpers centralize that resolution so every ops component agrees on
// what "configured" means and reads the key the same way.

const ADMIN_KEY_STORAGE = "dealix_admin_api_key";

/**
 * Resolve the admin API key.
 * Order: in-browser override (localStorage) -> build-time env -> "".
 * SSR-safe: never touches localStorage on the server.
 */
export function getAdminApiKey(): string {
  if (typeof window !== "undefined") {
    try {
      const stored = window.localStorage.getItem(ADMIN_KEY_STORAGE);
      if (stored && stored.trim()) return stored.trim();
    } catch {
      // localStorage unavailable (private mode) — fall through to env.
    }
  }
  return process.env.NEXT_PUBLIC_DEALIX_ADMIN_API_KEY || "";
}

/**
 * True when ops calls can authenticate: an admin key is present, or the
 * server-side ops proxy is enabled (it injects the key for us).
 */
export function isOpsConfigured(): boolean {
  if (getAdminApiKey()) return true;
  return process.env.NEXT_PUBLIC_USE_DEALIX_OPS_PROXY === "1";
}

/** Bilingual message shown when ops tools are not configured. */
export function opsMissingKeyMessage(isAr: boolean): string {
  return isAr
    ? "أدوات العمليات غير مفعّلة. اضبط مفتاح الإدارة (NEXT_PUBLIC_DEALIX_ADMIN_API_KEY) أو فعّل بروكسي العمليات (NEXT_PUBLIC_USE_DEALIX_OPS_PROXY=1)."
    : "Operational tools are not configured. Set the admin key (NEXT_PUBLIC_DEALIX_ADMIN_API_KEY) or enable the ops proxy (NEXT_PUBLIC_USE_DEALIX_OPS_PROXY=1).";
}
