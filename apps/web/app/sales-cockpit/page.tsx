import { FounderShell } from "../../components/founder-shell";
import { getSalesFunnel } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function SalesCockpitPage() {
  const data = await getSalesFunnel();
  return (
    <FounderShell title="Sales Cockpit" source={data.source}>
      <section className="card">
        <h2>Funnel stages</h2>
        <table>
          <thead>
            <tr>
              <th>Stage</th>
              <th>Count</th>
            </tr>
          </thead>
          <tbody>
            {data.stages.length === 0 ? (
              <tr>
                <td colSpan={2}>No funnel data yet.</td>
              </tr>
            ) : (
              data.stages.map((s) => (
                <tr key={s.name}>
                  <td>{s.name}</td>
                  <td>{s.count}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </section>
    </FounderShell>
  );
}
