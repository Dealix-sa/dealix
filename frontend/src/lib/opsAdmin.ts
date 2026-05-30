// Admin API key helpers for Ops dashboard features.
// Key is stored in localStorage — never exposed through a NEXT_PUBLIC_ env var.

const ADMIN_KEY = "dealix_admin_api_key";

export function getAdminApiKey(): string {
  if (typeof window === "undefined") return "";
  try {
    return localStorage.getItem(ADMIN_KEY) || "";
  } catch {
    return "";
  }
}

export function setAdminApiKey(key: string): void {
  if (typeof window === "undefined") return;
  try {
    localStorage.setItem(ADMIN_KEY, key);
  } catch {
    // ignore storage quota errors
  }
}

export function clearAdminApiKey(): void {
  if (typeof window === "undefined") return;
  try {
    localStorage.removeItem(ADMIN_KEY);
  } catch {
    // ignore storage errors
  }
}

export function isOpsConfigured(): boolean {
  const key = getAdminApiKey();
  return Boolean(key && key.length > 0);
}

export function opsMissingKeyMessage(isAr: boolean): string {
  return isAr
    ? "مفتاح الـ API غير مُعيَّن. أدخل مفتاح المشرف لعرض هذه البيانات."
    : "Admin API key not configured. Enter your admin key to access this data.";
}
