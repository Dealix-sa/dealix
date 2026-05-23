import { FounderShell, Stat } from "../../components/founder-shell";
import { loadSalesFunnel } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

function detectBottleneck(funnel: {
  lead_intelligence: number;
  approved_outreach: number;
  sent: number;
  positive_replies: number;
  proposals: number;
  payment_capture: number;
}): string {
  if (funnel.lead_intelligence < 100) return "Lead intelligence < 100 records";
  if (funnel.approved_outreach > funnel.sent) return "Approved drafts not sent";
  if (funnel.positive_replies > funnel.proposals) return "Positive replies without proposals";
  if (funnel.proposals > 0 && funnel.payment_capture === 0)
    return "Proposals without payment follow-up";
  return "No active bottleneck";
}

export default async function SalesCockpitPage() {
  const result = await loadSalesFunnel();

  if (!result.ok) {
    return (
      <FounderShell
        title="Sales Cockpit"
        subtitle="Funnel · bottleneck · next move"
        error={result.error}
      >
        <div className="card">
          <p style={{ margin: 0 }}>
            Funnel runtime is unreachable. Start the API and bootstrap Private
            Ops to see live numbers.
          </p>
        </div>
      </FounderShell>
    );
  }

  const funnel = result.data;
  const bottleneck = detectBottleneck(funnel);

  return (
    <FounderShell
      title="Sales Cockpit"
      subtitle="One funnel. One bottleneck. One next move."
      source={funnel.source}
      lastUpdated={funnel.last_updated}
    >
      <section className="card">
        <div style={{ fontSize: 12, color: "#64748b" }}>Bottleneck</div>
        <h2 style={{ margin: "6px 0 0" }}>{bottleneck}</h2>
      </section>

      <section
        className="grid"
        style={{ gridTemplateColumns: "repeat(auto-fit, minmax(160px, 1fr))" }}
      >
        <Stat label="Lead intelligence" value={funnel.lead_intelligence} hint="Total accounts in base" />
        <Stat label="A leads" value={funnel.a_leads} />
        <Stat label="Pending approval" value={funnel.pending_approval} />
        <Stat label="Approved outreach" value={funnel.approved_outreach} />
        <Stat label="Sent" value={funnel.sent} />
        <Stat label="Replies" value={funnel.replies} />
        <Stat label="Positive replies" value={funnel.positive_replies} />
        <Stat label="Samples" value={funnel.samples} />
        <Stat label="Proposals" value={funnel.proposals} />
        <Stat label="Payment capture" value={funnel.payment_capture} />
      </section>
    </FounderShell>
  );
}
