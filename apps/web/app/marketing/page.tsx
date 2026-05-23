import { FounderShell } from "../../components/founder-shell";
import { BrandCard } from "../../components/brand/brand-card";
import { SectionHeading } from "../../components/brand/section-heading";
import { SummaryGrid } from "../../components/brand/summary-grid";
import { getMarketingSummary, getBrandSummary } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function MarketingPage() {
  const [marketing, brand] = await Promise.all([getMarketingSummary(), getBrandSummary()]);
  return (
    <FounderShell active="/marketing">
      <SectionHeading title="Marketing" subtitle="Content output, inbound funnel, brand health." />
      <BrandCard title="Marketing Summary" source={marketing.source}>
        <SummaryGrid metrics={marketing.data.metrics} />
      </BrandCard>
      <BrandCard title="Brand Summary" source={brand.source}>
        <SummaryGrid metrics={brand.data.metrics} />
      </BrandCard>
    </FounderShell>
  );
}
