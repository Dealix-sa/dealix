// Dealix runtime — server-side fetch helper for the Founder Console.
//
// Reads INTERNAL_API_URL + DEALIX_ADMIN_API_KEY from env (server-only).
// Returns {data, source, freshness, is_estimate} with graceful fallback
// so npm build never depends on a live backend.

export type RuntimeEnvelope<T = unknown> = {
  data: T;
  source: "api" | "fallback";
  freshness: string;
  is_estimate: boolean;
};

const FALLBACK_DATA: Record<string, RuntimeEnvelope> = {
  "/api/v1/internal/founder-console/ceo/daily-brief": {
    data: [
      {
        section: "top_action",
        summary_en: "Run `make everything`; populate /opt/dealix CSVs.",
        summary_ar: "شغّل make everything ثم املأ ملفات /opt/dealix.",
      },
    ],
    source: "fallback",
    freshness: new Date().toISOString(),
    is_estimate: true,
  },
  "/api/v1/internal/founder-console/capital-allocation": {
    data: [{ category: "_no_data_", monthly_sar: "0", is_estimate: "true" }],
    source: "fallback",
    freshness: new Date().toISOString(),
    is_estimate: true,
  },
  "/api/v1/internal/founder-console/market-attack": {
    data: [{ sector: "_none_yet_", paid_pilots: "0", is_estimate: "true" }],
    source: "fallback",
    freshness: new Date().toISOString(),
    is_estimate: true,
  },
  "/api/v1/internal/founder-console/ai-governance": {
    data: [
      { label: "agents_registered", value: "—" },
      { label: "machines_registered", value: "—" },
      { label: "kill_switch_default", value: "true" },
    ],
    source: "fallback",
    freshness: new Date().toISOString(),
    is_estimate: true,
  },
  "/api/v1/internal/founder-console/trust/flags": {
    data: [{ flag_id: "init", summary_en: "no flags", summary_ar: "لا توجد تنبيهات" }],
    source: "fallback",
    freshness: new Date().toISOString(),
    is_estimate: true,
  },
  "/api/v1/internal/founder-console/audit/recent": {
    data: [{ decision_id: "init", action_class: "_no_data_", approved: "n/a" }],
    source: "fallback",
    freshness: new Date().toISOString(),
    is_estimate: true,
  },
};

export async function fetchInternal<T = unknown>(
  path: string,
): Promise<RuntimeEnvelope<T>> {
  const base = process.env.INTERNAL_API_URL || "";
  const token = process.env.DEALIX_ADMIN_API_KEY || "";
  if (!base || !token) {
    return (FALLBACK_DATA[path] ?? {
      data: [] as unknown as T,
      source: "fallback",
      freshness: new Date().toISOString(),
      is_estimate: true,
    }) as RuntimeEnvelope<T>;
  }
  try {
    const res = await fetch(`${base}${path}`, {
      headers: { Authorization: `Bearer ${token}` },
      cache: "no-store",
    });
    if (!res.ok) {
      return (FALLBACK_DATA[path] ?? {
        data: [] as unknown as T,
        source: "fallback",
        freshness: new Date().toISOString(),
        is_estimate: true,
      }) as RuntimeEnvelope<T>;
    }
    const json = (await res.json()) as RuntimeEnvelope<T>;
    return json;
  } catch {
    return (FALLBACK_DATA[path] ?? {
      data: [] as unknown as T,
      source: "fallback",
      freshness: new Date().toISOString(),
      is_estimate: true,
    }) as RuntimeEnvelope<T>;
  }
}
