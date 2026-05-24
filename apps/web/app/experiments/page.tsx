import { FounderPage } from "../../components/brand/founder-page";

export default function ExperimentsPage() {
  return (
    <FounderPage
      title="Experiments"
      subtitle="Offer-market-fit tests · message angles · sector hypotheses."
      blocks={[
        { title: "Offer-market-fit", body: <p>market_attack/offer_market_fit_tests.csv</p> },
        { title: "Report", body: <p>market_attack/offer_market_fit_report.md</p> },
      ]}
    />
  );
}
