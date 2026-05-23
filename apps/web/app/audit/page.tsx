import { FounderShell, DataTable } from "../../components/founder/founder-shell";
import { getAuditEvents } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function AuditPage() {
  const data = await getAuditEvents();
  return (
    <FounderShell
      title={`Audit (${data.count} events)`}
      subtitle="Append-only decision log written under ${DEALIX_PRIVATE_OPS}/trust/approval_decisions.csv."
      source={data.source}
    >
      <DataTable
        columns={[
          "timestamp",
          "approval_id",
          "type",
          "actor",
          "decision",
          "approval_class",
          "risk_level",
          "policy_result",
          "external_action_allowed"
        ]}
        rows={data.events}
      />
    </FounderShell>
  );
}
