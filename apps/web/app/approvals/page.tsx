import { FounderShell, DataTable } from "../../components/founder/founder-shell";
import { getApprovals } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function ApprovalsPage() {
  const data = await getApprovals();
  const rows = data.items.map((item) => ({
    approval_id: item.approval_id,
    type: item.type,
    class: item.approval_class,
    risk: item.risk_level,
    summary: item.summary,
    evidence: item.evidence ? "present" : "missing",
    recommended: item.recommended_action,
    created_at: item.created_at
  }));
  return (
    <FounderShell
      title={`Approvals (${data.count})`}
      subtitle="Approve / Reject / Needs Edit / Escalate. Every decision is audited; A3 is never auto."
      source={data.source}
    >
      <DataTable
        columns={[
          "approval_id",
          "type",
          "class",
          "risk",
          "summary",
          "evidence",
          "recommended",
          "created_at"
        ]}
        rows={rows}
      />
      <div className="card" style={{ fontSize: 12, color: "#64748b" }}>
        Use the action client (apps/web/lib/dealix-actions.ts) from a server
        action or admin tool to record decisions. The internal API writes every
        decision to {"${DEALIX_PRIVATE_OPS}"}/trust/approval_decisions.csv.
      </div>
    </FounderShell>
  );
}
