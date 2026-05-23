import { PageShell } from "../../components/brand/page-shell";
import { SectionHeading } from "../../components/brand/section-heading";
import { BrandCard } from "../../components/brand/brand-card";
import { MetricCard } from "../../components/brand/metric-card";

export default function SovereignPage() {
  return (
    <PageShell currentPath="/sovereign">
      <SectionHeading
        eyebrow="Sovereign"
        title="Data sovereignty + tenants."
        description="Saudi data stays in Saudi-aligned regions. Tenant isolation by default. PDPL boundaries enforced at the data layer."
      />
      <div className="dlx-grid dlx-grid-4">
        <MetricCard label="Tenants" value="—" source="fallback" />
        <MetricCard label="PDPL boundaries" value="enforced" />
        <MetricCard label="Cross-tenant probes" value="0 success" />
        <MetricCard label="Data region" value="ksa-aligned" />
      </div>
      <BrandCard title="Sovereignty discipline">
        <ul className="dlx-muted" style={{ margin: 0, paddingInlineStart: 18, lineHeight: 1.8 }}>
          <li>Tenant isolation: separate schemas, separate queues, separate ledgers.</li>
          <li>Cross-tenant read = block.</li>
          <li>Customer data stays where the customer agreed it would stay.</li>
        </ul>
      </BrandCard>
    </PageShell>
  );
}
