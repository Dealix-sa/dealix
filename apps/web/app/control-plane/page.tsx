import { FounderShell, KV } from "../../components/founder-shell";
import { getControlPlaneSummary } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function ControlPlanePage() {
  const data = await getControlPlaneSummary();
  return (
    <FounderShell title="Control Plane" source={data.source}>
      <section className="card">
        <h2>Governance counts</h2>
        <KV k="Policy classes" v={data.policies.classes_count} />
        <KV k="Policy rules" v={data.policies.rules_count} />
        <KV k="Agents in registry" v={data.agents.count} />
        <KV k="Eval suites" v={data.evals.count} />
        <KV k="Internal API auth mode" v={data.auth_mode} />
      </section>
      <section className="card">
        <h2>Operating scorecard (preview)</h2>
        <pre>{data.scorecard.scorecard_md ?? "(not generated yet)"}</pre>
      </section>
      <section className="card">
        <h2>Sovereign readiness (preview)</h2>
        <pre>{data.sovereign.readiness_md ?? "(not generated yet)"}</pre>
      </section>
    </FounderShell>
  );
}
