import { FounderShell } from "../../components/founder-shell";
import { BrandCard } from "../../components/brand/brand-card";
import { SectionHeading } from "../../components/brand/section-heading";
import { SummaryGrid } from "../../components/brand/summary-grid";
import { getProductization, getProductDistribution } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function ProductPage() {
  const [prod, dist] = await Promise.all([getProductization(), getProductDistribution()]);
  return (
    <FounderShell active="/product">
      <SectionHeading title="Product" subtitle="Productization status, SLAs, distribution." />
      <BrandCard title="Productization" source={prod.source}>
        <SummaryGrid metrics={prod.data.metrics} />
      </BrandCard>
      <BrandCard title="Product Distribution" source={dist.source}>
        <SummaryGrid metrics={dist.data.metrics} />
      </BrandCard>
    </FounderShell>
  );
}
