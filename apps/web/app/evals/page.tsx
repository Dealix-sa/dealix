import { PageShell } from "../../components/brand/page-shell";
import { SectionHeading } from "../../components/brand/section-heading";
import { BrandCard } from "../../components/brand/brand-card";
import { MetricCard } from "../../components/brand/metric-card";

export default function EvalsPage() {
  return (
    <PageShell currentPath="/evals">
      <SectionHeading
        eyebrow="Evals"
        title="Agent eval suites + red-team gate."
        description="Every agent passes its eval suite before deploy. Every release passes the red-team gate."
      />
      <div className="dlx-grid dlx-grid-4">
        <MetricCard label="Agents registered" value="12" hint="see docs/ai/AGENT_REGISTRY.md" />
        <MetricCard label="Eval suites" value="—" source="fallback" />
        <MetricCard label="Red-team pass" value="—" source="fallback" />
        <MetricCard label="Failed deploys" value="—" source="fallback" />
      </div>
      <BrandCard title="Red-team probes">
        <ul className="dlx-muted" style={{ margin: 0, paddingInlineStart: 18, lineHeight: 1.8 }}>
          <li>Prompt-injection via tool inputs</li>
          <li>Excessive-agency probes</li>
          <li>Data exfiltration probes</li>
          <li>Cross-tenant probes</li>
          <li>Jailbreak / system-prompt overrides</li>
        </ul>
      </BrandCard>
    </PageShell>
  );
}
