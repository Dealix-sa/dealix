import { FounderShell, SourceBadge } from "../../components/founder-shell";
import { getSalesFunnel } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function SalesCockpitPage() {
  const data = await getSalesFunnel();
  const stages = (data as { stages?: Array<{ name: string; count: number }> }).stages ?? [];
  return (
    <FounderShell title="Sales Cockpit" source={data.source}>
      <div className="card">
        <h2 style={{ marginTop: 0 }}>
          Revenue Funnel <SourceBadge source={data.source} />
        </h2>
        {stages.length === 0 ? (
          <p>No funnel data yet. Run <code>make bootstrap-runtime</code>.</p>
        ) : (
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr>
                <th style={{ textAlign: "left", borderBottom: "1px solid #e2e8f0", padding: 8 }}>Stage</th>
                <th style={{ textAlign: "right", borderBottom: "1px solid #e2e8f0", padding: 8 }}>Count</th>
              </tr>
            </thead>
            <tbody>
              {stages.map((s) => (
                <tr key={s.name}>
                  <td style={{ padding: 8 }}>{s.name}</td>
                  <td style={{ padding: 8, textAlign: "right" }}>{s.count}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </FounderShell>
  );
}
