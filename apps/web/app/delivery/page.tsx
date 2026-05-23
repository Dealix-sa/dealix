import { FounderShell } from "../../components/founder-shell";
import { getDeliveryQueue } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function DeliveryPage() {
  const data = await getDeliveryQueue();
  return (
    <FounderShell title="Delivery" source={data.source}>
      <section className="card">
        <h2>Active proposals + delivery</h2>
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Customer</th>
              <th>Offer</th>
              <th>Status</th>
              <th>Updated</th>
            </tr>
          </thead>
          <tbody>
            {data.items.length === 0 ? (
              <tr>
                <td colSpan={5}>No active proposals.</td>
              </tr>
            ) : (
              data.items.map((row, i) => (
                <tr key={`${row.id ?? i}`}>
                  <td>{row.id}</td>
                  <td>{row.customer}</td>
                  <td>{row.offer}</td>
                  <td>{row.status}</td>
                  <td>{row.updated_at}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </section>
    </FounderShell>
  );
}
