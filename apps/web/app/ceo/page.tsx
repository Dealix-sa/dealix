import { PageShell } from "../../components/brand/page-shell";
import { SectionHeading } from "../../components/brand/section-heading";
import { BrandCard } from "../../components/brand/brand-card";
import { MetricCard } from "../../components/brand/metric-card";
import { StatusBadge } from "../../components/brand/status-badge";

export default function CeoPage() {
  return (
    <PageShell currentPath="/ceo">
      <SectionHeading
        eyebrow="CEO"
        title="One screen, one decision."
        description="Weekly KPI tree, one prioritised gap, one proposed experiment. Drafted by Dealix, approved by you."
      />
      <div className="dlx-grid dlx-grid-4">
        <MetricCard label="Tier-A accounts" value="—" hint="weekly refresh" source="fallback" />
        <MetricCard label="Drafts queued" value="—" hint="across all channels" source="fallback" />
        <MetricCard label="Approvals (7d)" value="—" hint="founder decisions" source="fallback" />
        <MetricCard label="CAR (qtr)" value="—" hint="compounding approved revenue" source="fallback" />
      </div>
      <BrandCard
        title="This week's prioritised gap"
        subtitle="Surfaced by the performance analyst — never auto-acted."
        action={<StatusBadge label="needs founder review" tone="warning" />}
      >
        <p className="dlx-muted" style={{ margin: 0 }}>
          Connect the Dealix API to populate this card. The console renders without an API on purpose
          so the founder can audit the shell at any time.
        </p>
      </BrandCard>
    </PageShell>
  );
}
