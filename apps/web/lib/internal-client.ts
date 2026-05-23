// Runtime client for the Dealix internal Launch / Risk / Finance / Learning
// endpoints. All routes are admin-key gated server-side; this module only
// shapes the request and degrades to a `fallback` envelope when the API is
// unreachable, so pages can still render.
//
// Usage on the server (recommended): call `getLaunchSummary()` inside a
// Server Component. Client components should never embed the admin key.

const DEFAULT_BASE =
  process.env.NEXT_PUBLIC_DEALIX_API_BASE ??
  process.env.DEALIX_API_BASE ??
  "http://localhost:8000";

function adminHeaders(): HeadersInit {
  const key = process.env.DEALIX_ADMIN_KEY ?? process.env.INTERNAL_ADMIN_KEY ?? "";
  return key ? { "X-Admin-API-Key": key } : {};
}

async function fetchJson<T>(path: string, init?: RequestInit): Promise<T | null> {
  const url = `${DEFAULT_BASE.replace(/\/$/, "")}${path}`;
  try {
    const res = await fetch(url, {
      // Do not cache — these endpoints reflect live operational state.
      cache: "no-store",
      headers: { Accept: "application/json", ...adminHeaders(), ...(init?.headers ?? {}) },
      ...init,
    });
    if (!res.ok) return null;
    return (await res.json()) as T;
  } catch {
    return null;
  }
}

export interface LaunchSummary {
  source: "api" | "fallback";
  reason?: string;
  readiness_score: number | null;
  readiness_decision: string | null;
  launch_blockers: Array<{ id?: string; description?: string; severity?: string; status?: string }>;
  next_ceo_action: string | null;
  active_campaign: string | null;
  target_sector: string | null;
  approved_assets: Array<{ id?: string; name?: string; status?: string }>;
  distribution_queues: Record<string, unknown>;
  trust_risks: Array<{ id?: string; severity?: string; description?: string; status?: string }>;
  revenue_forecast: string | null;
}

export async function getLaunchSummary(): Promise<LaunchSummary> {
  const data = await fetchJson<LaunchSummary>("/api/v1/internal/launch/summary");
  if (data) return data;
  return {
    source: "fallback",
    reason: "API unreachable or admin key missing",
    readiness_score: null,
    readiness_decision: null,
    launch_blockers: [],
    next_ceo_action: null,
    active_campaign: null,
    target_sector: null,
    approved_assets: [],
    distribution_queues: {},
    trust_risks: [],
    revenue_forecast: null,
  };
}

export interface RiskRegister {
  source: "api" | "fallback";
  reason?: string;
  total: number;
  open?: number;
  critical_open?: number;
  rows: Array<{
    risk_id?: string;
    category?: string;
    description?: string;
    severity?: string;
    likelihood?: string;
    owner?: string;
    mitigation?: string;
    status?: string;
    next_review?: string;
  }>;
}

export async function getRiskRegister(): Promise<RiskRegister> {
  const data = await fetchJson<RiskRegister>("/api/v1/internal/risks/register");
  if (data) return data;
  return {
    source: "fallback",
    reason: "API unreachable or admin key missing",
    total: 0,
    rows: [],
  };
}
