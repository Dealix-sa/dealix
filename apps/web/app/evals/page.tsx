import { FounderShell } from "../../components/founder-shell";
import { getEvalStatus } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function EvalsPage() {
  const data = await getEvalStatus();
  return (
    <FounderShell title="Eval Gate" source={data.source}>
      <section className="card">
        <h2>Eval suites ({data.count})</h2>
        <ul>
          {data.suites.length === 0 ? (
            <li>No eval suites registered.</li>
          ) : (
            data.suites.map((s) => <li key={s}>{s}</li>)
          )}
        </ul>
        <p className="muted">
          Defined in <code>evals/gates/dealix_agent_eval_gate.yaml</code>.
          The CI workflow runs <code>scripts/verify_eval_gate.py</code> on
          every push.
        </p>
      </section>
    </FounderShell>
  );
}
