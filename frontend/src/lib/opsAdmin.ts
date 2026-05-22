"use client";

/**
 * Centralised access to the Dealix Ops admin API key on the client.
 *
 * The key is exposed via `NEXT_PUBLIC_DEALIX_ADMIN_API_KEY` and consumed by
 * the founder-only OPS dashboards (war room, marketing calendar, evidence
 * ledger, etc.). Components are expected to fall back to a friendly
 * "configure admin key" message when the key is absent — they must not
 * crash and must not silently send unauthenticated requests.
 */

const ADMIN_KEY_LOCAL_STORAGE_KEY = "dealix_admin_api_key_override";

function readEnvAdminKey(): string {
  return (process.env.NEXT_PUBLIC_DEALIX_ADMIN_API_KEY || "").trim();
}

function readOverrideAdminKey(): string {
  if (typeof window === "undefined") return "";
  try {
    return (window.localStorage.getItem(ADMIN_KEY_LOCAL_STORAGE_KEY) || "").trim();
  } catch {
    return "";
  }
}

/** Returns the active admin key (override wins over env). Empty string if none. */
export function getAdminApiKey(): string {
  return readOverrideAdminKey() || readEnvAdminKey();
}

/** Cheap check — does any admin key resolve at all? */
export function isOpsConfigured(): boolean {
  return getAdminApiKey().length > 0;
}

/**
 * Standard bilingual hint shown to founders when an OPS panel needs the
 * admin key but none is configured. Components render this verbatim instead
 * of attempting requests that would 401.
 *
 * Accepts either a locale string ("ar"/"en") or a boolean isAr flag — most
 * callers already compute `isAr = locale === "ar"`, so we just take it.
 */
export function opsMissingKeyMessage(localeOrIsAr: string | boolean): string {
  const isAr =
    typeof localeOrIsAr === "boolean" ? localeOrIsAr : localeOrIsAr === "ar";
  if (isAr) {
    return "هذه الشاشة للمؤسس فقط. اضبط NEXT_PUBLIC_DEALIX_ADMIN_API_KEY أو ضع مفتاحاً مؤقتاً عبر localStorage.dealix_admin_api_key_override.";
  }
  return "Founder-only view. Set NEXT_PUBLIC_DEALIX_ADMIN_API_KEY in env, or paste a temporary key into localStorage.dealix_admin_api_key_override.";
}

/** Optional helper — let the founder paste a key for the current session. */
export function setOverrideAdminKey(value: string): void {
  if (typeof window === "undefined") return;
  try {
    if (value.trim()) {
      window.localStorage.setItem(ADMIN_KEY_LOCAL_STORAGE_KEY, value.trim());
    } else {
      window.localStorage.removeItem(ADMIN_KEY_LOCAL_STORAGE_KEY);
    }
  } catch {
    // ignore — localStorage may be disabled
  }
}
