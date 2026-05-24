import { FounderPage } from "../../components/brand/founder-page";

export default function DeliveryPage() {
  return (
    <FounderPage
      title="Delivery"
      subtitle="Engagement state · proof pack · capital asset registration."
      blocks={[
        { title: "Sprint state", body: <p>delivery sub-agent · governance review · proof pack</p> },
        { title: "Doc", body: <p>docs/delivery/DELIVERY_OVERVIEW.md</p> },
      ]}
    />
  );
}
