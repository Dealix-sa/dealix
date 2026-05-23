import { ConsolePage } from "../../components/brand/console-page";

export const metadata = { title: "Distribution War Room — Dealix" };

export default function Page() {
  return (
    <ConsolePage
      eyebrow="Growth Operating Surface"
      title="Distribution War Room"
      description="All distribution machines in one view. Each produces drafts, queues, scores and recommendations — never external action."
      status={{ tone: "ok", label: "draft-only" }}
      sections={[
        { title: "Outbound Draft Machine", description: "Personalised email drafts per account.", bullets: ["Queue: outreach_queue.csv", "Approval: founder", "Source-of-truth: ICP + triggers"] },
        { title: "LinkedIn Queue Machine", description: "Connection notes and InMail drafts.", bullets: ["Queue: linkedin_queue.csv", "Manual send", "Suppression respected"] },
        { title: "Email Draft Machine", description: "Sequenced cadences for ICP-fit accounts.", bullets: ["Drafts only", "Trust gate on send"] },
        { title: "Contact Form Queue", description: "Human-completed inbound forms for partners and gated accounts.", bullets: ["Queue: contact_form_queue.csv", "Manual operator action"] },
        { title: "Follow-up Planner", description: "Time- and event-based reminders.", bullets: ["Queue: followup_queue.csv", "Closes silently on reply"] },
        { title: "Reply Router", description: "Classifies replies; recommends next best action.", bullets: ["No auto-reply", "Routes to sales / nurture / suppression"] },
        { title: "Nurture Machine", description: "Long-cycle warming for not-yet-ready accounts.", bullets: ["Content-led", "Tied to proof"] },
        { title: "Partner / Referral Machine", description: "Co-sell, intro requests, partner enablement.", bullets: ["Queue: partner_referral_queue.csv"] },
        { title: "ABM Strategic Account Machine", description: "Top-tier accounts with bespoke plays.", bullets: ["Queue: abm_account_queue.csv"] },
        { title: "Proof-to-Demand Machine", description: "Routes approved proof artifacts to demand triggers.", bullets: ["Queue: proof_to_demand_queue.csv"] },
      ]}
      api={[
        { method: "GET", path: "/api/v1/internal/growth/targeting", note: "Sector targeting, ICP & accounts." },
        { method: "GET", path: "/api/v1/internal/marketing/summary", note: "Active campaigns and content calendar." },
      ]}
      trustNote="No machine sends externally. All output is draft, queue, score or recommendation. External action requires a per-item approval in /approvals."
      related={[
        { href: "/sales-cockpit", label: "Sales Cockpit" },
        { href: "/marketing", label: "Marketing OS" },
        { href: "/approvals", label: "Approvals" },
      ]}
    />
  );
}
