import { FounderShell, Stat } from "../../components/founder-shell";
import { loadCeoSummary } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function CeoPage() {
  const result = await loadCeoSummary();

  if (!result.ok) {
    return (
      <FounderShell
        title="CEO Console"
        subtitle="Top action · status · bottleneck"
        error={result.error}
      >
        <div className="card">
          <p style={{ margin: 0 }}>
            Runtime is unreachable. Start the API
            (<code>make run</code>) and bootstrap Private Ops
            (<code>scripts/bootstrap_private_ops.sh</code>) to wire live data.
          </p>
        </div>
      </FounderShell>
    );
  }

  const ceo = result.data;
  return (
    <FounderShell
      title="CEO Console"
      subtitle="One action. One status. Real numbers."
      source={ceo.source}
      lastUpdated={ceo.last_updated}
    >
      <section className="card">
        <div style={{ fontSize: 12, color: "#64748b" }}>Top action</div>
        <h2 style={{ margin: "6px 0 0" }}>{ceo.top_action}</h2>
        <div style={{ marginTop: 8, color: "#475569" }}>{ceo.status}</div>
      </section>

      <section
        className="grid"
        style={{ gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))" }}
      >
        <Stat label="Cash collected (SAR)" value={ceo.cash_collected_sar} />
        <Stat label="Approved outreach" value={ceo.approved_outreach} />
        <Stat label="Positive replies" value={ceo.positive_replies} />
        <Stat label="Proposals due" value={ceo.proposals_due} />
        <Stat label="Payment follow-ups" value={ceo.payment_followups_due} />
        <Stat label="Risk flags" value={ceo.risk_flags} />
      </section>
    </FounderShell>
  );
}
