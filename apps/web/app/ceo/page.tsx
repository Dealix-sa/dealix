import { FounderShell } from "../../components/founder-shell";
import { getCEOSummary } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

function formatSar(value: number): string {
  return value.toLocaleString("en-US") + " SAR";
}

export default async function CEOPage() {
  const summary = await getCEOSummary();
  return (
    <FounderShell title="CEO Command Center">
      <p className="lead">
        Top action, company status, revenue snapshot, trust flags, and
        worker health. Read-only in v1.
      </p>
      <section className="row">
        <div className="card kpi">
          <span className="muted">Top Action</span>
          <strong>{summary.top_action}</strong>
        </div>
        <div className="card kpi">
          <span className="muted">Status</span>
          <strong>{summary.status}</strong>
        </div>
        <div className="card kpi">
          <span className="muted">Risk Flags</span>
          <span className="kpi-value">{summary.risk_flags}</span>
        </div>
        <div className="card kpi">
          <span className="muted">Cash Collected</span>
          <span className="kpi-value">
            {formatSar(summary.cash_collected_sar)}
          </span>
        </div>
        <div className="card kpi">
          <span className="muted">Approved Outreach</span>
          <span className="kpi-value">{summary.approved_outreach}</span>
        </div>
        <div className="card kpi">
          <span className="muted">Positive Replies</span>
          <span className="kpi-value">{summary.positive_replies}</span>
        </div>
        <div className="card kpi">
          <span className="muted">Proposals Due</span>
          <span className="kpi-value">{summary.proposals_due}</span>
        </div>
        <div className="card kpi">
          <span className="muted">Payment Follow-ups Due</span>
          <span className="kpi-value">{summary.payment_followups_due}</span>
        </div>
      </section>
      <p className="muted" style={{ marginTop: 24 }}>
        Last updated: {summary.last_updated}
      </p>
    </FounderShell>
  );
}
