import { ConsolePage } from "../../components/brand/console-page";

export const metadata = { title: "Product Ladder — Dealix" };

const LADDER = [
  { rung: "1. Free Sample / Diagnostic", who: "First-touch ICP-fit accounts", desc: "Diagnostic sample built from real public signal." },
  { rung: "2. Revenue Sprint", who: "Founders who want a quick proof", desc: "Two-week sprint focused on one revenue lever." },
  { rung: "3. Managed Pilot", who: "Teams ready to operate", desc: "Six-week operated pilot with full QA." },
  { rung: "4. Revenue Desk Retainer", who: "Operating customers", desc: "Monthly retainer running Distribution + Delivery." },
  { rung: "5. Founder Console / Command Center", who: "Hands-on founders", desc: "Console + retainer hybrid for founder-led teams." },
  { rung: "6. Enterprise Revenue Intelligence OS", who: "Larger orgs", desc: "Multi-tenant deployment with sovereign data." },
  { rung: "7. Partner / White-label Revenue OS", who: "Agencies, system integrators", desc: "Operate Dealix under a partner brand." },
];

export default function Page() {
  return (
    <ConsolePage
      eyebrow="Product Operating Surface"
      title="Product Ladder"
      description="Seven rungs from free diagnostic to white-label OS. Pricing guardrails apply; no guaranteed-result claims anywhere."
      status={{ tone: "ok", label: "guardrails-on" }}
      sections={LADDER.map((r) => ({ title: r.rung, description: r.desc, bullets: [r.who] }))}
      api={[
        { method: "GET", path: "/api/v1/internal/product/distribution", note: "Offer ladder + active queues." },
      ]}
      trustNote="No rung promises guaranteed revenue, leads or close rates. All claims are evidence-bound."
      related={[
        { href: "/marketing", label: "Marketing OS" },
        { href: "/sales-cockpit", label: "Sales Cockpit" },
      ]}
    />
  );
}
