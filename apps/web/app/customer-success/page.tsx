import { FounderPage } from "../../components/brand/founder-page";

export default function CustomerSuccessPage() {
  return (
    <FounderPage
      title="Customer Success"
      subtitle="Client health · referrals · expansion · renewal risk."
      blocks={[
        { title: "Health", body: <p>customer_success/client_health.csv</p> },
        { title: "Referrals", body: <p>customer_success/referral_queue.csv</p> },
        { title: "Expansion", body: <p>customer_success/expansion_opportunities.csv</p> },
        { title: "Renewal risk", body: <p>customer_success/renewal_risk.csv</p> },
      ]}
    />
  );
}
