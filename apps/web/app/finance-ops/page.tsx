import { FounderShell } from "../../components/founder-shell";
import { BrandCard } from "../../components/brand/brand-card";
import { SectionHeading } from "../../components/brand/section-heading";
import { SummaryGrid } from "../../components/brand/summary-grid";
import { getFinanceOpsSummary } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function FinanceOpsPage() {
  const ops = await getFinanceOpsSummary();
  return (
    <FounderShell active="/finance-ops">
      <SectionHeading title="Finance Ops" subtitle="Invoices, ZATCA, refunds, payouts." />
      <BrandCard title="Summary" source={ops.source}>
        <SummaryGrid metrics={ops.data.metrics} />
      </BrandCard>
    </FounderShell>
  );
}
