import { FounderPage } from "../../components/brand/founder-page";

export default function PartnerEcosystemPage() {
  return (
    <FounderPage
      title="Partner Ecosystem"
      subtitle="Channel partners · co-sell · white label · referral."
      blocks={[
        { title: "Pipeline", body: <p>partners/partner_pipeline.csv</p> },
        { title: "Ecosystem", body: <p>partners/partner_ecosystem.csv</p> },
        { title: "Co-sell", body: <p>partners/co_sell_opportunities.csv</p> },
        { title: "White label", body: <p>partners/white_label_pipeline.csv</p> },
      ]}
    />
  );
}
