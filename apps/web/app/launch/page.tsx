import { FounderPage } from "../../components/brand/founder-page";

export default function LaunchPage() {
  return (
    <FounderPage
      title="Launch"
      subtitle="Launch readiness gate · pre-flight checklist."
      blocks={[
        { title: "Verifier", body: <p><code>scripts/verify_launch_readiness.py</code></p> },
        { title: "Execution gate", body: <p><code>scripts/verify_execution_launch_layer.py</code></p> },
        { title: "Workflow", body: <p>.github/workflows/dealix-execution-launch-layer.yml</p> },
      ]}
    />
  );
}
