import { FounderShell } from "../../components/founder-shell";
import { BrandCard } from "../../components/brand/brand-card";
import { StatusBadge } from "../../components/brand/status-badge";
import { getWorkerHealth } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function WorkersPage() {
  const res = await getWorkerHealth();
  return (
    <FounderShell title="Workers">
      <BrandCard title="Worker health" subtitle="From runtime/worker_state.csv" source={res.source}>
        {res.data.workers.length === 0 ? (
          <p style={{ color: "var(--dealix-soft-silver)" }}>
            No workers reported. Run a worker (e.g. scripts/run_ceo_summary_worker.py) to populate this view.
          </p>
        ) : (
          <table className="dealix-table">
            <thead>
              <tr>
                <th>Id</th>
                <th>Name</th>
                <th>Status</th>
                <th>Last run</th>
                <th>Failures</th>
              </tr>
            </thead>
            <tbody>
              {res.data.workers.map((w) => (
                <tr key={w.id}>
                  <td>{w.id}</td>
                  <td>{w.name}</td>
                  <td>
                    <StatusBadge tone={w.status === "ok" ? "ok" : w.status === "failed" ? "danger" : "warn"}>
                      {w.status}
                    </StatusBadge>
                  </td>
                  <td>{w.last_run ?? "—"}</td>
                  <td>{w.failure_count}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </BrandCard>
    </FounderShell>
  );
}
