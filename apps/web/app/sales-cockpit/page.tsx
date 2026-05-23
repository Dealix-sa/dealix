import { PageShell } from "../../components/brand/page-shell";
import { SectionHeading } from "../../components/brand/section-heading";
import { BrandCard } from "../../components/brand/brand-card";
import { MetricCard } from "../../components/brand/metric-card";
import { StatusBadge } from "../../components/brand/status-badge";

export default function SalesCockpitPage() {
  return (
    <PageShell currentPath="/sales-cockpit">
      <SectionHeading
        eyebrow="Sales"
        title="Pipeline by tier. Next approval first."
        description="The cockpit ranks accounts by composite score and surfaces the next draft that needs your sign-off."
      />
      <div className="dlx-grid dlx-grid-4">
        <MetricCard label="Tier A" value="—" hint="≥ 80 composite" source="fallback" />
        <MetricCard label="Tier B" value="—" hint="60–79" source="fallback" />
        <MetricCard label="Tier C" value="—" hint="40–59" source="fallback" />
        <MetricCard label="Stale > 60d" value="—" hint="needs refresh" source="fallback" />
      </div>
      <BrandCard title="Next approval" action={<StatusBadge label="awaiting you" tone="accent" />}>
        <p className="dlx-muted" style={{ margin: 0 }}>
          No live drafts available offline. When the API is reachable, the highest-priority draft will
          render here, with a one-click approve / dismiss / edit.
        </p>
      </BrandCard>
    </PageShell>
  );
}
