import { ConsolePage } from "../../components/brand/console-page";

export const metadata = { title: "CEO Console — Dealix" };

export default function CeoPage() {
  return (
    <ConsolePage
      eyebrow="Founder Operating Surface"
      title="CEO Console"
      description="One screen for the founder: daily brief, top decisions, cash forecast, distribution heat, and trust posture."
      status={{ tone: "ok", label: "operational" }}
      sections={[
        {
          title: "Daily brief",
          description: "Auto-assembled signals across cash, distribution, delivery and trust.",
          bullets: [
            "Cash captured today vs. forecast",
            "Top three approvals awaiting consent",
            "Top three at-risk deals",
            "Top three sectors converting this week",
          ],
        },
        {
          title: "Decision queue",
          description: "Trust-gated items the founder must approve, decline or defer.",
          bullets: [
            "External sends (email / LinkedIn / forms)",
            "Proposal commitments",
            "Refunds, discounts, custom terms",
            "Proof publication",
          ],
        },
        {
          title: "Cash forecast",
          description: "Forecast counts only confirmed payments and contractually-fenced invoices.",
          bullets: ["Pipeline coverage vs. target", "Receivables ageing", "Retention book MRR"],
        },
        {
          title: "Risk posture",
          description: "From trust, security, evals and audit.",
          bullets: ["Open trust gate violations", "Failing evals", "Open security findings"],
        },
      ]}
      api={[
        { method: "GET", path: "/api/v1/internal/brand/summary", note: "Brand tokens + pillars (read-only)." },
        { method: "GET", path: "/api/v1/internal/growth/targeting", note: "Sector and ICP signal." },
        { method: "GET", path: "/api/v1/internal/marketing/summary", note: "Active campaigns and queues." },
        { method: "GET", path: "/api/v1/internal/product/distribution", note: "Offer ladder + queues." },
      ]}
      trustNote="The CEO console reads from internal signals only; it never triggers external action without an explicit approval from /approvals."
      related={[
        { href: "/approvals", label: "Approvals" },
        { href: "/sales-cockpit", label: "Sales Cockpit" },
        { href: "/distribution", label: "Distribution" },
        { href: "/finance", label: "Finance" },
      ]}
    />
  );
}
