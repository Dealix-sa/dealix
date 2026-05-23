import { FounderShell } from "../../components/founder-shell";
import { getSovereignReadiness } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function SovereignPage() {
  const data = await getSovereignReadiness();
  return (
    <FounderShell title="Sovereign Readiness" source={data.source}>
      <section className="card">
        <h2>Readiness scorecard</h2>
        {data.readiness_md ? (
          <pre>{data.readiness_md}</pre>
        ) : (
          <p>
            Run <code>make sovereign-readiness</code> to generate the
            readiness markdown. Until then, this view shows fallback.
          </p>
        )}
      </section>
    </FounderShell>
  );
}
