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

function getStoredUser(): DealixSessionUser | null {
  if (typeof window === "undefined") return null;
  const raw = localStorage.getItem(USER_KEY);
  if (!raw) return null;
  try {
    const parsed = JSON.parse(raw);
    if (!parsed || typeof parsed !== "object" || typeof parsed.email !== "string") {
      return null;
    }
    return {
      email: parsed.email,
      tenant_slug:
        typeof parsed.tenant_slug === "string" ? parsed.tenant_slug : undefined,
    };
  } catch {
    return null;
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
  } else {
    localStorage.removeItem("dealix_expires_at");
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

function withBearer(init: RequestInit, token: string): RequestInit {
  const headers = new Headers(init.headers || {});
  headers.set("Authorization", `Bearer ${token}`);
  if (!headers.has("Accept")) headers.set("Accept", "application/json");
  return { ...init, headers };
}

async function rotateSession(): Promise<string | null> {
  const refreshToken = getRefreshToken();
  const user = getStoredUser();
  if (!refreshToken || !user) return null;

  const response = await fetch(apiUrl("/api/v1/auth/refresh"), {
    method: "POST",
    headers: { "Content-Type": "application/json", Accept: "application/json" },
    body: JSON.stringify({ refresh_token: refreshToken }),
    cache: "no-store",
  });
  if (!response.ok) return null;

  const tokens: DealixSessionTokens = await response.json();
  if (!tokens.access_token || !tokens.refresh_token) return null;
  persistSession(tokens, user);
  return tokens.access_token;
}

/**
 * Fetch a JWT-protected customer endpoint and rotate the refresh token once on
 * HTTP 401. The backend revokes the previous refresh token during rotation, so
 * only the newest pair is persisted. A failed rotation clears the local session.
 */
export async function authenticatedFetch(
  path: string,
  init: RequestInit = {},
): Promise<Response> {
  const accessToken = getAccessToken();
  if (!accessToken) {
    return new Response(null, { status: 401, statusText: "Missing session" });
  }

  const firstResponse = await fetch(
    apiUrl(path),
    withBearer({ ...init, cache: init.cache || "no-store" }, accessToken),
  );
  if (firstResponse.status !== 401) return firstResponse;

  try {
    const rotatedAccessToken = await rotateSession();
    if (!rotatedAccessToken) {
      clearSession();
      return firstResponse;
    }
    return await fetch(
      apiUrl(path),
      withBearer({ ...init, cache: init.cache || "no-store" }, rotatedAccessToken),
    );
  } catch {
    clearSession();
    return firstResponse;
  }
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
