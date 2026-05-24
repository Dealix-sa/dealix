import { ConsolePage } from "../../components/brand/console-page";

export const metadata = { title: "Evals — Dealix" };

export default function Page() {
  return (
    <ConsolePage
      eyebrow="Quality Operating Surface"
      title="Evals"
      description="Every agent has an eval suite. Failing evals block release. The Eval Guardian agent runs the suite on every change."
      status={{ tone: "ok", label: "gate-enforced" }}
      sections={[
        { title: "Suites", bullets: ["Brand Guardian — voice + visual conformance", "Growth Strategist — sector scoring stability", "Distribution Operator — draft quality + suppression honour", "Trust Guardian — gate coverage + prompt-injection resilience"] },
        { title: "Red team", description: "Adversarial inputs and prompt-injection drills.", bullets: ["Run weekly", "Findings tracked in audit"] },
      ]}
      trustNote="Eval failures are surfaced and routed to /approvals — they do not silently degrade production behaviour."
      related={[
        { href: "/trust", label: "Trust Center" },
        { href: "/agents", label: "Agent Registry" },
      ]}
    />
  );
}
