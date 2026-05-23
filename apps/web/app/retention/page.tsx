import { ConsolePage } from "../../components/brand/console-page";

export const metadata = { title: "Retention — Dealix" };

export default function Page() {
  return (
    <ConsolePage
      eyebrow="Customer Operating Surface"
      title="Retention"
      description="Customer health, expansion paths and referral asks. Designed so renewal is the natural conclusion of value delivered."
      status={{ tone: "ok", label: "value-led" }}
      sections={[
        { title: "Health signals", bullets: ["Usage trend", "Outcome attribution", "Operator NPS", "Open issues"] },
        { title: "Expansion", description: "When the next rung of the offer ladder is the right move.", bullets: ["Triggered by outcomes, not quotas", "Founder-approved upgrade", "Pricing guardrails enforced"] },
        { title: "Referrals", description: "Ask for referrals only after a delivered outcome and explicit consent.", bullets: ["Queue: partner_referral_queue.csv", "No spammy mass-ask"] },
      ]}
      trustNote="Customer escalations and saves are surfaced here but resolved through approvals, not autonomous action."
      related={[
        { href: "/finance", label: "Finance" },
        { href: "/proof", label: "Proof" },
        { href: "/delivery", label: "Delivery QA" },
      ]}
    />
  );
}
