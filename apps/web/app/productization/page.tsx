import { FounderPage } from "../../components/brand/founder-page";

export default function ProductizationPage() {
  return (
    <FounderPage
      title="Productization"
      subtitle="From services to repeatable offers · candidates · pipeline."
      blocks={[
        { title: "Offer ladder", body: <p>product/offer_ladder.csv</p> },
        { title: "Distribution", body: <p>product/product_distribution.csv</p> },
        { title: "Candidates", body: <p>product/productization_candidates.csv</p> },
        { title: "Pipeline", body: <p>product/productization_pipeline.csv</p> },
      ]}
    />
  );
}
