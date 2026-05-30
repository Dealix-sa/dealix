/**
 * Founder ops admin-key helpers.
 *
 * Centralizes how ops/GTM components read the admin API key and decide whether
 * the ops surfaces are configured. The key is sourced from the public env var
 * `NEXT_PUBLIC_DEALIX_ADMIN_API_KEY` and sent to the backend as the
 * `X-Admin-API-Key` header (see `lib/api.ts`).
 *
 * Note: this lives under `frontend/src/lib`, which is matched by the repo-root
 * `.gitignore` `lib/` rule — it must be committed with `git add -f`.
 */

/** Returns the configured admin API key, trimmed. Empty string when unset. */
export function getAdminApiKey(): string {
  return (process.env.NEXT_PUBLIC_DEALIX_ADMIN_API_KEY ?? "").trim();
}

/** True when an admin API key is configured (ops surfaces are usable). */
export function isOpsConfigured(): boolean {
  return getAdminApiKey().length > 0;
}

/** Bilingual message shown when the admin key is missing. */
export function opsMissingKeyMessage(isAr: boolean): string {
  return isAr
    ? "مفتاح الإدارة غير مُهيّأ. اضبط NEXT_PUBLIC_DEALIX_ADMIN_API_KEY لتفعيل لوحات التشغيل."
    : "Admin key is not configured. Set NEXT_PUBLIC_DEALIX_ADMIN_API_KEY to enable ops panels.";
}
