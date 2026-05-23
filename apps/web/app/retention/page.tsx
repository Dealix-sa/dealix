import { FounderShell } from "../../components/founder-shell";
import { BrandCard } from "../../components/brand/brand-card";
import { SectionHeading } from "../../components/brand/section-heading";
import { RowsTable } from "../../components/brand/rows-table";
import { getRetentionQueue } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function RetentionPage() {
  const queue = await getRetentionQueue();
  return (
    <FounderShell active="/retention">
      <SectionHeading title="Retention" subtitle="Renewals, expansion, churn risk." />
      <BrandCard title="Retention Queue" source={queue.source}>
        <RowsTable rows={queue.data.rows} emptyMessage="No retention plays queued." />
      </BrandCard>
    </FounderShell>
  );
}
