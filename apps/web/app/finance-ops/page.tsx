import { FounderShell } from "../../components/founder-shell";
import { BrandCard } from "../../components/brand/brand-card";
import { MetricCard } from "../../components/brand/metric-card";
import { getFinanceOpsSummary } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function FinanceOpsPage() {
  const res = await getFinanceOpsSummary();
  const d = res.data;
  return (
    <FounderShell title="Finance Ops">
      <BrandCard title="Invoice & unit economics" source={res.source}>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))", gap: 12 }}>
          <MetricCard label="Invoices open" value={d.invoices_open} />
          <MetricCard label="Overdue" value={d.invoices_overdue} />
          <MetricCard label="Cash in · 30d (SAR)" value={(d.cash_in_30d_sar || 0).toLocaleString()} />
          <MetricCard label="AI cost / deal (USD)" value={String(d.ai_unit_cost_per_deal_usd ?? "—")} />
        </div>
      </BrandCard>
    </FounderShell>
  );
}
