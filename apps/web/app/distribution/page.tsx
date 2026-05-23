import { FounderShell } from "../../components/founder-shell";
import { FounderMetric } from "../../components/founder-metric";
import { getDistributionSummary } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function DistributionPage() {
  const summary = await getDistributionSummary();
  return (
    <FounderShell>
      <main>
        <h1>Distribution</h1>
        <p>Channels, sectors, experiments. Decide double-down, fix, or kill.</p>
        <p className="founder-source">Source: {summary.source}</p>
        <section className="founder-metric-grid">
          <FounderMetric label="Channels" value={summary.channels} />
          <FounderMetric label="Active Sectors" value={summary.active_sectors} />
          <FounderMetric label="Experiments" value={summary.experiments} />
          <FounderMetric label="Double-Down" value={summary.double_down ?? "—"} />
        </section>
      </main>
    </FounderShell>
  );
}
