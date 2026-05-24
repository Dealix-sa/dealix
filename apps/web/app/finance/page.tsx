import { FounderPage } from "../../components/brand/founder-page";

export default function FinancePage() {
  return (
    <FounderPage
      title="Finance"
      subtitle="Cash collected · pipeline · AI unit economics."
      blocks={[
        { title: "Cash", body: <p>finance/cash_collected.csv</p> },
        { title: "Forecast", body: <p>finance/revenue_forecast.md</p> },
        { title: "AI unit economics", body: <p>finance/ai_unit_economics.csv</p> },
        { title: "ROI priority matrix", body: <p>finance/roi_priority_matrix.csv</p> },
      ]}
    />
  );
}
