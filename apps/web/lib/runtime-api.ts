const configuredApiBase =
  process.env.NEXT_PUBLIC_DEALIX_API_BASE ||
  process.env.NEXT_PUBLIC_API_URL ||
  "";

export const DEALIX_API_BASE = configuredApiBase.replace(/\/$/, "");

const TOKEN_KEY = "dealix_access_token";
const REFRESH_KEY = "dealix_refresh_token";
const USER_KEY = "dealix_user";

export interface DealixSessionTokens {
  access_token: string;
  refresh_token: string;
  expires_in?: number;
}

export interface DealixSessionUser {
  email: string;
  tenant_slug?: string;
}

export function apiUrl(path: string): string {
  const normalizedPath = path.startsWith("/") ? path : `/${path}`;
  return DEALIX_API_BASE ? `${DEALIX_API_BASE}${normalizedPath}` : normalizedPath;
}

function decodeStoredString(value: string | null): string | null {
  if (!value) return null;
  try {
    const parsed = JSON.parse(value);
    return typeof parsed === "string" ? parsed : null;
  } catch {
    // Accept raw values written by newer/other clients during migration.
    return value;
  }
}

export function getAccessToken(): string | null {
  if (typeof window === "undefined") return null;
  return decodeStoredString(localStorage.getItem(TOKEN_KEY));
}

export function getRefreshToken(): string | null {
  if (typeof window === "undefined") return null;
  return decodeStoredString(localStorage.getItem(REFRESH_KEY));
}

export function persistSession(
  tokens: DealixSessionTokens,
  user: DealixSessionUser,
): void {
  if (typeof window === "undefined") return;
  // Keep JSON encoding for compatibility with the existing axios client.
  localStorage.setItem(TOKEN_KEY, JSON.stringify(tokens.access_token));
  localStorage.setItem(REFRESH_KEY, JSON.stringify(tokens.refresh_token));
  localStorage.setItem(USER_KEY, JSON.stringify(user));
  if (tokens.expires_in) {
    localStorage.setItem(
      "dealix_expires_at",
      String(Date.now() + tokens.expires_in * 1000),
    );
  }
}

export function clearSession(): void {
  if (typeof window === "undefined") return;
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(REFRESH_KEY);
  localStorage.removeItem(USER_KEY);
  localStorage.removeItem("dealix_expires_at");
}

export function bearerHeaders(): Record<string, string> {
  const token = getAccessToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export async function parseApiError(response: Response): Promise<string> {
  try {
    const payload = await response.json();
    if (typeof payload?.detail === "string") return payload.detail;
    if (typeof payload?.message === "string") return payload.message;
  } catch {
    // Preserve the HTTP fallback below.
  }
  return `Request failed (${response.status})`;
}
