import { FounderPage } from "../../components/brand/founder-page";

export default function RevenueIntelligencePage() {
  return (
    <FounderPage
      title="Revenue Intelligence"
      subtitle="Graph of accounts · contacts · signals · messages · proof · objections."
      blocks={[
        {
          title: "Nodes",
          body: (
            <ul>
              <li>graph/accounts.csv</li>
              <li>graph/contacts.csv</li>
              <li>graph/offers.csv</li>
            </ul>
          ),
        },
        {
          title: "Edges",
          body: (
            <ul>
              <li>graph/signals.csv</li>
              <li>graph/messages.csv</li>
              <li>graph/objections.csv</li>
              <li>graph/proof_edges.csv</li>
              <li>graph/partner_edges.csv</li>
              <li>graph/learnings.csv</li>
            </ul>
          ),
        },
        { title: "Report", body: <p>graph/revenue_intelligence_graph_report.md</p> },
      ]}
    />
  );
}
