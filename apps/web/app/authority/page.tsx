import { FounderPage } from "../../components/brand/founder-page";

export default function AuthorityPage() {
  return (
    <FounderPage
      title="Authority"
      subtitle="Founder-led content queue · approval required."
      blocks={[
        { title: "Content queue", body: <p>campaigns/campaign_assets.csv</p> },
        { title: "Doc", body: <p>docs/marketing/AUTHORITY_CONTENT_QUEUE.md</p> },
      ]}
    />
  );
}
