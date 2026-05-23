import { PageShell } from "../../components/brand/page-shell";
import { SectionHeading } from "../../components/brand/section-heading";
import { BrandCard } from "../../components/brand/brand-card";
import { MetricCard } from "../../components/brand/metric-card";

export default function RetentionPage() {
  return (
    <PageShell currentPath="/retention">
      <SectionHeading
        eyebrow="Retention"
        title="Health + renewal cycles."
        description="Daily health roll-up. Weekly retention review. Monthly business review. Renewal at 60 days out."
      />
      <div className="dlx-grid dlx-grid-4">
        <MetricCard label="Logo retention" value="—" source="fallback" />
        <MetricCard label="Net retention" value="—" source="fallback" />
        <MetricCard label="Referrals (qtr)" value="—" source="fallback" />
        <MetricCard label="MBRs due" value="—" source="fallback" />
      </div>
      <BrandCard title="Retention guardrails">
        <ul className="dlx-muted" style={{ margin: 0, paddingInlineStart: 18, lineHeight: 1.8 }}>
          <li>Referral asks only when health is green ≥ 21 days.</li>
          <li>One referral per customer per 60 days.</li>
          <li>Drafted asks; the founder sends.</li>
        </ul>
      </BrandCard>
    </PageShell>
  );
}
