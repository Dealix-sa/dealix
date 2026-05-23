import { PageShell } from "../../components/brand/page-shell";
import { SectionHeading } from "../../components/brand/section-heading";
import { BrandCard } from "../../components/brand/brand-card";
import { MetricCard } from "../../components/brand/metric-card";

export default function AuditPage() {
  return (
    <PageShell currentPath="/audit">
      <SectionHeading
        eyebrow="Audit"
        title="Every approval is searchable evidence."
        description="The ledger records who approved what, when, and against which draft / artifact / run."
      />
      <div className="dlx-grid dlx-grid-4">
        <MetricCard label="Approvals (7d)" value="—" source="fallback" />
        <MetricCard label="Blocks (7d)" value="—" source="fallback" />
        <MetricCard label="Agent runs (24h)" value="—" source="fallback" />
        <MetricCard label="Tenant scope" value="default" source="fallback" />
      </div>
      <BrandCard title="Ledger paths">
        <ul style={{ margin: 0, paddingInlineStart: 18, lineHeight: 1.8, fontFamily: "monospace", fontSize: 13 }} className="dlx-muted">
          <li>governance/approvals.csv</li>
          <li>audit/agents/&lt;agent_id&gt;.jsonl</li>
          <li>audit/distribution_*_runs.jsonl</li>
          <li>audit/evals/</li>
          <li>audit/red_team/</li>
        </ul>
      </BrandCard>
    </PageShell>
  );
}
