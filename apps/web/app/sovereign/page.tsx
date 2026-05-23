import { FounderShell } from "../../components/founder-shell";
import { BrandCard } from "../../components/brand/brand-card";
import { MetricCard } from "../../components/brand/metric-card";
import { getSovereignReadiness } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function SovereignPage() {
  const res = await getSovereignReadiness();
  const d = res.data;
  return (
    <FounderShell title="Sovereign Readiness">
      <BrandCard
        title="Saudi sovereign operating stack"
        subtitle="Data residency, PDPL, NCA alignment, Arabic quality"
        source={res.source}
      >
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))", gap: 12 }}>
          <MetricCard label="Data residency" value={String(d.saudi_data_residency ?? "unknown")} />
          <MetricCard label="PDPL alignment" value={String(d.pdpl_alignment ?? "unknown")} />
          <MetricCard label="NCA alignment" value={String(d.nca_alignment ?? "unknown")} />
          <MetricCard label="Arabic quality" value={String(d.arabic_quality ?? "unknown")} />
        </div>
      </BrandCard>
    </FounderShell>
  );
}
