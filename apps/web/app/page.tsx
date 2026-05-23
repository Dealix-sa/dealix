import Link from "next/link";
import { FounderShell } from "../components/founder-shell";
import { BrandCard } from "../components/brand/brand-card";
import { SectionHeading } from "../components/brand/section-heading";
import { MetricCard } from "../components/brand/metric-card";
import { CtaButton } from "../components/brand/cta-button";
import { brandTokens } from "../lib/brand-tokens";
import { getCEOSummary } from "../lib/dealix-runtime";

export const dynamic = "force-dynamic";

const SECTIONS: Array<{ href: string; label: string; description: string }> = [
  { href: "/ceo", label: "CEO Cockpit", description: "Pipeline, approvals, trust, runway at a glance." },
  { href: "/sales-cockpit", label: "Sales Cockpit", description: "Funnel stages, win rates, next-best deals." },
  { href: "/approvals", label: "Approvals", description: "Human-in-the-loop oversight queue." },
  { href: "/workers", label: "Workers", description: "Live agent + worker health." },
  { href: "/trust", label: "Trust", description: "Policy violations and guard flags." },
  { href: "/finance", label: "Finance", description: "MRR, AR aging, collections, runway." },
  { href: "/distribution", label: "Distribution", description: "Channels, sends, compliance rate." },
  { href: "/delivery", label: "Delivery", description: "Deliverables waiting on humans." },
  { href: "/retention", label: "Retention", description: "Renewals, expansion, churn risk." },
  { href: "/proof", label: "Proof Library", description: "ProofPacks ready to share." },
  { href: "/control-plane", label: "Control Plane", description: "Runs, policies, scorecard." },
  { href: "/audit", label: "Audit", description: "Append-only audit event log." },
  { href: "/evals", label: "Evals", description: "Agent eval suites + coverage." },
  { href: "/product", label: "Product", description: "Productization + SLA posture." },
  { href: "/security", label: "Security", description: "PDPL, incidents, posture." },
  { href: "/sovereign", label: "Sovereign Readiness", description: "Saudi-first scorecard." },
  { href: "/growth", label: "Growth Targeting", description: "ICP + targeting health." },
  { href: "/marketing", label: "Marketing", description: "Content + inbound funnel." },
  { href: "/customer-success", label: "Customer Success", description: "NRR, NPS, at-risk." },
  { href: "/finance-ops", label: "Finance Ops", description: "Invoices, ZATCA, payouts." },
];

export default async function HomePage() {
  const ceo = await getCEOSummary();
  return (
    <FounderShell active="/">
      <SectionHeading
        title="Welcome to the Dealix Founder Console"
        subtitle={brandTokens.tagline}
      />
      <BrandCard title="CEO Snapshot" source={ceo.source}>
        {ceo.data.metrics.length === 0 ? (
          <div className="dealix-empty">
            No metrics available yet. Connect the private ops root or run the activation sprint.
          </div>
        ) : (
          <div className="dealix-grid dealix-grid--4">
            {ceo.data.metrics.map((m) => (
              <MetricCard key={m.label} value={m.value} label={m.label} delta={m.delta} />
            ))}
          </div>
        )}
      </BrandCard>
      <BrandCard title="Founder Console Sections">
        <div className="dealix-grid dealix-grid--3">
          {SECTIONS.map((s) => (
            <Link
              key={s.href}
              href={s.href}
              style={{
                display: "block",
                padding: 14,
                borderRadius: 10,
                border: "1px solid rgba(178,187,198,0.18)",
                background: "rgba(11,18,32,0.6)",
                textDecoration: "none",
                color: "inherit",
              }}
            >
              <div style={{ fontWeight: 600, color: "var(--dealix-white)", fontSize: 14 }}>{s.label}</div>
              <div style={{ fontSize: 12, color: "var(--dealix-soft-silver)", marginTop: 4 }}>{s.description}</div>
            </Link>
          ))}
        </div>
      </BrandCard>
      <BrandCard title="Brand Pillars">
        <div className="dealix-grid dealix-grid--3">
          {brandTokens.pillars.map((p) => (
            <div key={p} className="dealix-metric" style={{ alignItems: "flex-start" }}>
              <span className="dealix-metric__label">Pillar</span>
              <span style={{ color: "var(--dealix-white)", fontWeight: 600 }}>{p}</span>
            </div>
          ))}
        </div>
        <div style={{ marginTop: 16, display: "flex", gap: 8 }}>
          <CtaButton as="link" href="/ceo">
            Open CEO Cockpit
          </CtaButton>
          <CtaButton as="link" href="/control-plane" variant="ghost">
            View Control Plane
          </CtaButton>
        </div>
      </BrandCard>
    </FounderShell>
  );
}
