import { FounderShell } from "../../components/founder-shell";
import { BrandCard } from "../../components/brand/brand-card";
import { MetricCard } from "../../components/brand/metric-card";
import { TrustBadge } from "../../components/brand/trust-badge";
import { getCEOSummary } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function CEOPage() {
  const res = await getCEOSummary();
  const d = res.data;
  return (
    <FounderShell title="CEO — Daily Operating Brief">
      <BrandCard
        title="Founder Daily Brief"
        subtitle="Intelligent deals. Real growth. Trust-gated execution."
        source={res.source}
      >
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))", gap: 12 }}>
          <MetricCard label="Pipeline Value (SAR)" value={(d.pipeline_value_sar || 0).toLocaleString()} />
          <MetricCard label="Cash Collected · 30d (SAR)" value={(d.cash_collected_30d_sar || 0).toLocaleString()} />
          <MetricCard label="Open Approvals" value={d.open_approvals ?? 0} />
          <MetricCard label="Trust Flags" value={(d as { trust_flags?: number }).trust_flags ?? 0} />
          <MetricCard label="Incidents Open" value={d.incidents_open ?? 0} />
        </div>
        <p style={{ color: "var(--dealix-soft-silver)", marginTop: 16 }}>
          {res.source === "fallback"
            ? "Backend not reachable — showing zeros until the private ops runtime worker writes its first scorecard."
            : "Live from the Dealix internal runtime."}
        </p>
        <TrustBadge approved={false} label="No external action without approval" />
      </BrandCard>
    </FounderShell>
  );
}
