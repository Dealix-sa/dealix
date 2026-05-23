import { FounderShell } from "../../components/founder-shell";
import { getWorkerHealth } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function WorkersPage() {
  const workers = await getWorkerHealth();
  return (
    <FounderShell title="Workers">
      <p className="lead">
        Runtime worker status, failures, last run, and backlog.
      </p>
      {workers.length === 0 ? (
        <section className="card">No worker health data connected yet.</section>
      ) : (
        <section className="grid">
          {workers.map((worker) => (
            <article key={worker.name} className="card">
              <header style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <strong>{worker.name}</strong>
                <span className="tag">{worker.status}</span>
              </header>
              <div className="muted" style={{ marginTop: 8 }}>
                Last run: {worker.last_run ?? "never"}
              </div>
              <div style={{ marginTop: 8 }}>
                Backlog: <strong>{worker.backlog}</strong>
              </div>
              <div>
                Failures (24h): <strong>{worker.failures_24h}</strong>
              </div>
            </article>
          ))}
        </section>
      )}
    </FounderShell>
  );
}
