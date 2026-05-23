import { FounderShell } from "../../components/founder-shell";
import { BrandCard } from "../../components/brand/brand-card";
import { MetricCard } from "../../components/brand/metric-card";
import { getDataPlatformSummary } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function DataPage() {
  const res = await getDataPlatformSummary();
  const d = res.data;
  return (
    <FounderShell title="Data Platform">
      <BrandCard title="Data platform health" source={res.source}>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))", gap: 12 }}>
          <MetricCard label="Primary store" value={String(d.primary_store ?? "postgres")} />
          <MetricCard label="DQ score" value={String(d.dq_score ?? "—")} />
          <MetricCard label="Failed pipelines (24h)" value={d.pipelines_failed_24h} />
          <MetricCard label="Last DQ run" value={String(d.last_dq_run ?? "—")} />
        </div>
      </BrandCard>
    </FounderShell>
  );
}
