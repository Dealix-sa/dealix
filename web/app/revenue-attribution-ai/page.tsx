// Revenue Attribution for AI Channels — GEO page.
export const metadata = {
  title: "Revenue Attribution for AI Channels | Dealix",
  description:
    "Attribute verified revenue across AI search, outbound, content, and partners using first/last/multi-touch, asset, agent, and partner influence.",
  alternates: { canonical: "/revenue-attribution-ai" },
};

export default function Page() {
  return (
    <main lang="en" className="mx-auto max-w-3xl px-6 py-12">
      <h1>Revenue Attribution for AI Channels</h1>
      <p>
        Marketing dashboards confuse pipeline with revenue, and AI
        channels are missing entirely. Dealix attributes verified revenue
        across first/last/multi-touch, asset-influenced, agent-influenced,
        and partner-influenced models.
      </p>

      <h2>How it works</h2>
      <ol>
        <li>Instrument touches across all channels.</li>
        <li>Tag assets and agents that influenced the deal.</li>
        <li>Verify revenue against payment and signed agreement.</li>
        <li>Normalize weights and feed the growth dashboard.</li>
      </ol>

      <h2>FAQ</h2>
      <details>
        <summary>What counts as verified revenue?</summary>
        <p>
          Payment received, signed agreement, retainer activated, or
          partner-paid-customer — anything else is pipeline.
        </p>
      </details>

      <a href="/docs/architecture/REVENUE_ASSURANCE" className="cta">See the attribution model</a>
    </main>
  );
}
