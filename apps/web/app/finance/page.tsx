import { FounderShell } from "../../components/founder-shell";
import { FounderMetric } from "../../components/founder-metric";
import { getFinanceSummary } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function FinancePage() {
  const summary = await getFinanceSummary();
  return (
    <FounderShell>
      <main>
        <h1>Finance</h1>
        <p>Cash, MRR, pipeline, weighted pipeline, payment follow-ups.</p>
        <p className="founder-source">Source: {summary.source}</p>
        <section className="founder-metric-grid">
          <FounderMetric label="Cash Collected (SAR)" value={summary.cash_collected_sar} />
          <FounderMetric label="MRR (SAR)" value={summary.mrr_sar} />
          <FounderMetric label="Pipeline (SAR)" value={summary.pipeline_sar} />
          <FounderMetric label="Weighted Pipeline (SAR)" value={summary.weighted_pipeline_sar} />
          <FounderMetric label="Payment Follow-ups" value={summary.payment_followups_due} />
        </section>
      </main>
    </FounderShell>
  );
}
