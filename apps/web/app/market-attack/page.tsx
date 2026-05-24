import { FounderPage } from "../../components/brand/founder-page";

export default function MarketAttackPage() {
  return (
    <FounderPage
      title="Market Attack"
      subtitle="Beachhead · strategic accounts · message angle · scale/fix/kill."
      blocks={[
        { title: "Beachhead sector", body: <p>ERP/CRM implementers</p> },
        { title: "Top strategic accounts", body: <p>10 accounts · market_attack/strategic_accounts.csv</p> },
        {
          title: "Best message angle",
          body: <p>"Turn your implementation expertise into predictable qualified deal flow."</p>,
        },
        {
          title: "Scale / Fix / Kill",
          body: (
            <ul>
              <li>Scale ERP/CRM</li>
              <li>Fix cybersecurity</li>
              <li>Kill generic agency segment until new proof</li>
            </ul>
          ),
        },
      ]}
    />
  );
}
