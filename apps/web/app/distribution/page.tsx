import { FounderPage } from "../../components/brand/founder-page";

export default function DistributionPage() {
  return (
    <FounderPage
      title="Distribution"
      subtitle="Channels · machines · message performance."
      blocks={[
        { title: "Distribution machines", body: <p>growth/distribution_machines.csv</p> },
        { title: "Message performance", body: <p>growth/message_performance.csv</p> },
        { title: "Target segments", body: <p>growth/target_segments.csv</p> },
      ]}
    />
  );
}
