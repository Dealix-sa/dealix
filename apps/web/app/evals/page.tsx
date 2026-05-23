import { FounderShell } from "../../components/founder-shell";
import { BrandCard } from "../../components/brand/brand-card";
import { SectionHeading } from "../../components/brand/section-heading";
import { SummaryGrid } from "../../components/brand/summary-grid";
import { getEvalStatus } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function EvalsPage() {
  const evals = await getEvalStatus();
  return (
    <FounderShell active="/evals">
      <SectionHeading title="Evals" subtitle="Agent eval suites and coverage." />
      <BrandCard title="Eval Status" source={evals.source}>
        <SummaryGrid metrics={evals.data.metrics} />
      </BrandCard>
    </FounderShell>
  );
}
