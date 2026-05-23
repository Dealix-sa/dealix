import { PageShell } from "../../components/brand/page-shell";
import { SectionHeading } from "../../components/brand/section-heading";
import { BrandCard } from "../../components/brand/brand-card";
import { StatusBadge } from "../../components/brand/status-badge";

const MACHINES = [
  { id: "outbound_draft", label: "Outbound draft" },
  { id: "linkedin_queue", label: "LinkedIn queue" },
  { id: "email_draft", label: "Email draft" },
  { id: "contact_form_queue", label: "Contact-form queue" },
  { id: "follow_up", label: "Follow-up" },
  { id: "reply_router", label: "Reply router" },
  { id: "nurture", label: "Nurture" },
  { id: "partner_referral", label: "Partner referral" },
  { id: "abm_strategic_account", label: "ABM strategic account" },
  { id: "proof_to_demand", label: "Proof-to-demand" },
];

export default function DistributionPage() {
  return (
    <PageShell currentPath="/distribution">
      <SectionHeading
        eyebrow="Distribution"
        title="Drafts in. Approvals out."
        description="The Distribution War Machine. Each machine writes only to its queue — never to an external channel."
        action={<StatusBadge label="trust-gated" tone="accent" />}
      />
      <BrandCard title="Registered machines">
        <div className="dlx-grid dlx-grid-3">
          {MACHINES.map((m) => (
            <div key={m.id} className="dlx-card" style={{ background: "var(--dlx-surface-alt)" }}>
              <div style={{ fontWeight: 600 }}>{m.label}</div>
              <p className="dlx-muted" style={{ margin: "6px 0 8px", fontSize: 12 }}>
                {`docs/growth/${m.id.toUpperCase()}_MACHINE.md`}
              </p>
              <StatusBadge label="draft-only" tone="neutral" />
            </div>
          ))}
        </div>
      </BrandCard>
    </PageShell>
  );
}
