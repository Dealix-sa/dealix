import { FounderShell } from "../../components/founder-shell";
import { BrandCard } from "../../components/brand/brand-card";
import { SectionHeading } from "../../components/brand/section-heading";
import { SummaryGrid } from "../../components/brand/summary-grid";
import { getFinanceSummary } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function FinancePage() {
  const finance = await getFinanceSummary();
  return (
    <FounderShell active="/finance">
      <SectionHeading title="Finance" subtitle="MRR, collections, AR aging, runway." />
      <BrandCard title="Summary" source={finance.source}>
        <SummaryGrid metrics={finance.data.metrics} />
      </BrandCard>
    </FounderShell>
  );
}
