import { FounderShell } from "../../components/founder-shell";
import { BrandCard } from "../../components/brand/brand-card";
import { SectionHeading } from "../../components/brand/section-heading";
import { RowsTable } from "../../components/brand/rows-table";
import { getTrustFlags } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function TrustPage() {
  const flags = await getTrustFlags();
  return (
    <FounderShell active="/trust">
      <SectionHeading title="Trust" subtitle="Policy violations and guard flags." />
      <BrandCard title="Open Flags" source={flags.source}>
        <RowsTable rows={flags.data.rows} emptyMessage="No trust flags — guards are quiet." />
      </BrandCard>
    </FounderShell>
  );
}
