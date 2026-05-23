import { PageShell } from "../../components/brand/page-shell";
import { SectionHeading } from "../../components/brand/section-heading";
import { BrandCard } from "../../components/brand/brand-card";
import { MetricCard } from "../../components/brand/metric-card";
import { StatusBadge } from "../../components/brand/status-badge";

export default function TrustPage() {
  return (
    <PageShell currentPath="/trust">
      <SectionHeading
        eyebrow="Trust"
        title="Policy, consent, audit posture."
        description="The trust gate that sits between every agent and any external action. Cannot be disabled by other agents."
        action={<StatusBadge label="active" tone="accent" />}
      />
      <div className="dlx-grid dlx-grid-4">
        <MetricCard label="Blocks (7d)" value="—" hint="trust_guardian" source="fallback" />
        <MetricCard label="PDPL opt-outs" value="—" hint="enforced globally" source="fallback" />
        <MetricCard label="ZATCA accept" value="—" hint="target 100 %" source="fallback" />
        <MetricCard label="Consents active" value="—" hint="proof + outbound" source="fallback" />
      </div>
      <BrandCard title="Trust gate components">
        <ul style={{ margin: 0, paddingInlineStart: 18, lineHeight: 1.8 }} className="dlx-muted">
          <li>Consent registry — opt-in / opt-out / expiry</li>
          <li>Provenance source check — every record carries `source`, `collected_at`, `allowed_use`</li>
          <li>PDPL enforcement — every queue rejects opted-out targets</li>
          <li>ZATCA validation — every invoice fully populates buyer + seller fields</li>
          <li>Voice / brand check — drafts must pass the brand_guardian</li>
          <li>Kill-switch ledger — every kill-switch flip is audited</li>
        </ul>
      </BrandCard>
    </PageShell>
  );
}
