import { FounderPage } from "../../components/brand/founder-page";

export default function FounderLeveragePage() {
  return (
    <FounderPage
      title="Founder Leverage"
      subtitle="Highest ROI hours · what to delegate · what to drop."
      blocks={[
        { title: "Highest ROI hour", body: <p>Enterprise partner conversations.</p> },
        { title: "Lowest ROI hour", body: <p>Manual formatting / repetitive docs.</p> },
        { title: "Delegation queue", body: <p>founder/delegation_queue.csv</p> },
        { title: "Time audit", body: <p>founder/founder_time_audit.csv</p> },
      ]}
    />
  );
}
