import type { WorkerRow } from "../../lib/types";

export function WorkerHealthSummary({ workers }: { workers: WorkerRow[] }) {
  const totals = workers.reduce(
    (acc, w) => {
      acc[w.status] = (acc[w.status] ?? 0) + 1;
      return acc;
    },
    { ok: 0, degraded: 0, failed: 0, idle: 0 } as Record<WorkerRow["status"], number>
  );
  return (
    <div className="card">
      <h2>Worker Health</h2>
      <p style={{ marginTop: 0 }}>
        <span className="pill pill-ok">OK {totals.ok}</span>{" "}
        <span className="pill pill-warn">Degraded {totals.degraded}</span>{" "}
        <span className="pill pill-danger">Failed {totals.failed}</span>{" "}
        <span className="pill">Idle {totals.idle}</span>
      </p>
      <p style={{ margin: 0, opacity: 0.7, fontSize: 13 }}>
        تفاصيل في <a href="/workers">/workers</a>.
      </p>
    </div>
  );
}
