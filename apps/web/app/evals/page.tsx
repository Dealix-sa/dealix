import { FounderShell } from "../../components/founder-shell";
import { BrandCard } from "../../components/brand/brand-card";
import { MetricCard } from "../../components/brand/metric-card";
import { getEvalStatus } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function EvalsPage() {
  const res = await getEvalStatus();
  return (
    <FounderShell title="Evals">
      <BrandCard title="Eval gate status" subtitle="Blocking suites must pass before agent outputs reach the founder." source={res.source}>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))", gap: 12 }}>
          <MetricCard label="Last run" value={String(res.data.last_run ?? "—")} />
          <MetricCard label="Pass rate" value={String(res.data.pass_rate ?? "—")} />
          <MetricCard label="Blocking failures" value={String(res.data.blocking_failures ?? 0)} />
        </div>
      </BrandCard>
    </FounderShell>
  );
}
