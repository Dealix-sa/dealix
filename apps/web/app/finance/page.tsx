import { PageShell } from "../../components/brand/page-shell";
import { SectionHeading } from "../../components/brand/section-heading";
import { BrandCard } from "../../components/brand/brand-card";
import { MetricCard } from "../../components/brand/metric-card";

export default function FinancePage() {
  return (
    <PageShell currentPath="/finance">
      <SectionHeading
        eyebrow="Finance"
        title="ZATCA, payments, retainers."
        description="No auto-charge, no auto-discount. Every invoice is signed off and ZATCA-compliant."
      />
      <div className="dlx-grid dlx-grid-4">
        <MetricCard label="Invoiced (qtr)" value="—" hint="ZATCA Phase 2" source="fallback" />
        <MetricCard label="Captured (qtr)" value="—" hint="post-clearance" source="fallback" />
        <MetricCard label="Days sign → captured" value="—" hint="median" source="fallback" />
        <MetricCard label="Disputes" value="—" hint="under investigation" source="fallback" />
      </div>
      <BrandCard title="Pricing guardrails">
        <p className="dlx-muted" style={{ margin: 0 }}>
          Bands live in <code>docs/product/PRICING_GUARDRAILS.md</code>. Exact numbers in
          <code> data/private_ops_seed/product/pricing.yaml</code> (not in repo).
        </p>
      </BrandCard>
    </PageShell>
  );
}
