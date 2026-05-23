import { FounderShell, MetricGrid } from "../../components/founder/founder-shell";
import { getCEOSummary } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function CEOPage() {
  const summary = await getCEOSummary();
  return (
    <FounderShell
      title="CEO Briefing"
      subtitle={summary.top_action}
      source={summary.source}
    >
      <MetricGrid
        items={[
          { label: "Status", value: summary.status },
          { label: "Risk flags", value: summary.risk_flags },
          { label: "Cash collected (SAR)", value: summary.cash_collected_sar },
          { label: "Approved outreach", value: summary.approved_outreach },
          { label: "Sent outreach", value: summary.sent_outreach },
          { label: "Positive replies", value: summary.positive_replies },
          { label: "Proposals due", value: summary.proposals_due },
          { label: "Payment follow-ups", value: summary.payment_follow_ups }
        ]}
      />
      {summary.generated_at ? (
        <div className="card" style={{ fontSize: 12, color: "#64748b" }}>
          generated_at: {summary.generated_at}
        </div>
      ) : null}
    </FounderShell>
  );
}
