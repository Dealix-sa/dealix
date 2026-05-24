import { FounderShell } from "../../components/founder-console/founder-shell";
import { getLayer } from "../../lib/dealix-runtime";

export default async function AIGovernancePage() {
  const layer = await getLayer("ai_governance");
  return (
    <FounderShell
      title="AI Governance"
      subtitle="11 non-negotiables, approval thresholds, critical actions."
      source={layer.source === "live" || layer.source === "files" ? layer.source : "fallback"}
    >
      <p>
        Verifier: <code>make ai-governance</code>. Source:
        <code> docs/company/DEALIX_AI_GOVERNANCE.md</code>. Policy file:
        <code> policies/dealix_control_policy.yaml</code>.
      </p>
    </FounderShell>
  );
}
