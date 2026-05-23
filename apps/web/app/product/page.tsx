import { PageShell } from "../../components/brand/page-shell";
import { SectionHeading } from "../../components/brand/section-heading";
import { BrandCard } from "../../components/brand/brand-card";

const LADDER = [
  { rung: 1, name: "Free Sample / Diagnostic", one: "See where your revenue motion stands — bilingual, scored, no sales pitch." },
  { rung: 2, name: "Revenue Sprint", one: "Seven days, one queue, founder-approved drafts ready to go." },
  { rung: 3, name: "Managed Pilot", one: "Ninety days running the Revenue OS — scored pipeline, audit log, one proof artifact." },
  { rung: 4, name: "Revenue Desk Retainer", one: "A monthly cockpit, run with you weekly, built around your approval rhythm." },
  { rung: 5, name: "Founder Console", one: "Your always-on Revenue Operating System." },
  { rung: 6, name: "Enterprise Revenue OS", one: "Multi-BU Revenue OS with control plane and PMO." },
  { rung: 7, name: "Partner / White-label Revenue OS", one: "Dealix's engine inside your brand — governed, audited." },
];

export default function ProductPage() {
  return (
    <PageShell currentPath="/product">
      <SectionHeading
        eyebrow="Product"
        title="The Dealix ladder."
        description="Seven rungs. Each is a self-contained offer with a clear scope, a price band, and a clear next rung."
      />
      <BrandCard title="Product ladder">
        <ol style={{ margin: 0, paddingInlineStart: 22, lineHeight: 1.7 }}>
          {LADDER.map((r) => (
            <li key={r.rung} style={{ marginBottom: 10 }}>
              <div style={{ fontWeight: 600 }}>{r.name}</div>
              <div className="dlx-muted" style={{ fontSize: 13 }}>{r.one}</div>
            </li>
          ))}
        </ol>
      </BrandCard>
    </PageShell>
  );
}
