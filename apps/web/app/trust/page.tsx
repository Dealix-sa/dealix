import { FounderShell } from "../../components/founder-shell";
import { getTrustFlags } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function TrustPage() {
  const data = await getTrustFlags();
  return (
    <FounderShell title="Trust Flags" source={data.source}>
      <section className="card">
        <h2>Open trust signals</h2>
        <p className="muted">
          Trust flags are emitted by agents when they detect risk
          (suppression hits, missing evidence, policy edge cases).
        </p>
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Category</th>
              <th>Severity</th>
              <th>Status</th>
              <th>Target</th>
              <th>Opened</th>
            </tr>
          </thead>
          <tbody>
            {data.flags.length === 0 ? (
              <tr>
                <td colSpan={6}>No flags recorded yet.</td>
              </tr>
            ) : (
              data.flags.map((f, i) => (
                <tr key={`${f.id ?? i}`}>
                  <td>{f.id}</td>
                  <td>{f.category}</td>
                  <td>{f.severity}</td>
                  <td>{f.status}</td>
                  <td>{f.target}</td>
                  <td>{f.opened_at}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </section>
    </FounderShell>
  );
}
