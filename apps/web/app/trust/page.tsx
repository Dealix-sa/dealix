import { FounderShell } from "../../components/founder-shell";
import { getTrustFlags } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function TrustPage() {
  const flags = await getTrustFlags();
  return (
    <FounderShell>
      <main className="p-8">
        <h1 className="text-4xl font-bold">Trust</h1>
        <p className="mt-2 max-w-3xl">
          Open trust flags: policy violations, suppression hits, and
          anomalies caught by the Trust Plane.
        </p>
        <section className="mt-8 rounded-2xl border p-6">
          {flags.length === 0 ? (
            <p>No open trust flags. The Trust Plane is quiet.</p>
          ) : (
            <ul className="grid gap-3">
              {flags.map((flag) => (
                <li key={flag.id} className="rounded-xl border p-4">
                  <p className="font-semibold">{flag.severity.toUpperCase()}</p>
                  <p>{flag.reason}</p>
                  <p className="text-xs">Raised: {flag.raised_at}</p>
                </li>
              ))}
            </ul>
          )}
        </section>
        <p className="mt-6 text-xs">
          Source: trust_flag_log · Endpoint: /api/v1/internal/trust/flags
        </p>
      </main>
    </FounderShell>
  );
}
