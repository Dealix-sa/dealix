import { FounderShell } from "../../components/founder-shell";
import { getDistributionSummary } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function DistributionPage() {
  const data = await getDistributionSummary();
  return (
    <FounderShell title="Distribution" source={data.source}>
      <section className="card">
        <h2>By channel</h2>
        <table>
          <thead>
            <tr>
              <th>Channel</th>
              <th>Replies</th>
              <th>Proposals</th>
              <th>Cash (SAR)</th>
            </tr>
          </thead>
          <tbody>
            {data.by_channel.length === 0 ? (
              <tr>
                <td colSpan={4}>No channel data yet.</td>
              </tr>
            ) : (
              data.by_channel.map((c, i) => (
                <tr key={i}>
                  <td>{c.channel}</td>
                  <td>{c.replies}</td>
                  <td>{c.proposals}</td>
                  <td>{c.cash_sar}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </section>
      <section className="card">
        <h2>By sector</h2>
        <table>
          <thead>
            <tr>
              <th>Sector</th>
              <th>Replies</th>
              <th>Proposals</th>
              <th>Cash (SAR)</th>
            </tr>
          </thead>
          <tbody>
            {data.by_sector.length === 0 ? (
              <tr>
                <td colSpan={4}>No sector data yet.</td>
              </tr>
            ) : (
              data.by_sector.map((s, i) => (
                <tr key={i}>
                  <td>{s.sector}</td>
                  <td>{s.replies}</td>
                  <td>{s.proposals}</td>
                  <td>{s.cash_sar}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </section>
    </FounderShell>
  );
}
