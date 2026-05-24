import { FounderPage } from "../../components/brand/founder-page";

export default function DataPage() {
  return (
    <FounderPage
      title="Data"
      subtitle="Data platform · lineage · data moat."
      blocks={[
        { title: "Data moat", body: <p>docs/data/DATA_MOAT.md</p> },
        { title: "Intelligence base", body: <p>intelligence/lead_intelligence_base.csv</p> },
        { title: "Learning ledgers", body: <p>learning/company_memory.csv · learning/market_learning.csv</p> },
      ]}
    />
  );
}
