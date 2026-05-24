import { FounderPage } from "../../components/brand/founder-page";

export default function RetentionPage() {
  return (
    <FounderPage
      title="Retention"
      subtitle="Net revenue retention · expansion map · churn signals."
      blocks={[
        { title: "Expansion map", body: <p>customer_success/expansion_map.csv</p> },
        { title: "Renewal risk", body: <p>customer_success/renewal_risk.csv</p> },
      ]}
    />
  );
}
