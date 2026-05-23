import { FounderShell, DataTable } from "../../components/founder/founder-shell";
import { getDistributionSummary } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function DistributionPage() {
  const data = await getDistributionSummary();
  return (
    <FounderShell
      title="Distribution"
      subtitle={data.double_down ? `Double-down candidate: ${data.double_down}` : undefined}
      source={data.source}
    >
      <h2 style={{ margin: 0 }}>Sectors</h2>
      <DataTable
        columns={["sector", "pipeline_sar", "wins", "win_rate", "avg_cycle_days", "samples"]}
        rows={data.sectors}
      />
      <h2 style={{ margin: 0 }}>Channels</h2>
      <DataTable
        columns={["channel", "sent", "replies", "positive_replies", "samples", "proposals", "payments"]}
        rows={data.channels}
      />
    </FounderShell>
  );
}
