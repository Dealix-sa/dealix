import { ConsolePage } from "../../components/brand/console-page";

export const metadata = { title: "Sales Cockpit — Dealix" };

export default function Page() {
  return (
    <ConsolePage
      eyebrow="Revenue Operating Surface"
      title="Sales Cockpit"
      description="Pipeline, drafts, follow-ups and reply routing for the founder-led motion. No external send happens here without approval."
      status={{ tone: "ok", label: "founder-gated" }}
      sections={[
        {
          title: "Pipeline",
          bullets: ["Stages: lead → qualified → sample → proposal → committed → paid", "Forecast is cash-collected only", "Weekly win/loss review feeds the Learning Loop"],
        },
        {
          title: "Drafts",
          description: "Outbound, replies, and proposals drafted by the Outreach and Proposal agents.",
          bullets: ["Sit in the queue for review", "Bilingual AR + EN", "Never auto-sent"],
        },
        {
          title: "Follow-ups",
          bullets: ["Time-based and event-based reminders", "Suppression respected", "Reply router classifies inbound"],
        },
        {
          title: "Objection library",
          description: "Live record of objections, their best responses, and conversion deltas.",
          bullets: ["Sorted by sector and offer", "Updated weekly", "Linked to scripts"],
        },
      ]}
      api={[
        { method: "GET", path: "/api/v1/internal/growth/targeting", note: "ICP, sectors, account scores." },
        { method: "GET", path: "/api/v1/internal/product/distribution", note: "Offers and active queues." },
      ]}
      trustNote="Drafts may be sent only after explicit founder approval via /approvals. Bulk send is blocked by policy-as-code."
      related={[
        { href: "/distribution", label: "Distribution War Room" },
        { href: "/approvals", label: "Approvals" },
        { href: "/proof", label: "Proof" },
      ]}
    />
  );
}
