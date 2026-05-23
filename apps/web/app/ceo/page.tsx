import { FounderShell } from "../../components/founder-shell";
import { FounderMetric } from "../../components/founder-metric";
import { getCEOSummary } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function CEOCommandCenterPage() {
  const summary = await getCEOSummary();
  return (
    <FounderShell>
      <main>
        <section>
          <p className="founder-source">Dealix Internal</p>
          <h1>CEO Command Center</h1>
          <p>
            Control Dealix revenue, approvals, workers, trust, finance, and delivery from one screen.
          </p>
        </section>
        <section className="founder-callout">
          <p className="founder-callout__label">Top CEO Action</p>
          <h2 className="founder-callout__title">{summary.top_action}</h2>
          <p>Status: {summary.status}</p>
          <p className="founder-source">Source: {summary.source}</p>
        </section>
        <section className="founder-metric-grid">
          <FounderMetric label="Risk Flags" value={summary.risk_flags} />
          <FounderMetric label="Cash SAR" value={summary.cash_collected_sar} />
          <FounderMetric label="Approved Outreach" value={summary.approved_outreach} />
          <FounderMetric label="Positive Replies" value={summary.positive_replies} />
          <FounderMetric label="Proposals Due" value={summary.proposals_due} />
          <FounderMetric label="Payment Follow-ups" value={summary.payment_followups_due} />
        </section>
        <p className="founder-source" style={{ marginTop: 24 }}>
          Last updated: {summary.last_updated}
        </p>
      </main>
    </FounderShell>
  );
}
