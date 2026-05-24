// Dealix Runtime Reader (client-safe).
// Calls internal API for snapshots; falls back to empty stub if API unavailable.
// All data is internal — never call this from a public page.

export type Snapshot = {
  source: string;
  freshness_iso: string;
  data: Record<string, unknown>;
};

const BASE = process.env.NEXT_PUBLIC_DEALIX_INTERNAL_API ?? "";

export async function fetchSnapshot(slug: string): Promise<Snapshot> {
  if (!BASE) {
    return {
      source: "static_stub",
      freshness_iso: new Date().toISOString().slice(0, 10),
      data: {},
    };
  }
  try {
    const res = await fetch(`${BASE}/internal/founder-console/${slug}`, {
      headers: { "x-internal-key": process.env.NEXT_PUBLIC_DEALIX_INTERNAL_KEY ?? "" },
      cache: "no-store",
    });
    if (!res.ok) throw new Error(`status_${res.status}`);
    return (await res.json()) as Snapshot;
  } catch {
    return {
      source: "fallback",
      freshness_iso: new Date().toISOString().slice(0, 10),
      data: {},
    };
  }
}
