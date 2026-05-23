import { getRiskRegister } from "../../lib/internal-client";

export const dynamic = "force-dynamic";

const SEVERITY_TONE: Record<string, string> = {
  critical: "#dc2626",
  high: "#ea580c",
  medium: "#f59e0b",
  low: "#16a34a",
};

export default async function RiskPage() {
  const data = await getRiskRegister();
  return (
    <main className="grid">
      <h1>Risk Register</h1>
      <p style={{ marginTop: -8, color: "#64748b" }}>
        Source: <strong>{data.source}</strong>
        {data.reason ? ` — ${data.reason}` : ""}
      </p>

      <section className="card">
        <p>
          Total: <strong>{data.total}</strong> · Open: <strong>{data.open ?? 0}</strong> ·
          Critical open: <strong>{data.critical_open ?? 0}</strong>
        </p>
      </section>

      <section className="card">
        {data.rows.length === 0 ? (
          <p>No risks registered. See <code>docs/risk/DEALIX_RISK_REGISTER.md</code>.</p>
        ) : (
          <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 13 }}>
            <thead>
              <tr style={{ textAlign: "left", borderBottom: "1px solid #e2e8f0" }}>
                <th>ID</th>
                <th>Category</th>
                <th>Description</th>
                <th>Severity</th>
                <th>Likelihood</th>
                <th>Owner</th>
                <th>Status</th>
                <th>Next review</th>
              </tr>
            </thead>
            <tbody>
              {data.rows.map((r, i) => (
                <tr key={r.risk_id ?? i} style={{ borderBottom: "1px solid #f1f5f9" }}>
                  <td>{r.risk_id}</td>
                  <td>{r.category}</td>
                  <td>{r.description}</td>
                  <td style={{ color: SEVERITY_TONE[(r.severity ?? "").toLowerCase()] ?? "#0f172a" }}>
                    {r.severity}
                  </td>
                  <td>{r.likelihood}</td>
                  <td>{r.owner}</td>
                  <td>{r.status}</td>
                  <td>{r.next_review}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>
    </main>
  );
}
