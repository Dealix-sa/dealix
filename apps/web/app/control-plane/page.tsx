import { FounderShell, MetricGrid, DataTable } from "../../components/founder/founder-shell";
import { getControlPlaneSummary, getAgentRegistry } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function ControlPlanePage() {
  const [summary, registry] = await Promise.all([getControlPlaneSummary(), getAgentRegistry()]);
  const scorecard = summary.operating_scorecard;

  return (
    <FounderShell
      title="Control Plane"
      subtitle={`Top bottleneck: ${scorecard.top_bottleneck} · Next: ${scorecard.next_best_action}`}
      source={summary.source}
    >
      <MetricGrid
        items={[
          { label: "Policy rules", value: summary.policies.rules.length },
          { label: "Approval classes", value: summary.policies.approval_classes.length },
          { label: "Registered agents", value: summary.agents.agent_count },
          { label: "Open risks", value: summary.open_risks },
          { label: "Eval blocking failures", value: summary.eval_gate.blocking_failures },
          { label: "Production token", value: summary.production_token_set ? "set" : "unset" }
        ]}
      />

      <h2 style={{ margin: 0 }}>Operating Scorecard</h2>
      <MetricGrid
        items={[
          { label: "Revenue", value: scorecard.revenue_score },
          { label: "Trust", value: scorecard.trust_score },
          { label: "Runtime", value: scorecard.runtime_score },
          { label: "Founder leverage", value: scorecard.founder_leverage_score },
          { label: "Productization", value: scorecard.productization_score }
        ]}
      />

      <h2 style={{ margin: 0 }}>Agent Registry</h2>
      <DataTable
        columns={[
          "id",
          "name",
          "approval_class_max",
          "external_action_allowed",
          "kill_switch",
          "enabled"
        ]}
        rows={registry.agents.map((a) => ({
          id: a.id,
          name: a.name,
          approval_class_max: a.approval_class_max,
          external_action_allowed: String(a.external_action_allowed),
          kill_switch: String(a.kill_switch),
          enabled: String(a.enabled)
        }))}
      />
    </FounderShell>
  );
}
