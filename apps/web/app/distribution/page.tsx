import { FounderShell, SourceBadge } from "../../components/founder-shell";
import { getDistributionSummary } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function DistributionPage() {
  const data = await getDistributionSummary();
  const channels = (data as { channels?: Array<Record<string, string>> }).channels ?? [];
  const sectors = (data as { sectors?: Array<Record<string, string>> }).sectors ?? [];
  const doubleDown = (data as { double_down?: string | null }).double_down ?? null;
  return (
    <FounderShell title="Distribution" source={data.source}>
      <div className="card">
        <h2 style={{ marginTop: 0 }}>
          Channels <SourceBadge source={data.source} />
        </h2>
        {channels.length === 0 ? <p>No channel scorecard yet.</p> : (
          <ul>{channels.map((c, i) => <li key={i}>{c.channel}: ROI {c.roi}</li>)}</ul>
        )}
        <p>Recommended double-down: <strong>{doubleDown ?? "n/a"}</strong></p>
      </div>
      <div className="card">
        <h2>Sectors</h2>
        {sectors.length === 0 ? <p>No sector data yet.</p> : (
          <ul>{sectors.map((s, i) => <li key={i}>{s.sector}: {s.signal}</li>)}</ul>
        )}
      </div>
    </FounderShell>
  );
}
