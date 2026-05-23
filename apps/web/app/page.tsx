import { ConsoleShell, FOUNDER_CONSOLE_NAV } from "../components/shell/ConsoleShell";
import { BrandCard } from "../components/brand/BrandCard";
import { SectionHeading } from "../components/brand/SectionHeading";
import { MetricCard } from "../components/brand/MetricCard";
import { StatusBadge } from "../components/brand/StatusBadge";
import { DataSourceTag } from "../components/brand/DataSourceTag";

export default function HomePage() {
  return (
    <ConsoleShell active="/">
      <BrandCard
        title="Dealix Founder Console"
        subtitle="Intelligent Deals. Real Growth."
        actions={<DataSourceTag source="fallback" />}
      >
        <p style={{ color: "var(--dx-text-secondary)", marginTop: 0 }}>
          Saudi B2B Revenue Operating System. Trust-gated AI execution.
          Founder-approved growth. All external actions are draft-queued and
          require approval — automation never sends, never publishes, never
          commits price, contract, or payment terms on its own.
        </p>
      </BrandCard>

      <SectionHeading title="Operating Snapshot" meta="fallback data" />
      <div className="dx-grid dx-grid--cols-3">
        <MetricCard label="Approval queue" value="—" helper="A2 items waiting" />
        <MetricCard label="Workers fresh" value="—" helper="last 24h" />
        <MetricCard label="Trust flags" value="—" helper="open / total" />
      </div>

      <SectionHeading title="Console Map" />
      <div className="dx-grid dx-grid--cols-3">
        {Array.from(new Set(FOUNDER_CONSOLE_NAV.map((n) => n.group ?? ""))).map(
          (group) => (
            <BrandCard key={group} title={group} subtitle={`${group} surfaces`}>
              <ul style={{ margin: 0, paddingInlineStart: 20, color: "var(--dx-text-secondary)" }}>
                {FOUNDER_CONSOLE_NAV.filter((n) => n.group === group).map((n) => (
                  <li key={n.href} style={{ marginBottom: 6 }}>
                    <a href={n.href}>{n.label}</a>
                  </li>
                ))}
              </ul>
            </BrandCard>
          )
        )}
      </div>

      <SectionHeading title="Trust Posture" />
      <div className="dx-grid dx-grid--cols-3">
        <BrandCard title="Approval Classes">
          <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
            <StatusBadge tone="a1">A1 auto-safe</StatusBadge>
            <StatusBadge tone="a2">A2 founder approval</StatusBadge>
            <StatusBadge tone="a3">A3 escalation only</StatusBadge>
          </div>
        </BrandCard>
        <BrandCard title="Non-negotiables">
          <ul style={{ margin: 0, paddingInlineStart: 20, color: "var(--dx-text-secondary)" }}>
            <li>No external sending without approval</li>
            <li>No proof published without approval</li>
            <li>No guaranteed revenue/sales claims</li>
            <li>No price/contract/payment commitments</li>
          </ul>
        </BrandCard>
        <BrandCard title="Brand Pillars">
          <ul style={{ margin: 0, paddingInlineStart: 20, color: "var(--dx-text-secondary)" }}>
            <li>Built on Trust</li>
            <li>Driven by Growth</li>
            <li>Closing Deals</li>
            <li>Focused on Results</li>
            <li>Global Mindset, Local Impact</li>
          </ul>
        </BrandCard>
      </div>
    </ConsoleShell>
  );
}
