import { FounderShell } from "../../components/founder-shell";
import { BrandCard } from "../../components/brand/brand-card";
import { MetricCard } from "../../components/brand/metric-card";
import { getFinanceSummary } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function FinancePage() {
  const res = await getFinanceSummary();
  const d = res.data;
  return (
    <FounderShell title="Finance">
      <BrandCard title="Finance summary" subtitle="Cash, ARR estimate, AI unit economics" source={res.source}>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))", gap: 12 }}>
          <MetricCard label="Cash collected · 30d (SAR)" value={(d.cash_collected_30d_sar || 0).toLocaleString()} />
          <MetricCard label="Pipeline value (SAR)" value={(d.pipeline_value_sar || 0).toLocaleString()} />
          <MetricCard label="ARR estimate (SAR)" value={(d.arr_estimate_sar || 0).toLocaleString()} />
          <MetricCard label="Invoices outstanding" value={d.invoices_outstanding ?? 0} />
          <MetricCard label="AI cost · 30d (USD)" value={(d.ai_cost_30d_usd || 0).toLocaleString()} />
          <MetricCard label="Margin health" value={String(d.margin_health ?? "unknown")} />
        </div>
      </BrandCard>
    </FounderShell>
  );
}
