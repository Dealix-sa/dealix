import { FounderPage } from "../../components/brand/founder-page";

export default function SalesCockpitPage() {
  return (
    <FounderPage
      title="Sales Cockpit"
      subtitle="Pipeline · stage · next action · approval state."
      blocks={[
        { title: "Stage rollup", body: <p>graph/accounts.csv · graph/contacts.csv</p> },
        { title: "Next action queue", body: <p>outreach/outreach_queue.csv · approvals/approval_queue.csv</p> },
        { title: "Reply routing", body: <p>outreach/reply_routing_queue.csv</p> },
      ]}
    />
  );
}
