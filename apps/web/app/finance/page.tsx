import { FounderShell, SourceBadge } from "../../components/founder-shell";
import { getFinanceSummary } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function FinancePage() {
  const s = await getFinanceSummary();
  return (
    <FounderShell title="Finance" source={s.source}>
      <div className="card">
        <h2 style={{ marginTop: 0 }}>
          Finance Snapshot <SourceBadge source={s.source} />
        </h2>
        <ul>
          <li>Cash collected: {s.cash_total}</li>
          <li>MRR: {s.mrr}</li>
          <li>Pipeline: {s.pipeline}</li>
          <li>Weighted pipeline: {s.weighted_pipeline}</li>
          <li>Payment follow-ups due: {s.payment_followups}</li>
        </ul>
      </div>
    </FounderShell>
  );
}
