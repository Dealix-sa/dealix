import { FounderShell } from "../../components/founder-shell";
import { getTrustFlags } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function TrustPage() {
  const flags = await getTrustFlags();
  const critical = flags.filter((f) => f.severity === "Critical").length;
  const high = flags.filter((f) => f.severity === "High").length;
  return (
    <FounderShell>
      <main>
        <h1>Trust</h1>
        <p>Suppression breaches, approval breaches, overclaims, AI evals, incidents.</p>
        <section className="founder-metric-grid">
          <div className="founder-metric">
            <p className="founder-metric__label">Open Flags</p>
            <p className="founder-metric__value">{flags.length}</p>
          </div>
          <div className="founder-metric">
            <p className="founder-metric__label">Critical</p>
            <p className="founder-metric__value">{critical}</p>
          </div>
          <div className="founder-metric">
            <p className="founder-metric__label">High</p>
            <p className="founder-metric__value">{high}</p>
          </div>
        </section>
        {flags.length === 0 ? (
          <p className="founder-source" style={{ marginTop: 16 }}>
            No open trust flags. Source: <code>/api/v1/internal/trust/flags</code>.
          </p>
        ) : (
          <section className="founder-metric-grid">
            {flags.map((flag) => (
              <article key={flag.id} className="founder-metric">
                <p className="founder-metric__label">
                  {flag.severity} · {flag.category}
                </p>
                <p>{flag.summary}</p>
                <p className="founder-source">Opened: {flag.opened_at}</p>
              </article>
            ))}
          </section>
        )}
      </main>
    </FounderShell>
  );
}
