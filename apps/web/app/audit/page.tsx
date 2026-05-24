import { FounderPage } from "../../components/brand/founder-page";

export default function AuditPage() {
  return (
    <FounderPage
      title="Audit"
      subtitle="Decision log · approvals · trust flags · incidents."
      blocks={[
        { title: "Decisions", body: <p>founder/decision_log.csv</p> },
        { title: "Approval decisions", body: <p>trust/approval_decisions.csv</p> },
        { title: "Incidents", body: <p>trust/incidents.csv</p> },
      ]}
    />
  );
}
