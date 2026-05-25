import { DealixLogo } from "../components/brand/dealix-logo";
import { BrandCard } from "../components/brand/brand-card";
import { MetricCard } from "../components/brand/metric-card";
import { CtaButton } from "../components/brand/cta-button";
import { SectionHeading } from "../components/brand/section-heading";
import { StatusBadge } from "../components/brand/status-badge";
import { DEALIX_BRAND, semanticColors, spacing } from "../lib/brand-tokens";

const surfaces = [
  { href: "/founder", label: "Founder Console" },
  { href: "/control-plane", label: "Control Plane" },
  { href: "/agents", label: "Agents" },
  { href: "/approvals", label: "Approvals" },
  { href: "/safety", label: "Safety" },
  { href: "/sandbox", label: "Sandbox" },
  { href: "/value-engine", label: "Value Engine" },
  { href: "/self-evolving", label: "Self-Evolving" }
];

export default function HomePage() {
  return (
    <main
      style={{
        minHeight: "100vh",
        background: semanticColors.backgroundPrimary,
        color: semanticColors.textPrimary,
        padding: spacing[8],
        display: "grid",
        gap: spacing[8],
        alignContent: "start"
      }}
    >
      <header
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          gap: spacing[6]
        }}
      >
        <DealixLogo variant="lockup" withTagline />
        <StatusBadge kind="ok">Human-approved workflows</StatusBadge>
      </header>

      <section
        style={{
          display: "grid",
          gridTemplateColumns: "1fr",
          gap: spacing[6],
          maxWidth: 980
        }}
      >
        <SectionHeading
          eyebrow="Saudi B2B Revenue Intelligence"
          title={DEALIX_BRAND.tagline}
          subtitle="Trust-gated AI assistance for sales, delivery, and revenue. Every external action is founder-approved before it leaves the system."
        />
        <div style={{ display: "flex", gap: spacing[3] }}>
          <CtaButton href="/founder">Open Founder Console</CtaButton>
          <CtaButton href="/control-plane" variant="ghost">View Control Plane</CtaButton>
        </div>
      </section>

      <section
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
          gap: spacing[4]
        }}
      >
        <MetricCard
          label="Approval queue"
          value="0"
          delta="trust-gated"
          deltaDirection="flat"
          hint="No drafts pending review."
        />
        <MetricCard
          label="Active sprints"
          value="—"
          hint="Founder-approved engagements."
        />
        <MetricCard
          label="Proof packs"
          value="—"
          hint="Bilingual artefacts ready to send."
        />
        <MetricCard
          label="Kill switch"
          value="OK"
          deltaDirection="flat"
          hint="One click halts all outbound."
        />
      </section>

      <section
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))",
          gap: spacing[4]
        }}
      >
        {surfaces.map((s) => (
          <BrandCard key={s.href} eyebrow="Surface" title={s.label}>
            <a
              href={s.href}
              style={{
                color: semanticColors.accentPrimary,
                textDecoration: "none",
                fontWeight: 600
              }}
            >
              {s.href} →
            </a>
          </BrandCard>
        ))}
      </section>

      <footer
        style={{
          marginTop: spacing[8],
          color: semanticColors.textSecondary,
          fontSize: 12,
          lineHeight: 1.6
        }}
      >
        {DEALIX_BRAND.pillars.join("  ·  ")}
        <br />
        AI-assisted. Trust-gated. Founder-approved. No uncontrolled outbound automation.
      </footer>
    </main>
  );
}
