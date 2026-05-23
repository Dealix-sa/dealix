import {
  ConsolePage,
  PlaceholderTable,
} from "../../components/shell/ConsolePage";
import { BrandCard } from "../../components/brand/BrandCard";
import { SectionHeading } from "../../components/brand/SectionHeading";
import { MetricCard } from "../../components/brand/MetricCard";
import { loadInternal } from "../../lib/runtime-client";

type WorkerRow = {
  worker: string;
  last_run: string | null;
  status: string | null;
  failures_24h: number | null;
  next_run: string | null;
  notes?: string | null;
};

const fallback: WorkerRow[] = [
  { worker: "ceo_summary_worker", last_run: null, status: null, failures_24h: null, next_run: null },
  { worker: "sales_funnel_worker", last_run: null, status: null, failures_24h: null, next_run: null },
  { worker: "trust_flags_worker", last_run: null, status: null, failures_24h: null, next_run: null },
  { worker: "finance_summary_worker", last_run: null, status: null, failures_24h: null, next_run: null },
  { worker: "operating_scorecard_worker", last_run: null, status: null, failures_24h: null, next_run: null },
  { worker: "sovereign_readiness_worker", last_run: null, status: null, failures_24h: null, next_run: null },
  { worker: "lead_scoring_worker", last_run: null, status: null, failures_24h: null, next_run: null },
  { worker: "approval_queue_worker", last_run: null, status: null, failures_24h: null, next_run: null },
  { worker: "followup_queue_worker", last_run: null, status: null, failures_24h: null, next_run: null },
  { worker: "payment_capture_worker", last_run: null, status: null, failures_24h: null, next_run: null },
];

export default async function WorkersPage() {
  const payload = await loadInternal<WorkerRow[]>(
    "/api/v1/internal/founder/workers",
    fallback
  );

  return (
    <ConsolePage
      active="/workers"
      title="Worker Orchestrator"
      subtitle="Internal workers — schedule, freshness, failures"
      source={payload.source}
    >
      <div className="dx-grid dx-grid--cols-3">
        <MetricCard label="Total workers" value={payload.data.length} />
        <MetricCard
          label="Failing (24h)"
          value={payload.data.filter((w) => (w.failures_24h ?? 0) > 0).length}
        />
        <MetricCard
          label="Stale (>24h)"
          value={payload.data.filter((w) => !w.last_run).length}
          helper="missing or unknown last_run"
        />
      </div>

      <SectionHeading title="Worker State" />
      <BrandCard>
        <table className="dx-table">
          <thead>
            <tr>
              <th>Worker</th>
              <th>Last run</th>
              <th>Status</th>
              <th>Failures 24h</th>
              <th>Next run</th>
            </tr>
          </thead>
          <tbody>
            {payload.data.map((w) => (
              <tr key={w.worker}>
                <td>{w.worker}</td>
                <td>{w.last_run ?? "—"}</td>
                <td>{w.status ?? "—"}</td>
                <td>{w.failures_24h ?? "—"}</td>
                <td>{w.next_run ?? "—"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </BrandCard>
    </ConsolePage>
  );
}
