import { FounderPage } from "../../components/brand/founder-page";

export default function StrategyPage() {
  return (
    <FounderPage
      title="Strategy Scorecard"
      subtitle="Strategic assumptions · validation state · decisions made."
      blocks={[
        { title: "Validated", body: <p>ERP/CRM implementers want predictable qualified deal flow.</p> },
        { title: "Open assumptions", body: <p>founder/strategic_assumptions.csv</p> },
        { title: "Decision log", body: <p>founder/decision_log.csv</p> },
      ]}
    />
  );
}
