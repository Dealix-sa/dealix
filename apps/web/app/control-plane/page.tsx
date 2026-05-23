import { FounderShell, SourceBadge } from "../../components/founder-shell";
import {
  getControlPlaneSummary,
  getOperatingScorecard,
} from "../../lib/dealix-runtime";

export const dynamic = "force-dynamic";

export default async function ControlPlanePage() {
  const summary = await getControlPlaneSummary();
  const scorecard = await getOperatingScorecard();
  return (
    <FounderShell title="Control Plane" source={summary.source}>
      <div className="card">
        <h2 style={{ marginTop: 0 }}>
          Operating Layer <SourceBadge source={summary.source} />
        </h2>
        <ul>
          <li>Policies (rules count): {summary.policies}</li>
          <li>Agents registered: {summary.agents}</li>
          <li>Eval suites: {summary.eval_suites}</li>
        </ul>
      </div>
      <div className="card">
        <h2>Operating Scorecard</h2>
        {"markdown" in scorecard && typeof (scorecard as { markdown?: string }).markdown === "string" ? (
          <pre style={{ whiteSpace: "pre-wrap" }}>{(scorecard as { markdown?: string }).markdown}</pre>
        ) : (
          <>
            <p>Top bottleneck: {(scorecard as { top_bottleneck?: string }).top_bottleneck}</p>
            <p>Next best action: {(scorecard as { next_best_action?: string }).next_best_action}</p>
          </>
        )}
      </div>
    </FounderShell>
  );
}
