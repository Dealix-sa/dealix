import { ConsolePage } from "../../components/brand/console-page";

export const metadata = { title: "Delivery QA — Dealix" };

export default function Page() {
  return (
    <ConsolePage
      eyebrow="Delivery Operating Surface"
      title="Delivery QA"
      description="Sample, proposal, sprint and managed retainer delivery — quality-gated, on time, in brand."
      status={{ tone: "ok", label: "QA-gated" }}
      sections={[
        { title: "Sample Factory", description: "Free diagnostic and trial samples produced from real customer data.", bullets: ["Time-boxed", "Brand-checked", "No external publish"] },
        { title: "Proposal Factory", description: "Proposals assembled from product ladder, pricing guardrails and customer signal.", bullets: ["Never auto-sent", "Pricing guardrails enforced"] },
        { title: "Delivery QA OS", description: "Checklist of evidence before any artifact reaches a customer.", bullets: ["Brand check", "Trust check", "Accuracy check", "Founder sign-off"] },
        { title: "Delivery Copilot", description: "Drafts updates, status reports and QA checklists.", bullets: ["Draft-only", "Bilingual"] },
      ]}
      trustNote="Delivery artifacts are never shared externally without founder sign-off and a passing QA checklist."
      related={[
        { href: "/proof", label: "Proof" },
        { href: "/retention", label: "Retention" },
        { href: "/approvals", label: "Approvals" },
      ]}
    />
  );
}
