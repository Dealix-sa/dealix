"use client";

const LS_KEY = "dealix_admin_api_key";

export function getAdminApiKey(): string {
  if (typeof window === "undefined") {
    return process.env.NEXT_PUBLIC_DEALIX_ADMIN_API_KEY || "";
  }
  try {
    return (
      localStorage.getItem(LS_KEY) ||
      process.env.NEXT_PUBLIC_DEALIX_ADMIN_API_KEY ||
      ""
    );
  } catch {
    return process.env.NEXT_PUBLIC_DEALIX_ADMIN_API_KEY || "";
  }
}

export function setAdminApiKey(key: string): void {
  if (typeof window === "undefined") return;
  try {
    localStorage.setItem(LS_KEY, key);
  } catch {
    // ignore
  }
}

export function isOpsConfigured(): boolean {
  return getAdminApiKey().trim().length > 0;
}

export function opsMissingKeyMessage(isAr = false): string {
  return isAr
    ? "ضع NEXT_PUBLIC_DEALIX_ADMIN_API_KEY في .env.local أو أدخل مفتاح المسؤول في الإعدادات للمتابعة."
    : "Set NEXT_PUBLIC_DEALIX_ADMIN_API_KEY in .env.local or enter an admin key in settings to continue.";
}
