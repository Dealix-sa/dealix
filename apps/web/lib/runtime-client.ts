// Fallback-safe runtime client for the Founder Console.
// Reads from the internal API when available; otherwise returns a
// statically-tagged fallback payload. Never throws.

export type SourcedPayload<T> = {
  source: "api" | "fallback";
  fetchedAt: string;
  data: T;
  error?: string;
};

const INTERNAL_API_BASE =
  process.env.INTERNAL_API_BASE_URL ?? "http://localhost:8000";

const INTERNAL_API_TOKEN = process.env.INTERNAL_API_TOKEN ?? "";

export async function loadInternal<T>(
  path: string,
  fallback: T,
  init?: RequestInit
): Promise<SourcedPayload<T>> {
  const url = `${INTERNAL_API_BASE.replace(/\/$/, "")}${path}`;
  const headers: Record<string, string> = {
    Accept: "application/json",
    "X-Internal-Client": "founder-console",
  };
  if (INTERNAL_API_TOKEN) {
    headers["X-Internal-Token"] = INTERNAL_API_TOKEN;
  }
  try {
    const res = await fetch(url, {
      cache: "no-store",
      headers,
      ...init,
    });
    if (!res.ok) {
      return {
        source: "fallback",
        fetchedAt: new Date().toISOString(),
        data: fallback,
        error: `HTTP ${res.status}`,
      };
    }
    const json = (await res.json()) as T;
    return {
      source: "api",
      fetchedAt: new Date().toISOString(),
      data: json,
    };
  } catch (err) {
    return {
      source: "fallback",
      fetchedAt: new Date().toISOString(),
      data: fallback,
      error: err instanceof Error ? err.message : "unknown error",
    };
  }
}
