import { FounderShell, MetricGrid } from "../../components/founder/founder-shell";
import { getSalesFunnel } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function SalesCockpitPage() {
  const funnel = await getSalesFunnel();
  return (
    <FounderShell title="Sales Cockpit" source={funnel.source}>
      <MetricGrid
        items={[
          { label: "Lead intelligence", value: funnel.lead_intelligence_count },
          { label: "A leads", value: funnel.a_leads },
          { label: "Pending approval", value: funnel.pending_approval },
          { label: "Approved outreach", value: funnel.approved_outreach },
          { label: "Sent", value: funnel.sent },
          { label: "Replies", value: funnel.replies },
          { label: "Positive replies", value: funnel.positive_replies },
          { label: "Samples", value: funnel.samples },
          { label: "Proposals", value: funnel.proposals },
          { label: "Payment capture", value: funnel.payment_capture }
        ]}
      />
    </FounderShell>
  );
}
