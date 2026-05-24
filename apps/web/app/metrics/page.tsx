import { FounderPage } from "../../components/brand/founder-page";
import { MetricCard } from "../../components/brand/metric-card";

export default function MetricsPage() {
  return (
    <FounderPage
      title="Metrics"
      subtitle="DORA · revenue · trust · adoption."
      blocks={[
        {
          title: "Snapshot",
          body: (
            <div className="dlx-grid">
              <MetricCard label="Deployment frequency" value="—" />
              <MetricCard label="Lead time" value="—" />
              <MetricCard label="Change failure rate" value="—" />
              <MetricCard label="Recovery time" value="—" />
              <MetricCard label="Cash collected" value="—" />
              <MetricCard label="Weighted pipeline" value="—" />
            </div>
          ),
        },
        { title: "Source", body: <p>metrics/hypergrowth_metrics.csv</p> },
      ]}
    />
  );
}
