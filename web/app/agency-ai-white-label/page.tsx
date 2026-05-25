// White-Label AI for Agencies — GEO page.
export const metadata = {
  title: "White-Label AI for Agencies | Dealix",
  description:
    "Run Dealix's governed agents under your agency brand, with approved claims, delivery playbooks, and revenue share.",
  alternates: { canonical: "/agency-ai-white-label" },
};

export default function Page() {
  return (
    <main lang="en" className="mx-auto max-w-3xl px-6 py-12">
      <h1>White-Label AI for Saudi Agencies</h1>
      <p>
        Agencies want to sell AI services without building governance,
        runtime, or evidence packs from scratch. Dealix gives you a
        packaged shelf, an approved claims library, delivery playbooks,
        and a revenue-share contract.
      </p>

      <h2>How it works</h2>
      <ol>
        <li>Sign the partner agreement and select your tier.</li>
        <li>Pick from the productized package shelf.</li>
        <li>Deliver under your brand with Dealix's playbooks and evidence packs.</li>
        <li>Track verified revenue and share automatically.</li>
      </ol>

      <h2>Tiers</h2>
      <table>
        <thead><tr><th>Tier</th><th>Revenue share</th><th>Certification</th></tr></thead>
        <tbody>
          <tr><td>Referral</td><td>10%</td><td>None</td></tr>
          <tr><td>White-label</td><td>30%</td><td>Required</td></tr>
          <tr><td>Implementation</td><td>20%</td><td>Required</td></tr>
          <tr><td>Strategic</td><td>40%</td><td>Required</td></tr>
        </tbody>
      </table>

      <h2>FAQ</h2>
      <details>
        <summary>Can we say "powered by Dealix"?</summary>
        <p>Yes — the approved claims library includes co-branding lines.</p>
      </details>

      <a href="/partners/apply" className="cta">Apply to the Partner Program</a>
    </main>
  );
}
