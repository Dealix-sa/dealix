import { FounderShell } from "../../components/founder-shell";
import { BrandCard } from "../../components/brand/brand-card";
import { MetricCard } from "../../components/brand/metric-card";
import { getCustomerSuccessSummary } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function CustomerSuccessPage() {
  const res = await getCustomerSuccessSummary();
  const d = res.data;
  return (
    <FounderShell title="Customer Success">
      <BrandCard title="Customer success snapshot" source={res.source}>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))", gap: 12 }}>
          <MetricCard label="Active clients" value={d.clients_active} />
          <MetricCard label="At risk" value={d.clients_at_risk} />
          <MetricCard label="Referrals open" value={d.referrals_open} />
          <MetricCard label="NPS" value={String(d.nps ?? "—")} />
        </div>
      </BrandCard>
    </FounderShell>
  );
}
