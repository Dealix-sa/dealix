import { PageShell } from "../../components/brand/page-shell";
import { SectionHeading } from "../../components/brand/section-heading";
import { BrandCard } from "../../components/brand/brand-card";
import { StatusBadge } from "../../components/brand/status-badge";

const SWITCHES = [
  "DEALIX_DISTRIBUTION_OUTBOUND_ENABLED",
  "DEALIX_DISTRIBUTION_LINKEDIN_ENABLED",
  "DEALIX_DISTRIBUTION_EMAIL_ENABLED",
  "DEALIX_DISTRIBUTION_FOLLOW_UP_ENABLED",
  "DEALIX_AGENT_BRAND_GUARDIAN_ENABLED",
  "DEALIX_AGENT_DISTRIBUTION_OPERATOR_ENABLED",
  "DEALIX_AGENT_GROWTH_STRATEGIST_ENABLED",
  "DEALIX_AGENT_CONTENT_STRATEGIST_ENABLED",
  "DEALIX_AGENT_OFFER_ARCHITECT_ENABLED",
  "DEALIX_AGENT_PERFORMANCE_ANALYST_ENABLED",
];

export default function SecurityPage() {
  return (
    <PageShell currentPath="/security">
      <SectionHeading
        eyebrow="Security"
        title="Kill switches. Policy-as-code."
        description="Trust guardian cannot be disabled by other agents. Founder owns the master switch."
        action={<StatusBadge label="armed" tone="accent" />}
      />
      <BrandCard title="Kill switches">
        <ul style={{ margin: 0, paddingInlineStart: 18, lineHeight: 1.9, fontFamily: "monospace", fontSize: 13 }} className="dlx-muted">
          {SWITCHES.map((s) => <li key={s}>{s}</li>)}
        </ul>
      </BrandCard>
      <BrandCard title="Hard refusals">
        <ul style={{ margin: 0, paddingInlineStart: 18, lineHeight: 1.8 }} className="dlx-muted">
          <li>No external send without per-message approval.</li>
          <li>No commitment on pricing, contract, refund, payment.</li>
          <li>No guaranteed-revenue claims.</li>
          <li>No publish without consent.</li>
        </ul>
      </BrandCard>
    </PageShell>
  );
}
