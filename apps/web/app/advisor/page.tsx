import { FounderPage } from "../../components/brand/founder-page";

export default function AdvisorPage() {
  return (
    <FounderPage
      title="Advisor / Board"
      subtitle="Monthly advisor update · founder approved before sending."
      blocks={[
        { title: "Latest update", body: <p>docs/founder/MONTHLY_ADVISOR_UPDATE.md</p> },
        { title: "Generator", body: <p><code>scripts/generate_monthly_advisor_update.py</code></p> },
      ]}
    />
  );
}
