import { FounderShell } from "../../components/founder-shell";
import { BrandCard } from "../../components/brand/brand-card";
import { MetricCard } from "../../components/brand/metric-card";
import { SectionHeading } from "../../components/brand/section-heading";
import { CtaButton } from "../../components/brand/cta-button";
import { StatusBadge } from "../../components/brand/status-badge";
import { semanticColors, spacing } from "../../lib/brand-tokens";

export default function FounderHomePage() {
  return (
    <FounderShell active="CEO">
      <SectionHeading
        eyebrow="Founder Console"
        title="Today's revenue picture"
        subtitle="Approval queue, active sprints, proof artefacts, and kill switches in one place."
      />

      <section
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
          gap: spacing[4]
        }}
      >
        <MetricCard
          label="Approvals pending"
          value="0"
          hint="Drafts awaiting founder decision."
        />
        <MetricCard
          label="Sprints active"
          value="—"
          hint="Time-boxed engagements in flight."
        />
        <MetricCard
          label="Proof packs"
          value="—"
          hint="Bilingual artefacts ready to share."
        />
        <MetricCard
          label="Worker health"
          value="OK"
          deltaDirection="up"
          hint="No degraded agents."
        />
      </section>

      <section
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))",
          gap: spacing[4]
        }}
      >
        <BrandCard eyebrow="Trust" title="Nothing leaves without you" accent>
          <p style={{ marginTop: 0 }}>
            All outbound drafts (email, LinkedIn, proposal) require explicit founder
            approval before they can be sent.
          </p>
          <div style={{ display: "flex", gap: spacing[3], flexWrap: "wrap" }}>
            <StatusBadge kind="ok">Approval queue: empty</StatusBadge>
            <StatusBadge kind="info">Kill switch: armed</StatusBadge>
          </div>
        </BrandCard>

        <BrandCard eyebrow="Growth" title="Revenue Sprint pipeline">
          <p style={{ marginTop: 0 }}>
            View the 7-day Revenue Sprints in motion and the next prospect ready to start.
          </p>
          <div style={{ display: "flex", gap: spacing[3] }}>
            <CtaButton href="/founder/sales" variant="ghost">Open Sales</CtaButton>
            <CtaButton href="/founder/delivery" variant="ghost">Open Delivery</CtaButton>
          </div>
        </BrandCard>

        <BrandCard eyebrow="Proof" title="Last proof artefacts">
          <p style={{ marginTop: 0, color: semanticColors.textSecondary }}>
            No proof packs published yet. Run a sprint to assemble the first bilingual pack.
          </p>
          <CtaButton href="/founder/proof" variant="ghost">Open Proof OS</CtaButton>
        </BrandCard>
      </section>

      <section>
        <SectionHeading
          eyebrow="Distribution"
          title="Trust-gated machines"
          subtitle="Each machine prepares, scores, drafts, or queues. None of them sends anything externally without founder approval."
        />
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))",
            gap: spacing[4]
          }}
        >
          <BrandCard title="Outreach Draft Machine">
            Drafts personalised outbound; queues for review. Never sends.
          </BrandCard>
          <BrandCard title="Proposal Factory Machine">
            Renders bilingual proposals from approved templates.
          </BrandCard>
          <BrandCard title="Proof-to-Demand Machine">
            Turns delivered work into proof artefacts and warm-list candidates.
          </BrandCard>
        </div>
      </section>
    </FounderShell>
  );
}
