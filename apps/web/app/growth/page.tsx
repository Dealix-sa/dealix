import { FounderShell } from "../../components/founder-shell";
import { BrandCard } from "../../components/brand/brand-card";
import { SectionHeading } from "../../components/brand/section-heading";
import { RowsTable } from "../../components/brand/rows-table";
import { getGrowthTargeting } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function GrowthPage() {
  const targeting = await getGrowthTargeting();
  return (
    <FounderShell active="/growth">
      <SectionHeading title="Growth Targeting" subtitle="ICP, sectors, targeting health." />
      <BrandCard title="Targeting" source={targeting.source}>
        <RowsTable rows={targeting.data.rows} emptyMessage="No targeting rows yet." />
      </BrandCard>
    </FounderShell>
  );
}
