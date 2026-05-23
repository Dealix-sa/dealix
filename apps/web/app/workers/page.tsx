import { FounderShell } from "../../components/founder-shell";
import { getWorkersHealth } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function WorkersPage() {
  const workers = await getWorkersHealth();
  return (
    <FounderShell>
      <main className="p-8">
        <h1 className="text-4xl font-bold">Workers</h1>
        <p className="mt-2 max-w-3xl">
          Health snapshot of every runtime worker. A red row means an
          operating loop is silently broken.
        </p>
        <section className="mt-8 rounded-2xl border p-6">
          {workers.length === 0 ? (
            <p>No worker heartbeats yet. Start runtime workers to populate this view.</p>
          ) : (
            <table className="w-full text-sm">
              <thead>
                <tr>
                  <th className="text-left">Worker</th>
                  <th className="text-left">Status</th>
                  <th className="text-left">Last heartbeat</th>
                  <th className="text-left">Notes</th>
                </tr>
              </thead>
              <tbody>
                {workers.map((w) => (
                  <tr key={w.worker}>
                    <td>{w.worker}</td>
                    <td>{w.status}</td>
                    <td>{w.last_heartbeat}</td>
                    <td>{w.notes ?? ""}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </section>
        <p className="mt-6 text-xs">
          Source: worker_health_logs · Endpoint: /api/v1/internal/workers/health
        </p>
      </main>
    </FounderShell>
  );
}
