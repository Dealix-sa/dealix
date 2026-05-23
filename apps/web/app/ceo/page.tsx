import { FounderShell } from "../../components/founder-shell";
import { BrandCard } from "../../components/brand/brand-card";
import { SectionHeading } from "../../components/brand/section-heading";
import { SummaryGrid } from "../../components/brand/summary-grid";
import { getCEOSummary } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function CEOPage() {
  const ceo = await getCEOSummary();
  return (
    <FounderShell active="/ceo">
      <SectionHeading title="CEO Cockpit" subtitle="Pipeline, approvals, trust, runway." />
      <BrandCard title="Today" source={ceo.source}>
        <SummaryGrid metrics={ceo.data.metrics} />
        {ceo.data.highlights && ceo.data.highlights.length > 0 ? (
          <ul className="dealix-list" style={{ marginTop: 16 }}>
            {ceo.data.highlights.map((h) => (
              <li key={h}>{h}</li>
            ))}
          </ul>
        ) : null}
      </BrandCard>
    </FounderShell>
  );
}
