import { FounderShell } from "../../components/founder-shell";
import { BrandCard } from "../../components/brand/brand-card";
import { SectionHeading } from "../../components/brand/section-heading";
import { RowsTable } from "../../components/brand/rows-table";
import { getSalesFunnel } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function SalesCockpitPage() {
  const funnel = await getSalesFunnel();
  return (
    <FounderShell active="/sales-cockpit">
      <SectionHeading title="Sales Cockpit" subtitle="Funnel stages, conversions, next-best deals." />
      <BrandCard title="Funnel" source={funnel.source}>
        <RowsTable rows={funnel.data.rows} emptyMessage="No funnel rows yet — load sales/funnel.csv." />
      </BrandCard>
    </FounderShell>
  );
}
