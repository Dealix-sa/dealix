export const dynamic = "force-dynamic";

import { FounderShell } from "../../components/founder-console/founder-shell";
import { getLayer } from "../../lib/dealix-runtime";

export default async function StrategyPage() {
  const layer = await getLayer("strategy_metrics");
  return (
    <FounderShell
      title="Strategy Metrics"
      subtitle="North-star (VOCD), input metrics, output metrics."
      source={layer.source === "live" || layer.source === "files" ? layer.source : "fallback"}
    >
      <p>
        Scorecard: <code>make strategy-scorecard</code>. Source:
        <code> docs/company/DEALIX_STRATEGY_METRICS.md</code>.
      </p>
    </FounderShell>
  );
}
