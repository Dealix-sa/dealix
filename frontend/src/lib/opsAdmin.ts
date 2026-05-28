/**
 * Founder ops-admin client-side helpers.
 *
 * The /[locale]/ops/* surfaces are gated by an admin API key that the
 * founder pastes into NEXT_PUBLIC_DEALIX_ADMIN_API_KEY (or accepts via
 * a server-side proxy when NEXT_PUBLIC_USE_DEALIX_OPS_PROXY=1).
 *
 * These helpers centralize the read so each component does not duplicate
 * the env-var fallback chain.
 *
 * Doctrine note: this returns a key for OUTBOUND requests to the Dealix
 * backend; it never auto-sends external email/WhatsApp/etc. (doctrine #1).
 */

/** Read the admin API key from env, with a localStorage fallback for dev. */
export function getAdminApiKey(): string {
  if (typeof process !== "undefined") {
    const fromEnv = process.env.NEXT_PUBLIC_DEALIX_ADMIN_API_KEY;
    if (fromEnv && fromEnv.length > 0) return fromEnv;
  }
  if (typeof window !== "undefined") {
    try {
      const stored = window.localStorage.getItem("dealix.adminApiKey");
      if (stored && stored.length > 0) return stored;
    } catch {
      // localStorage may be blocked (private mode); fall through
    }
  }
  return "";
}

/** True if the ops console has a usable admin key OR a proxy is configured. */
export function isOpsConfigured(): boolean {
  const key = getAdminApiKey();
  if (key && key.length > 0) return true;
  if (typeof process !== "undefined") {
    const proxy = process.env.NEXT_PUBLIC_USE_DEALIX_OPS_PROXY;
    if (proxy === "1" || proxy === "true") return true;
  }
  return false;
}

/** Bilingual "missing key" message used by Ops* panels for non-blocking UX. */
export function opsMissingKeyMessage(isAr: boolean): string {
  return isAr
    ? "لم يتم تعيين مفتاح Dealix Admin. أضف NEXT_PUBLIC_DEALIX_ADMIN_API_KEY أو فعّل البروكسي."
    : "Dealix Admin key not set. Add NEXT_PUBLIC_DEALIX_ADMIN_API_KEY or enable the proxy.";
}
