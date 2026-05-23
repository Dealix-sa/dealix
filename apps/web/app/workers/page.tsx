import { FounderShell, SourceBadge } from "../../components/founder-shell";
import { getWorkerHealth } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function WorkersPage() {
  const data = await getWorkerHealth();
  const workers = (data as { workers?: Array<Record<string, string>> }).workers ?? [];
  return (
    <FounderShell title="Workers" source={data.source}>
      <div className="card">
        <h2 style={{ marginTop: 0 }}>
          Worker Health <SourceBadge source={data.source} />
        </h2>
        {workers.length === 0 ? (
          <p>No worker state yet. Run a worker script in <code>scripts/</code>.</p>
        ) : (
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr>
                {["worker", "last_run", "status", "failures_24h", "next_run", "notes"].map((h) => (
                  <th key={h} style={{ textAlign: "left", borderBottom: "1px solid #e2e8f0", padding: 8 }}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {workers.map((w, i) => (
                <tr key={i}>
                  {["worker", "last_run", "status", "failures_24h", "next_run", "notes"].map((h) => (
                    <td key={h} style={{ padding: 8, borderBottom: "1px solid #f1f5f9" }}>{w[h] ?? ""}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </FounderShell>
  );
}
