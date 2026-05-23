import { PageShell } from "../../components/brand/page-shell";
import { SectionHeading } from "../../components/brand/section-heading";
import { BrandCard } from "../../components/brand/brand-card";
import { MetricCard } from "../../components/brand/metric-card";

const SECTORS = [
  "ERP / CRM implementers",
  "Cybersecurity",
  "B2B agencies",
  "Logistics / industrial services",
  "Consulting / digital transformation",
  "SaaS / software",
  "Enterprise services",
  "Saudi high-ticket B2B providers",
];

export default function GrowthPage() {
  return (
    <PageShell currentPath="/growth">
      <SectionHeading
        eyebrow="Growth"
        title="Sector. ICP. Account scoring."
        description="The intelligence layer that feeds the Distribution War Machine. Recommendations only — never auto-targeting."
      />
      <div className="dlx-grid dlx-grid-4">
        <MetricCard label="Sectors tracked" value={SECTORS.length} />
        <MetricCard label="Segments" value="—" source="fallback" />
        <MetricCard label="Tier-A accounts" value="—" source="fallback" />
        <MetricCard label="Trigger events (7d)" value="—" source="fallback" />
      </div>
      <BrandCard title="Initial target sectors">
        <ol style={{ margin: 0, paddingInlineStart: 22, lineHeight: 1.8 }} className="dlx-muted">
          {SECTORS.map((s) => <li key={s}>{s}</li>)}
        </ol>
      </BrandCard>
    </PageShell>
  );
}
