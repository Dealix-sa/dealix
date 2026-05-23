import { DealixLogo } from "../components/brand/dealix-logo";
import { BrandCard } from "../components/brand/brand-card";
import { SectionHeading } from "../components/brand/section-heading";
import { StatusBadge } from "../components/brand/status-badge";
import { CtaButton } from "../components/brand/cta-button";
import { dealixBrand } from "../lib/brand-tokens";

const SHELL_LINKS: { href: string; label: string; blurb: string; tone?: "accent" | "warning" }[] = [
  { href: "/ceo", label: "CEO", blurb: "Weekly KPI tree + one prioritised gap.", tone: "accent" },
  { href: "/sales-cockpit", label: "Sales Cockpit", blurb: "Pipeline by tier + the next approval." },
  { href: "/approvals", label: "Approvals", blurb: "Drafts waiting for your sign-off." },
  { href: "/workers", label: "Workers", blurb: "Background jobs + queues." },
  { href: "/trust", label: "Trust", blurb: "Policy, consent, audit posture." },
  { href: "/finance", label: "Finance", blurb: "ZATCA, payments, retainers." },
  { href: "/distribution", label: "Distribution", blurb: "Outbound, LinkedIn, Email queues." },
  { href: "/delivery", label: "Delivery", blurb: "Engagements + Day-1 packs." },
  { href: "/retention", label: "Retention", blurb: "Health + renewal cycles." },
  { href: "/proof", label: "Proof", blurb: "Consented case studies." },
  { href: "/control-plane", label: "Control Plane", blurb: "Workflow runs + traces." },
  { href: "/audit", label: "Audit", blurb: "Approval ledger + agent runs." },
  { href: "/evals", label: "Evals", blurb: "Agent eval + red-team gates." },
  { href: "/product", label: "Product", blurb: "Ladder + offer packaging." },
  { href: "/security", label: "Security", blurb: "Kill switches + policy-as-code." },
  { href: "/sovereign", label: "Sovereign", blurb: "Data sovereignty + tenants." },
  { href: "/growth", label: "Growth", blurb: "Sector / ICP / account scoring." },
  { href: "/marketing", label: "Marketing", blurb: "Content calendar + drafts." },
];

export default function HomePage() {
  return (
    <main className="dlx-grid">
      <header style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: 16, marginBottom: 16 }}>
        <DealixLogo height={36} withTagline />
        <StatusBadge label="trust-gated · audit-ready" tone="accent" />
      </header>

      <SectionHeading
        eyebrow="Founder Console"
        title={dealixBrand.taglineEn}
        description={dealixBrand.positioning}
        action={<CtaButton href="/approvals">Approve drafts</CtaButton>}
      />

      <BrandCard
        title="Operating pillars"
        subtitle="Every screen in this console serves one of these five pillars."
      >
        <ul style={{ margin: 0, paddingInlineStart: 18, columns: 2, columnGap: 32, lineHeight: 1.8 }}>
          {dealixBrand.pillars.map((p) => (
            <li key={p} className="dlx-muted">{p}</li>
          ))}
        </ul>
      </BrandCard>

      <BrandCard title="Surfaces" subtitle="One screen per operating layer.">
        <div className="dlx-grid dlx-grid-3">
          {SHELL_LINKS.map((link) => (
            <a
              key={link.href}
              href={link.href}
              style={{
                textDecoration: "none",
                color: "inherit",
                border: "1px solid var(--dlx-border)",
                borderRadius: 14,
                padding: "14px 16px",
                background: "var(--dlx-surface-alt)",
                display: "block",
              }}
            >
              <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: 8 }}>
                <span style={{ fontWeight: 600 }}>{link.label}</span>
                {link.tone && <StatusBadge label="primary" tone={link.tone} />}
              </div>
              <p className="dlx-muted" style={{ fontSize: 13, margin: "6px 0 0", lineHeight: 1.5 }}>
                {link.blurb}
              </p>
            </a>
          ))}
        </div>
      </BrandCard>
    </main>
  );
}
