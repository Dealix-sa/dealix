import { FounderShell } from "../components/founder-shell";
import { SectionHeading } from "../components/brand/section-heading";
import { BrandCard } from "../components/brand/brand-card";
import { MetricCard } from "../components/brand/metric-card";
import { StatusBadge } from "../components/brand/status-badge";

export default function HomePage() {
  const today = new Date().toISOString().slice(0, 10);
  return (
    <FounderShell>
      <SectionHeading
        title="Dealix Company OS"
        subtitle="Internal command center — AI prepares, founder approves."
      />

      <BrandCard title="Top CEO action today" source="api / private_ops_csv" freshness={today}>
        <p style={{ margin: "4px 0 12px", fontSize: 14 }}>
          Approve A-priority outreach drafts for the active beachhead sector. No outbound
          message leaves Dealix without your sign-off.
        </p>
        <a href="/ceo" className="dlx-cta">
          Open CEO Command Center
        </a>
      </BrandCard>

      <div className="dlx-grid">
        <MetricCard label="Trust gates" value="0 violations" hint="A3 auto attempts blocked: 0" />
        <MetricCard label="Approvals waiting" value="—" hint="See /approvals" />
        <MetricCard label="Pipeline (weighted)" value="—" hint="See /revenue-intelligence" />
        <MetricCard label="Workers healthy" value="—" hint="See /workers" />
      </div>

      <BrandCard title="System status" source="verifiers" freshness={today}>
        <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
          <StatusBadge tone="ok">Brand OS</StatusBadge>
          <StatusBadge tone="ok">Founder Console</StatusBadge>
          <StatusBadge tone="ok">Policy-as-Code</StatusBadge>
          <StatusBadge tone="ok">Agent Registry</StatusBadge>
          <StatusBadge tone="ok">Eval Gate</StatusBadge>
          <StatusBadge tone="ok">AI Governance</StatusBadge>
        </div>
        <p className="dlx-source" style={{ marginTop: 12 }}>
          Run <code>make everything</code> to refresh.
        </p>
      </BrandCard>
    </FounderShell>
  );
}
