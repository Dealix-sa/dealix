import { ConsolePage } from "../../components/brand/console-page";

export const metadata = { title: "Marketing OS — Dealix" };

export default function Page() {
  return (
    <ConsolePage
      eyebrow="Demand Operating Surface"
      title="Marketing OS"
      description="Content calendar, founder-led content engine, landing experiments and bilingual copywriting rules — under the brand voice."
      status={{ tone: "ok", label: "brand-bound" }}
      sections={[
        { title: "Content calendar", description: "Weekly themed cadence across LinkedIn, newsletter and landing.", bullets: ["File: marketing/content_calendar.csv", "AR + EN", "Tied to active sectors"] },
        { title: "Founder-led content", description: "Insight-driven posts from the founder's POV.", bullets: ["Sector insights", "Operational learnings", "Proof-safe excerpts"] },
        { title: "Campaigns", description: "Time-boxed thematic pushes.", bullets: ["File: marketing/campaigns.csv", "Each has a clear KPI", "Reviewed weekly"] },
        { title: "Landing experiments", description: "Iterating headlines, hero proof and CTA copy.", bullets: ["No paid-traffic experiments without approval", "Brand Guardian checks before publish"] },
      ]}
      api={[{ method: "GET", path: "/api/v1/internal/marketing/summary", note: "Active campaigns + calendar." }]}
      trustNote="No campaign is launched without a brand check and a trust check; no claim is published without evidence."
      related={[
        { href: "/distribution", label: "Distribution War Room" },
        { href: "/growth", label: "Growth Strategist" },
        { href: "/product", label: "Product Ladder" },
      ]}
    />
  );
}
