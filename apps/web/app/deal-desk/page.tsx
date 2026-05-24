import { FounderPage } from "../../components/brand/founder-page";

export default function DealDeskPage() {
  return (
    <FounderPage
      title="Deal Desk"
      subtitle="Proposal queue · sample packs · commercial guardrails."
      blocks={[
        { title: "Proposal queue", body: <p>sales/proposal_queue.csv</p> },
        { title: "Sample queue", body: <p>sales/sample_queue.csv</p> },
        { title: "Commercial guardrails", body: <p>legal/commercial_guardrails.csv</p> },
      ]}
    />
  );
}
