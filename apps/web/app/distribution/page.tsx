import { FounderShell } from "../../components/founder-shell";
import { getDistributionSummary } from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function DistributionPage() {
  const dist = await getDistributionSummary();
  return (
    <FounderShell title="Distribution">
      <p className="lead">
        Channel performance, sector performance, experiments, and
        double-down decisions.
      </p>
      <section className="row">
        <div className="card kpi">
          <span className="muted">Channels</span>
          <span className="kpi-value">{dist.channels}</span>
        </div>
        <div className="card kpi">
          <span className="muted">Active Sectors</span>
          <span className="kpi-value">{dist.active_sectors}</span>
        </div>
        <div className="card kpi">
          <span className="muted">Experiments</span>
          <span className="kpi-value">{dist.experiments}</span>
        </div>
        <div className="card kpi">
          <span className="muted">Double-down</span>
          <strong>{dist.double_down ?? "—"}</strong>
        </div>
      </section>
    </FounderShell>
  );
}
