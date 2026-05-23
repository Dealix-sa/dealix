import { FounderShell } from "../../components/founder-shell";
import { BrandCard } from "../../components/brand/brand-card";
import { SectionHeading } from "../../components/brand/section-heading";
import { SummaryGrid } from "../../components/brand/summary-grid";
import { getSecurityStatus } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function SecurityPage() {
  const security = await getSecurityStatus();
  return (
    <FounderShell active="/security">
      <SectionHeading title="Security" subtitle="PDPL, incidents, posture." />
      <BrandCard title="Posture" source={security.source}>
        <SummaryGrid metrics={security.data.metrics} />
      </BrandCard>
    </FounderShell>
  );
}
