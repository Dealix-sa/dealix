import { PageShell } from "../../components/brand/page-shell";
import { SectionHeading } from "../../components/brand/section-heading";
import { BrandCard } from "../../components/brand/brand-card";
import { MetricCard } from "../../components/brand/metric-card";
import { StatusBadge } from "../../components/brand/status-badge";

export default function ProofPage() {
  return (
    <PageShell currentPath="/proof">
      <SectionHeading
        eyebrow="Proof"
        title="Consented case studies only."
        description="No artifact is published without a customer consent row and a founder approval."
        action={<StatusBadge label="consent-required" tone="warning" />}
      />
      <div className="dlx-grid dlx-grid-4">
        <MetricCard label="Approved proofs" value="—" source="fallback" />
        <MetricCard label="Expiring (30d)" value="—" source="fallback" />
        <MetricCard label="Pending consent" value="—" source="fallback" />
        <MetricCard label="Withdrawn" value="—" source="fallback" />
      </div>
      <BrandCard title="Proof discipline">
        <ul className="dlx-muted" style={{ margin: 0, paddingInlineStart: 18, lineHeight: 1.8 }}>
          <li>Every proof row carries a consent_id and consent_expires_at.</li>
          <li>Withdrawn / expired consents block any pending share drafts.</li>
          <li>Composite "results" across unnamed customers are banned.</li>
        </ul>
      </BrandCard>
    </PageShell>
  );
}
