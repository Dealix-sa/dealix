import { FounderPage } from "../../components/brand/founder-page";
import { MetricCard } from "../../components/brand/metric-card";

export default function AiGovernancePage() {
  return (
    <FounderPage
      title="AI Governance"
      subtitle="NIST AI RMF: Govern · Map · Measure · Manage."
      blocks={[
        {
          title: "Snapshot",
          body: (
            <div className="dlx-grid">
              <MetricCard label="Registered agents" value="24" />
              <MetricCard label="Eval pass rate" value="96%" />
              <MetricCard label="A3 auto attempts" value="0" />
              <MetricCard label="Prompt-injection tests" value="PASS" />
              <MetricCard label="Kill switches" value="enabled" />
              <MetricCard label="External actions" value="approval-gated" />
            </div>
          ),
        },
        { title: "Policy", body: <p>policies/dealix_control_policy.yaml</p> },
        { title: "Registries", body: <p>registries/agent_registry.yaml · registries/machine_registry.yaml</p> },
        { title: "Eval gate", body: <p>evals/gates/dealix_agent_eval_gate.yaml</p> },
      ]}
    />
  );
}
