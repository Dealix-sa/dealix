import { BrandCard } from "../components/brand/brand-card";
import { MetricCard } from "../components/brand/metric-card";
import { SectionHeading } from "../components/brand/section-heading";
import { StatusBadge } from "../components/brand/status-badge";
import { CtaButton } from "../components/brand/cta-button";
import { brand } from "../lib/brand-tokens";

const PILLARS = [
  {
    eyebrow: "Built on Trust",
    title: "Approval gates by default",
    desc: "Every external action — outbound, payment, proof, deal commitment — is queued for founder approval and audited.",
  },
  {
    eyebrow: "Driven by Growth",
    title: "Every machine ladders to revenue",
    desc: "From lead intelligence to cash collection, each subsystem reports against the same KPI tree.",
  },
  {
    eyebrow: "Closing Deals",
    title: "Bias to cash collected",
    desc: "Forecasts only count payments captured. Pipeline theatrics are filtered at the source.",
  },
  {
    eyebrow: "Focused on Results",
    title: "Weekly learning loop",
    desc: "Every sector, message, offer and channel is scored, ranked and pruned weekly.",
  },
  {
    eyebrow: "Global Mindset, Local Impact",
    title: "Arabic-first, world-class engineering",
    desc: "Bilingual surfaces, KSA-aware ICP, and global engineering standards under one Operating System.",
  },
];

const SURFACES = [
  { href: "/ceo", label: "CEO Console", note: "Daily brief and top decisions." },
  { href: "/sales-cockpit", label: "Sales Cockpit", note: "Pipeline, drafts, follow-ups." },
  { href: "/distribution", label: "Distribution War Room", note: "Outbound, LinkedIn, ABM queues." },
  { href: "/approvals", label: "Approvals", note: "Trust-gated actions awaiting consent." },
  { href: "/trust", label: "Trust Center", note: "Audit, suppression, evals." },
  { href: "/finance", label: "Finance", note: "Payment capture, invoices, cash." },
  { href: "/delivery", label: "Delivery QA", note: "Sample, proposal, project QA." },
  { href: "/retention", label: "Retention", note: "Health, expansion, referrals." },
  { href: "/proof", label: "Proof", note: "Case studies under consent gate." },
  { href: "/product", label: "Product Ladder", note: "Five offers, pricing guardrails." },
  { href: "/marketing", label: "Marketing OS", note: "Content calendar and campaigns." },
  { href: "/growth", label: "Growth Strategist", note: "Sectors, ICP, accounts." },
  { href: "/workers", label: "Worker Orchestrator", note: "Jobs, queues, schedules." },
  { href: "/audit", label: "Audit Log", note: "Every event, every actor." },
  { href: "/evals", label: "Evals", note: "Agent quality and safety." },
  { href: "/control-plane", label: "Control Plane", note: "Tenants, flags, environments." },
  { href: "/security", label: "Security", note: "Policies, scans, incidents." },
  { href: "/sovereign", label: "Sovereign", note: "Saudi data residency posture." },
];

export default function HomePage() {
  return (
    <div className="dx-grid" style={{ gap: 32 }}>
      <section className="dx-card dx-card--elevated">
        <div style={{ display: "grid", gridTemplateColumns: "1.4fr 1fr", gap: 24, alignItems: "center" }}>
          <div>
            <div
              style={{
                color: "var(--dx-accent)",
                fontSize: "0.72rem",
                fontWeight: 700,
                letterSpacing: "0.24em",
                textTransform: "uppercase",
                marginBottom: 8,
              }}
            >
              Saudi B2B Revenue Operating System
            </div>
            <h1
              style={{
                margin: 0,
                fontSize: "2.5rem",
                lineHeight: 1.1,
                letterSpacing: "-0.01em",
                color: "var(--dx-text)",
              }}
            >
              {brand.tagline}
            </h1>
            <p className="dx-muted" style={{ marginTop: 12, maxWidth: 620 }}>
              {brand.positioning}
            </p>
            <div className="dx-row" style={{ marginTop: 16 }}>
              <CtaButton href="/ceo">Open CEO Console</CtaButton>
              <CtaButton href="/distribution" variant="ghost">Open Distribution</CtaButton>
              <CtaButton href="/trust" variant="ghost">Trust Center</CtaButton>
            </div>
          </div>
          <div className="dx-grid" style={{ gridTemplateColumns: "1fr 1fr", gap: 12 }}>
            <MetricCard label="Approvals queued" value="—" hint="awaiting founder consent" />
            <MetricCard label="Distribution drafts" value="—" hint="ready for review" />
            <MetricCard label="Cash captured (week)" value="—" hint="from confirmed payments" />
            <MetricCard label="Trust gate violations" value="0" trend="flat" hint="rolling 7d" />
          </div>
        </div>
      </section>

      <section>
        <SectionHeading
          eyebrow="Brand Pillars"
          title="What Dealix stands for"
          description="Five non-negotiable pillars that govern every surface, message and machine."
        />
        <div className="dx-grid" style={{ gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))" }}>
          {PILLARS.map((p) => (
            <BrandCard key={p.eyebrow} eyebrow={p.eyebrow} title={p.title} description={p.desc} />
          ))}
        </div>
      </section>

      <section>
        <SectionHeading
          eyebrow="Founder Console"
          title="Where the company is operated"
          description="Eighteen surfaces, one operating system. Every action is trust-gated; every event is audited."
        />
        <div className="dx-grid" style={{ gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))" }}>
          {SURFACES.map((s) => (
            <a
              key={s.href}
              href={s.href}
              className="dx-card"
              style={{ display: "block", textDecoration: "none", color: "inherit" }}
            >
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 6 }}>
                <strong style={{ color: "var(--dx-text)" }}>{s.label}</strong>
                <StatusBadge tone="info" label="Live" />
              </div>
              <p className="dx-muted" style={{ margin: 0, fontSize: "0.875rem" }}>{s.note}</p>
            </a>
          ))}
        </div>
      </section>
    </div>
  );
}
