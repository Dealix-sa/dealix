import { FounderShell } from "../../components/founder-shell";
import { BrandCard } from "../../components/brand/brand-card";
import { SectionHeading } from "../../components/brand/section-heading";
import { SummaryGrid } from "../../components/brand/summary-grid";
import { getDistributionSummary } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function DistributionPage() {
  const dist = await getDistributionSummary();
  return (
    <FounderShell active="/distribution">
      <SectionHeading title="Distribution" subtitle="Channels, sends, opt-out and compliance posture." />
      <BrandCard title="Channel Posture" source={dist.source}>
        <SummaryGrid metrics={dist.data.metrics} />
      </BrandCard>
    </FounderShell>
  );
}
