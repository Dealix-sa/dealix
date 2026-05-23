import type { FinanceSnapshot } from "../../lib/types";

function fmt(sar: number): string {
  return `${sar.toLocaleString()} SAR`;
}

export function CashSnapshot({ snapshot }: { snapshot: FinanceSnapshot }) {
  return (
    <div className="card">
      <h2>Cash Snapshot</h2>
      <div className="metric-grid">
        <div className="kpi">
          <div className="label">Cash</div>
          <div className="value">{fmt(snapshot.cashSar)}</div>
        </div>
        <div className="kpi">
          <div className="label">MRR</div>
          <div className="value">{fmt(snapshot.mrrSar)}</div>
        </div>
        <div className="kpi">
          <div className="label">Pipeline</div>
          <div className="value">{fmt(snapshot.pipelineSar)}</div>
          <div className="hint">weighted {fmt(snapshot.weightedPipelineSar)}</div>
        </div>
        <div className="kpi">
          <div className="label">Payment Follow-ups</div>
          <div className="value">{fmt(snapshot.paymentFollowUpsSar)}</div>
        </div>
        <div className="kpi">
          <div className="label">Monthly Burn</div>
          <div className="value">{fmt(snapshot.monthlyBurnSar)}</div>
        </div>
        <div className="kpi">
          <div className="label">Runway</div>
          <div className="value">{snapshot.runwayMonths.toFixed(1)} mo</div>
        </div>
      </div>
    </div>
  );
}
