import { FounderShell } from "../../components/founder-shell";
import { getWorkers } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function WorkersPage() {
  const workers = await getWorkers();
  const failing = workers.filter((w) => w.status === "failing").length;
  const stale = workers.filter((w) => w.status === "stale").length;
  return (
    <FounderShell>
      <main>
        <h1>Workers</h1>
        <p>Background machine health: last run, failures, backlog, stale jobs.</p>
        <section className="founder-metric-grid">
          <div className="founder-metric">
            <p className="founder-metric__label">Total Workers</p>
            <p className="founder-metric__value">{workers.length}</p>
          </div>
          <div className="founder-metric">
            <p className="founder-metric__label">Failing</p>
            <p className="founder-metric__value">{failing}</p>
          </div>
          <div className="founder-metric">
            <p className="founder-metric__label">Stale</p>
            <p className="founder-metric__value">{stale}</p>
          </div>
        </section>
        {workers.length === 0 ? (
          <p className="founder-source" style={{ marginTop: 16 }}>
            No worker reports yet. Source: <code>/api/v1/internal/workers/health</code>.
          </p>
        ) : (
          <section className="founder-metric-grid">
            {workers.map((worker) => (
              <article key={worker.name} className="founder-metric">
                <p className="founder-metric__label">{worker.status.toUpperCase()}</p>
                <p className="founder-metric__value" style={{ fontSize: 18 }}>
                  {worker.name}
                </p>
                <p>Backlog: {worker.backlog}</p>
                <p className="founder-source">Last run: {worker.last_run ?? "never"}</p>
                {worker.error ? <p className="founder-source">Error: {worker.error}</p> : null}
              </article>
            ))}
          </section>
        )}
      </main>
    </FounderShell>
  );
}
