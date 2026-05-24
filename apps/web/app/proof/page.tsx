import { ConsolePage } from "../../components/brand/console-page";

export const metadata = { title: "Proof — Dealix" };

export default function Page() {
  return (
    <ConsolePage
      eyebrow="Evidence Operating Surface"
      title="Proof"
      description="Case studies, outcome briefs, and sample artifacts — produced only after a delivered outcome and an explicit consent record."
      status={{ tone: "ok", label: "consent-gated" }}
      sections={[
        { title: "Proof Approval OS", description: "Customer signs off on every claim before it leaves the building.", bullets: ["Claim → evidence map", "Customer signature recorded", "Audit log entry on publish"] },
        { title: "Case study factory", description: "Templates and rendering pipeline for case studies.", bullets: ["Bilingual AR + EN", "Brand-checked", "No guaranteed-result claims"] },
        { title: "Proof-to-Demand", description: "Routes approved proofs to relevant ICP signals.", bullets: ["Queue: proof_to_demand_queue.csv", "Manual send"] },
      ]}
      trustNote="No proof artifact may be published or shared externally without a Customer Consent record stored alongside it."
      related={[
        { href: "/delivery", label: "Delivery QA" },
        { href: "/marketing", label: "Marketing OS" },
        { href: "/approvals", label: "Approvals" },
      ]}
    />
  );
}
