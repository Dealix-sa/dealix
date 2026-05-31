// Agentic Control Plane — GEO page.
export const metadata = {
  title: "Agentic Control Plane | Dealix",
  description:
    "A runtime that wraps every AI agent action with policy, approval, and audit gates — sovereignty, trust, data, tool, outcome.",
  alternates: { canonical: "/agentic-control-plane" },
};

export default function Page() {
  return (
    <main lang="en" className="mx-auto max-w-3xl px-6 py-12">
      <h1>What is an Agentic Control Plane?</h1>
      <p>
        An agentic control plane is a runtime that mediates every action
        an AI agent proposes. Instead of letting agents execute directly,
        each call passes through gates: sovereignty, trust, data, tool,
        approval, audit, outcome.
      </p>

      <h2>The problem</h2>
      <p>
        Free-roaming agents create incidents: leaked data, unauthorized
        spend, brand-risking messages, and unbounded blast radius.
      </p>

      <h2>How Dealix implements it</h2>
      <ol>
        <li>Register each agent with explicit capabilities and forbidden actions.</li>
        <li>Wrap every tool call in <code>ControlPlaneRuntime.dispatch</code>.</li>
        <li>Route high-risk actions to the approval center.</li>
        <li>Measure outcomes and feed learning back into the system.</li>
      </ol>

      <h2>Compare</h2>
      <table>
        <thead>
          <tr><th>Concern</th><th>Plain agent framework</th><th>Dealix Control Plane</th></tr>
        </thead>
        <tbody>
          <tr><td>Identity per agent</td><td>Implicit</td><td>Formal AgentIdentity</td></tr>
          <tr><td>Capability scope</td><td>tool allowlist</td><td>capability + tool registry</td></tr>
          <tr><td>Data boundary</td><td>App-level</td><td>Per workspace</td></tr>
          <tr><td>Approval gate</td><td>None</td><td>Built-in S2/S3/S4</td></tr>
        </tbody>
      </table>

      <h2>FAQ</h2>
      <details>
        <summary>Does Dealix block agents from acting?</summary>
        <p>It blocks them from acting *without* policy clearance. The default mode is draft-only.</p>
      </details>
      <details>
        <summary>Is this open source?</summary>
        <p>The reference architecture is documented. Productized usage is governed by the Dealix license.</p>
      </details>

      <h2>Trust signals</h2>
      <ul>
        <li>Architecture docs at <a href="/docs/architecture/CONTROL_PLANE">/docs/architecture/CONTROL_PLANE</a>.</li>
        <li>Outcome registry exposed to customers under retainer.</li>
      </ul>

      <a href="/docs/architecture/CONTROL_PLANE" className="cta">See the architecture docs</a>
    </main>
  );
}
