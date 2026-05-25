// Minimal fetch helper. Reads base URL from NEXT_PUBLIC_DEALIX_API_BASE.
// Pages currently render with provided sample payloads (server components pass
// fixtures as props) — when wiring live data, call `apiGet<T>(path)` server-side.

const DEFAULT_BASE = "http://localhost:8000";

export function apiBase(): string {
  return process.env.NEXT_PUBLIC_DEALIX_API_BASE ?? DEFAULT_BASE;
}

export async function apiGet<T>(path: string, init?: RequestInit): Promise<T> {
  const url = `${apiBase()}${path}`;
  const res = await fetch(url, { cache: "no-store", ...init });
  if (!res.ok) {
    throw new Error(`Dealix API ${path} → ${res.status} ${res.statusText}`);
  }
  return (await res.json()) as T;
}

export async function apiPost<T>(path: string, body: unknown, init?: RequestInit): Promise<T> {
  const url = `${apiBase()}${path}`;
  const res = await fetch(url, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(body),
    cache: "no-store",
    ...init,
  });
  if (!res.ok) {
    throw new Error(`Dealix API ${path} → ${res.status} ${res.statusText}`);
  }
  return (await res.json()) as T;
}
