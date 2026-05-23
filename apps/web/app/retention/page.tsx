import { FounderShell } from "../../components/founder-shell";
import { getRetentionQueue } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function RetentionPage() {
  const data = await getRetentionQueue();
  return (
    <FounderShell title="Retention" source={data.source}>
      <section className="card">
        <h2>Retention flags</h2>
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Category</th>
              <th>Customer</th>
              <th>Severity</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {data.items.length === 0 ? (
              <tr>
                <td colSpan={5}>No retention flags.</td>
              </tr>
            ) : (
              data.items.map((row, i) => (
                <tr key={`${row.id ?? i}`}>
                  <td>{row.id}</td>
                  <td>{row.category}</td>
                  <td>{row.target}</td>
                  <td>{row.severity}</td>
                  <td>{row.status}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </section>
    </FounderShell>
  );
}
