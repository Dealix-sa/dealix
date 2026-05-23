import { FounderShell } from "../../components/founder-shell";
import { getSalesFunnel } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function SalesCockpitPage() {
  const funnel = await getSalesFunnel();
  const metrics: Array<[string, number]> = [
    ["Lead Intelligence", funnel.lead_intelligence],
    ["A Leads", funnel.a_leads],
    ["Pending Approval", funnel.pending_approval],
    ["Approved Outreach", funnel.approved_outreach],
    ["Sent", funnel.sent],
    ["Replies", funnel.replies],
    ["Positive Replies", funnel.positive_replies],
    ["Samples", funnel.samples],
    ["Proposals", funnel.proposals],
    ["Payment Capture", funnel.payment_capture]
  ];
  return (
    <FounderShell>
      <main>
        <h1>Sales Cockpit</h1>
        <p>Track the Dealix revenue factory from market intelligence to payment capture.</p>
        <p className="founder-source">Source: {funnel.source}</p>
        <section className="founder-metric-grid">
          {metrics.map(([label, value]) => (
            <div key={label} className="founder-metric">
              <p className="founder-metric__label">{label}</p>
              <p className="founder-metric__value">{value}</p>
            </div>
          ))}
        </section>
      </main>
    </FounderShell>
  );
}
