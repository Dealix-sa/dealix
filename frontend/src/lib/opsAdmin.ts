/**
 * Ops admin key helpers — client-side utilities for founder ops panels.
 * The key is sourced from NEXT_PUBLIC_DEALIX_ADMIN_API_KEY, which is set
 * at build time via Railway environment variables (never hardcoded).
 */

export function getAdminApiKey(): string {
  return process.env.NEXT_PUBLIC_DEALIX_ADMIN_API_KEY ?? "";
}

export function isOpsConfigured(): boolean {
  return Boolean(getAdminApiKey());
}

export function opsMissingKeyMessage(isAr: boolean): string {
  return isAr
    ? "مفتاح API غير مضبوط. أضف NEXT_PUBLIC_DEALIX_ADMIN_API_KEY إلى متغيرات البيئة."
    : "Admin API key not configured. Set NEXT_PUBLIC_DEALIX_ADMIN_API_KEY in environment variables.";
}
