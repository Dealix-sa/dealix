import { PageShell } from "../../components/brand/page-shell";
import { SectionHeading } from "../../components/brand/section-heading";
import { BrandCard } from "../../components/brand/brand-card";
import { MetricCard } from "../../components/brand/metric-card";

export default function MarketingPage() {
  return (
    <PageShell currentPath="/marketing">
      <SectionHeading
        eyebrow="Marketing"
        title="Content calendar. Founder-led drafts."
        description="A single calendar drives every owned surface. Drafted by Dealix, approved by the founder."
      />
      <div className="dlx-grid dlx-grid-4">
        <MetricCard label="Calendar slots (7d)" value="—" source="fallback" />
        <MetricCard label="Drafts queued" value="—" source="fallback" />
        <MetricCard label="Voice blocks" value="—" source="fallback" />
        <MetricCard label="Published" value="—" source="fallback" />
      </div>
      <BrandCard title="Surfaces">
        <ul className="dlx-muted" style={{ margin: 0, paddingInlineStart: 18, lineHeight: 1.8 }}>
          <li>Founder LinkedIn — 2–4 / week</li>
          <li>Sector pulse — 1 / sector / month</li>
          <li>Case studies — 1 per consented proof</li>
          <li>Landing pages — quarterly review</li>
        </ul>
      </BrandCard>
    </PageShell>
  );
}
