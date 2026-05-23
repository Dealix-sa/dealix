import { FounderShell } from "../../components/founder-shell";
import { BrandCard } from "../../components/brand/brand-card";
import { SectionHeading } from "../../components/brand/section-heading";
import { RowsTable } from "../../components/brand/rows-table";
import { getAuditEvents } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function AuditPage() {
  const events = await getAuditEvents();
  return (
    <FounderShell active="/audit">
      <SectionHeading title="Audit" subtitle="Append-only audit event log." />
      <BrandCard title="Events" source={events.source}>
        <RowsTable rows={events.data.rows} emptyMessage="No audit events recorded yet." />
      </BrandCard>
    </FounderShell>
  );
}
