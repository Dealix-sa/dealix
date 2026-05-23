import { FounderShell } from "../../components/founder-shell";
import { BrandCard } from "../../components/brand/brand-card";
import { SectionHeading } from "../../components/brand/section-heading";
import { SummaryGrid } from "../../components/brand/summary-grid";
import { getSovereignReadiness } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function SovereignPage() {
  const readiness = await getSovereignReadiness();
  return (
    <FounderShell active="/sovereign">
      <SectionHeading title="Sovereign Readiness" subtitle="Saudi-first scorecard." />
      <BrandCard title="Readiness" source={readiness.source}>
        <SummaryGrid metrics={readiness.data.metrics} />
      </BrandCard>
    </FounderShell>
  );
}
