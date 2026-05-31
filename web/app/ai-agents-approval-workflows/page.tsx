// AI Agents with Approval Workflows — GEO page.
export const metadata = {
  title: "AI Agents with Approval Workflows | Dealix",
  description:
    "Agents propose; humans approve; the platform audits and measures. No free-roaming bots.",
  alternates: { canonical: "/ai-agents-approval-workflows" },
};

export default function Page() {
  return (
    <main lang="en" className="mx-auto max-w-3xl px-6 py-12">
      <h1>AI Agents with Real Approval Workflows</h1>
      <p>
        Most agent stacks let LLMs act first and explain later — that
        breaks in production. Dealix routes every high-risk action
        through an approval center backed by an audit log and an
        outcome registry.
      </p>

      <h2>How it works</h2>
      <ol>
        <li>Define which capabilities are high-risk.</li>
        <li>Route them to the approval center automatically.</li>
        <li>Resolve tickets with full context and evidence.</li>
        <li>Close the loop with an Outcome record.</li>
      </ol>

      <h2>FAQ</h2>
      <details>
        <summary>Can a customer self-approve?</summary>
        <p>Yes — within the scope of their own workspace and policies. Sovereign actions remain Sami-only.</p>
      </details>

      <a href="/docs/architecture/CONTROL_PLANE" className="cta">Read the approval gate guide</a>
    </main>
  );
}
