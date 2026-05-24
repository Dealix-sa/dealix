import { FounderPage } from "../../components/brand/founder-page";

export default function SecurityPage() {
  return (
    <FounderPage
      title="Security"
      subtitle="Internal API keys · secrets posture · OWASP LLM guardrails."
      blocks={[
        { title: "Posture", body: <p>security/security_status.csv</p> },
        { title: "Doc", body: <p>docs/security/SECURITY_OVERVIEW.md</p> },
      ]}
    />
  );
}
