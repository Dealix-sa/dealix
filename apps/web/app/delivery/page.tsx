import { PageShell } from "../../components/brand/page-shell";
import { SectionHeading } from "../../components/brand/section-heading";
import { BrandCard } from "../../components/brand/brand-card";
import { MetricCard } from "../../components/brand/metric-card";

export default function DeliveryPage() {
  return (
    <PageShell currentPath="/delivery">
      <SectionHeading
        eyebrow="Delivery"
        title="Every engagement, one Day-1 pack."
        description="Bilingual welcome, roles, cadence, PDPL note. Every artifact passes brand and trust gates before customer release."
      />
      <div className="dlx-grid dlx-grid-4">
        <MetricCard label="Active engagements" value="—" source="fallback" />
        <MetricCard label="On-time rate" value="—" source="fallback" />
        <MetricCard label="Open issues" value="—" source="fallback" />
        <MetricCard label="Last-touch recency" value="—" source="fallback" />
      </div>
      <BrandCard title="Delivery contract reference">
        <p className="dlx-muted" style={{ margin: 0 }}>
          See <code>docs/delivery/DELIVERY_QA_OS.md</code> for the canonical engagement shape.
        </p>
      </BrandCard>
    </PageShell>
  );
}
