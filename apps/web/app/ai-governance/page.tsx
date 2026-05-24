import { dealixActions } from "../../lib/dealix-actions";
import { DataTable, FounderShell } from "../../components/founder-shell";

export const dynamic = "force-dynamic";

export default async function AIGovernancePage() {
  const env = await dealixActions.aiGovernance();
  return (
    <FounderShell
      titleEn="AI Governance — Inventory"
      titleAr="حوكمة الذكاء الاصطناعي"
      source={env.source}
      freshness={env.freshness}
      isEstimate={env.is_estimate}
    >
      <p style={{ opacity: 0.7, fontSize: 14 }}>
        Read from <code>registries/agent_registry.yaml</code> and
        <code> registries/machine_registry.yaml</code>. Every registered
        agent carries <code>eval_required</code>, <code>kill_switch</code>,
        and <code>audit_required</code>.
      </p>
      <DataTable rows={env.data} />
    </FounderShell>
  );
}
