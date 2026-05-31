// MCP Risk Review — GEO page.
export const metadata = {
  title: "MCP Risk Review | Dealix",
  description:
    "A structured review of your MCP servers, tool descriptors, and approval routing. Audit and ship an approval-gated tool registry.",
  alternates: { canonical: "/mcp-risk-review" },
};

export default function Page() {
  return (
    <main lang="en" className="mx-auto max-w-3xl px-6 py-12">
      <h1>MCP Risk Review</h1>
      <p>
        MCP servers expose tools to LLMs with no review, no version
        pinning, and no approval gates. Dealix audits every descriptor,
        ranks risk, and ships an approval-gated tool registry.
      </p>

      <h2>How it works</h2>
      <ol>
        <li>Inventory current MCP servers and tools.</li>
        <li>Score each tool on data sensitivity and reversibility.</li>
        <li>Add approval gates for high-risk tools.</li>
        <li>Monitor descriptors for drift and reissue scores.</li>
      </ol>

      <h2>FAQ</h2>
      <details>
        <summary>Do you replace the MCP server?</summary>
        <p>No. The review and approval-gated registry sit alongside your existing servers.</p>
      </details>

      <a href="/contact?offer=mcp-risk-review" className="cta">Order the MCP Risk Review</a>
    </main>
  );
}
