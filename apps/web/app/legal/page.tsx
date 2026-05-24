import { FounderPage } from "../../components/brand/founder-page";

export default function LegalPage() {
  return (
    <FounderPage
      title="Legal"
      subtitle="Commercial guardrails · contracts · privacy."
      blocks={[
        { title: "Commercial guardrails", body: <p>legal/commercial_guardrails.csv</p> },
        { title: "Doc", body: <p>docs/legal/LEGAL_OVERVIEW.md</p> },
      ]}
    />
  );
}
