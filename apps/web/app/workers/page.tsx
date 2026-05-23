import { FounderShell } from "../../components/founder-shell";
import { BrandCard } from "../../components/brand/brand-card";
import { SectionHeading } from "../../components/brand/section-heading";
import { RowsTable } from "../../components/brand/rows-table";
import { getWorkerHealth } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function WorkersPage() {
  const health = await getWorkerHealth();
  return (
    <FounderShell active="/workers">
      <SectionHeading title="Workers" subtitle="Live agent + worker health." />
      <BrandCard title="Worker Health" source={health.source}>
        <RowsTable rows={health.data.rows} emptyMessage="No worker telemetry yet." />
      </BrandCard>
    </FounderShell>
  );
}
