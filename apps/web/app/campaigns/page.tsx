import { FounderPage } from "../../components/brand/founder-page";

export default function CampaignsPage() {
  return (
    <FounderPage
      title="Campaigns"
      subtitle="Drafts queued for founder approval · never auto-send."
      blocks={[
        { title: "Registry", body: <p>campaigns/campaign_registry.csv</p> },
        { title: "Approval queue", body: <p>campaigns/campaign_queue.csv · approvals/approval_queue.csv</p> },
        { title: "Results", body: <p>campaigns/campaign_results.csv</p> },
      ]}
    />
  );
}
