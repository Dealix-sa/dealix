import { FounderShell } from "../../components/founder-shell";
import { getTrustFlags } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function TrustPage() {
  const flags = await getTrustFlags();
  return (
    <FounderShell title="Trust Plane">
      <p className="lead">
        Suppression, approval breaches, overclaim risks, AI eval status,
        and incidents. Surfaces issues the Trust Plane has already caught.
      </p>
      {flags.length === 0 ? (
        <section className="card">No trust flags raised.</section>
      ) : (
        <section className="grid">
          {flags.map((flag) => (
            <article key={flag.id} className="card">
              <header style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <strong>{flag.category}</strong>
                <span className="tag">{flag.severity}</span>
              </header>
              <p style={{ marginTop: 8 }}>{flag.summary}</p>
              <div className="muted">Opened: {flag.opened_at}</div>
            </article>
          ))}
        </section>
      )}
    </FounderShell>
  );
}
