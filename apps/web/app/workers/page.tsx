import { FounderShell } from "../../components/founder-shell";
import { getWorkerHealth } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function WorkersPage() {
  const data = await getWorkerHealth();
  return (
    <FounderShell title="Worker Health" source={data.source}>
      <section className="card">
        <h2>Workers</h2>
        <table>
          <thead>
            <tr>
              <th>Worker</th>
              <th>Last run</th>
              <th>Status</th>
              <th>Failures (24h)</th>
              <th>Next run</th>
              <th>Notes</th>
            </tr>
          </thead>
          <tbody>
            {data.workers.length === 0 ? (
              <tr>
                <td colSpan={6}>No worker state recorded yet.</td>
              </tr>
            ) : (
              data.workers.map((w, i) => (
                <tr key={`${w.worker}-${i}`}>
                  <td>{w.worker}</td>
                  <td>{w.last_run}</td>
                  <td>{w.status}</td>
                  <td>{w.failures_24h}</td>
                  <td>{w.next_run}</td>
                  <td>{w.notes}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </section>
    </FounderShell>
  );
}
