import { ConsolePage } from "../../components/brand/console-page";

export const metadata = { title: "Finance — Dealix" };

export default function Page() {
  return (
    <ConsolePage
      eyebrow="Cash Operating Surface"
      title="Finance"
      description="Payment capture, invoices, receivables and cash forecast. Dealix counts cash collected, not pipeline promised."
      status={{ tone: "ok", label: "cash-first" }}
      sections={[
        { title: "Payment Capture OS", description: "End-to-end flow from quote → invoice → payment confirmed.", bullets: ["No commitment without founder approval", "Saudi VAT-aware invoicing", "Reconciliation against bank events"] },
        { title: "Receivables", description: "Ageing buckets, follow-up cadences, escalation rules.", bullets: ["0-15 / 15-30 / 30-60 / 60+", "Polite-first reminders", "Founder escalation at 30 days"] },
        { title: "Cash forecast", description: "Forward 30 / 60 / 90 day cash view.", bullets: ["Confirmed payments + fenced invoices only", "No pipeline weighting"] },
        { title: "Finance Copilot", description: "Reads finance data, drafts collection messages, recommends actions.", bullets: ["Draft-only", "Never moves money", "Audit-required"] },
      ]}
      trustNote="The Finance Copilot may draft collection messages, but no message is sent and no commitment is made without founder approval."
      related={[
        { href: "/sales-cockpit", label: "Sales Cockpit" },
        { href: "/delivery", label: "Delivery QA" },
        { href: "/retention", label: "Retention" },
      ]}
    />
  );
}
