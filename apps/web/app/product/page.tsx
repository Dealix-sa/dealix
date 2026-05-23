import { FounderShell } from "../../components/founder-shell";
import { getProductization } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function ProductPage() {
  const data = await getProductization();
  return (
    <FounderShell title="Product / Productization" source={data.source}>
      <section className="card">
        <h2>Productization candidates</h2>
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Theme</th>
              <th>Customer count</th>
              <th>Status</th>
              <th>Owner</th>
            </tr>
          </thead>
          <tbody>
            {data.candidates.length === 0 ? (
              <tr>
                <td colSpan={5}>No candidates yet.</td>
              </tr>
            ) : (
              data.candidates.map((row, i) => (
                <tr key={`${row.id ?? i}`}>
                  <td>{row.id}</td>
                  <td>{row.theme}</td>
                  <td>{row.customer_count}</td>
                  <td>{row.status}</td>
                  <td>{row.owner}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </section>
    </FounderShell>
  );
}
