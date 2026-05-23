import { FounderShell } from "../../components/founder-shell";
import { BrandCard } from "../../components/brand/brand-card";
import { SectionHeading } from "../../components/brand/section-heading";
import { SummaryGrid } from "../../components/brand/summary-grid";
import { getCustomerSuccessSummary } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function CustomerSuccessPage() {
  const cs = await getCustomerSuccessSummary();
  return (
    <FounderShell active="/customer-success">
      <SectionHeading title="Customer Success" subtitle="NRR, NPS, at-risk accounts." />
      <BrandCard title="Summary" source={cs.source}>
        <SummaryGrid metrics={cs.data.metrics} />
      </BrandCard>
    </FounderShell>
  );
}
