import { dealixActions } from "../../lib/dealix-actions";
import { DataTable, FounderShell } from "../../components/founder-shell";

export const dynamic = "force-dynamic";

export default async function AuditPage() {
  const env = await dealixActions.auditRecent();
  return (
    <FounderShell
      titleEn="Audit — Recent Approval Decisions"
      titleAr="آخر قرارات الموافقات"
      source={env.source}
      freshness={env.freshness}
      isEstimate={env.is_estimate}
    >
      <p style={{ opacity: 0.7, fontSize: 14 }}>
        Backed by <code>$PRIVATE_OPS/trust/approval_decisions.csv</code>.
        No external action class executes with <code>approved=false</code>.
      </p>
      <DataTable rows={env.data} />
    </FounderShell>
  );
}
