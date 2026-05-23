import { FounderShell } from "../../components/founder-shell";
import { BrandCard } from "../../components/brand/brand-card";
import { MetricCard } from "../../components/brand/metric-card";
import { getSecurityStatus } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function SecurityPage() {
  const res = await getSecurityStatus();
  const d = res.data;
  return (
    <FounderShell title="Security">
      <BrandCard title="Security posture" subtitle="Secrets, dependencies, PDPL" source={res.source}>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))", gap: 12 }}>
          <MetricCard label="Secrets scan" value={String(d.secrets_scan ?? "unknown")} />
          <MetricCard label="Dependency scan" value={String(d.dependency_scan ?? "unknown")} />
          <MetricCard label="PDPL review" value={String(d.pdpl_review ?? "unknown")} />
          <MetricCard label="Incidents open" value={String(d.incident_open ?? 0)} />
        </div>
      </BrandCard>
    </FounderShell>
  );
}
