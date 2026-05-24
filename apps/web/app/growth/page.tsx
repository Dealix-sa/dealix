import { ConsolePage } from "../../components/brand/console-page";

export const metadata = { title: "Growth Strategist — Dealix" };

const SECTORS = [
  "ERP / CRM",
  "Cybersecurity",
  "B2B agencies",
  "Logistics / industrial services",
  "Consulting / digital transformation",
  "SaaS / software",
  "Enterprise services",
  "Saudi high-ticket B2B providers",
];

export default function Page() {
  return (
    <ConsolePage
      eyebrow="Strategy Operating Surface"
      title="Growth Strategist"
      description="Sectors, ICP, buyer personas, account scores and trigger events. Recomputed daily; pruned weekly."
      status={{ tone: "ok", label: "live-ranking" }}
      sections={[
        { title: "Active sectors", description: "Ranked by fit, velocity, contract size and proof.", bullets: SECTORS },
        { title: "ICP segmentation", bullets: ["Size band", "Stack", "Revenue motion", "KSA presence"] },
        { title: "Account scoring", description: "Composite of fit, intent and capacity.", bullets: ["File: growth/account_scores.csv", "Refreshed daily"] },
        { title: "Trigger events", bullets: ["Funding", "Senior hires", "Tech adoption", "Regulatory moves"] },
      ]}
      api={[{ method: "GET", path: "/api/v1/internal/growth/targeting", note: "Sector + ICP + accounts." }]}
      trustNote="Account scoring is decision support, not decision authority. Engagement decisions are made by the founder."
      related={[
        { href: "/distribution", label: "Distribution" },
        { href: "/marketing", label: "Marketing OS" },
        { href: "/product", label: "Product Ladder" },
      ]}
    />
  );
}
