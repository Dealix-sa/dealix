import { FounderShell } from "../../components/founder-shell";
import { getFinanceSummary } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

function formatSar(value: number): string {
  return value.toLocaleString("en-US") + " SAR";
}

export default async function FinancePage() {
  const finance = await getFinanceSummary();
  return (
    <FounderShell title="Finance">
      <p className="lead">
        Cash, MRR, pipeline, weighted pipeline, and payment follow-ups.
      </p>
      <section className="row">
        <div className="card kpi">
          <span className="muted">Cash Collected</span>
          <span className="kpi-value">{formatSar(finance.cash_collected_sar)}</span>
        </div>
        <div className="card kpi">
          <span className="muted">MRR</span>
          <span className="kpi-value">{formatSar(finance.mrr_sar)}</span>
        </div>
        <div className="card kpi">
          <span className="muted">Pipeline</span>
          <span className="kpi-value">{formatSar(finance.pipeline_sar)}</span>
        </div>
        <div className="card kpi">
          <span className="muted">Weighted Pipeline</span>
          <span className="kpi-value">{formatSar(finance.weighted_pipeline_sar)}</span>
        </div>
        <div className="card kpi">
          <span className="muted">Payment Follow-ups Due</span>
          <span className="kpi-value">{finance.payment_followups_due}</span>
        </div>
      </section>
    </FounderShell>
  );
}
