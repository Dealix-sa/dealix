import { FounderPage } from "../../components/brand/founder-page";

export default function CapitalAllocationPage() {
  return (
    <FounderPage
      title="Capital Allocation"
      subtitle="Double down · cut · invest."
      blocks={[
        {
          title: "Double down",
          body: (
            <ul>
              <li>ERP/CRM sector</li>
              <li>Partner referral machine</li>
              <li>Proposal follow-up worker</li>
            </ul>
          ),
        },
        {
          title: "Cut",
          body: (
            <ul>
              <li>Low-signal email angle #3</li>
              <li>Generic SaaS outreach</li>
            </ul>
          ),
        },
        {
          title: "Invest",
          body: (
            <ul>
              <li>Sales asset designer</li>
              <li>Saudi B2B researcher</li>
              <li>Payment capture automation</li>
            </ul>
          ),
        },
        { title: "Source", body: <p>finance/capital_allocation.csv · finance/roi_priority_matrix.csv</p> },
      ]}
    />
  );
}
