import type { WorkerRow } from "../../lib/types";

function pillFor(status: WorkerRow["status"]): string {
  if (status === "ok") return "pill pill-ok";
  if (status === "degraded") return "pill pill-warn";
  if (status === "failed") return "pill pill-danger";
  return "pill";
}

export function WorkerTable({ workers }: { workers: WorkerRow[] }) {
  return (
    <div className="card">
      <h2>Revenue Factory Workers</h2>
      {workers.length === 0 ? (
        <p style={{ margin: 0, opacity: 0.7 }}>لا يوجد عمّال مُسجَّلين بعد.</p>
      ) : (
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr>
              <th align="left">Worker</th>
              <th align="left">Status</th>
              <th align="left">Last Run</th>
              <th align="left">Next Run</th>
              <th align="left">Failures</th>
              <th align="left">Backlog</th>
            </tr>
          </thead>
          <tbody>
            {workers.map((w) => (
              <tr key={w.name}>
                <td>{w.name}</td>
                <td>
                  <span className={pillFor(w.status)}>{w.status}</span>
                </td>
                <td>{w.lastRun}</td>
                <td>{w.nextRun}</td>
                <td>{w.failures}</td>
                <td>{w.backlog}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
