// AI Revenue Hunter — GEO page.
export const metadata = {
  title: "AI Revenue Hunter | Dealix",
  description:
    "A governed agent that researches ICPs, scores leads, and drafts proposals — without sending anything without your approval.",
  alternates: { canonical: "/ai-revenue-hunter" },
};

export default function Page() {
  return (
    <main lang="en" className="mx-auto max-w-3xl px-6 py-12">
      <h1>An AI Revenue Hunter for B2B Sales</h1>
      <p>
        The Revenue Hunter Pilot delivers a ranked list of accounts,
        evidence-backed messages, and proposal drafts — all reviewed before
        any external action.
      </p>

      <h2>How it works</h2>
      <ol>
        <li>Define ICP and offer constraints.</li>
        <li>Ingest target accounts and signals.</li>
        <li>Score and prioritize leads.</li>
        <li>Draft outbound and proposals for review.</li>
      </ol>

      <h2>Compare</h2>
      <table>
        <thead><tr><th>Capability</th><th>Generic SDR tool</th><th>Dealix Revenue Hunter</th></tr></thead>
        <tbody>
          <tr><td>Approval before external send</td><td>Optional</td><td>Required</td></tr>
          <tr><td>Evidence in proposal</td><td>Manual</td><td>Auto-attached</td></tr>
          <tr><td>Verified-revenue tracking</td><td>—</td><td>Built-in</td></tr>
        </tbody>
      </table>

      <h2>FAQ</h2>
      <details>
        <summary>Will the agent send emails on my behalf?</summary>
        <p>Not without your explicit approval. Default mode is draft-only.</p>
      </details>

      <a href="/contact?offer=revenue-hunter-pilot" className="cta">
        Book the Revenue Hunter Pilot
      </a>
    </main>
  );
}
