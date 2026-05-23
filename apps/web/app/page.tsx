const LEGACY_LINKS = [
  "/control-plane",
  "/agents",
  "/approvals",
  "/safety",
  "/sandbox",
  "/value-engine",
  "/self-evolving",
];

const FOUNDER_LINKS: Array<[string, string]> = [
  ["CEO", "/ceo"],
  ["Sales Cockpit", "/sales-cockpit"],
  ["Workers", "/workers"],
  ["Trust", "/trust"],
  ["Finance", "/finance"],
  ["Distribution", "/distribution"],
  ["Delivery", "/delivery"],
  ["Retention", "/retention"],
  ["Proof", "/proof"],
  ["Audit", "/audit"],
  ["Evals", "/evals"],
  ["Product · Offer Ladder", "/product"],
  ["Security", "/security"],
  ["Sovereign Readiness", "/sovereign"],
  ["Growth · Targeting", "/growth"],
  ["Marketing", "/marketing"],
  ["Customer Success", "/customer-success"],
  ["Finance Ops", "/finance-ops"],
  ["Data Platform", "/data"],
  ["Experiments", "/experiments"],
];

export default function HomePage() {
  return (
    <main className="grid">
      <h1>Dealix Enterprise Control Plane</h1>
      <div className="card">
        <p>نقطة دخول لوحات التحكم المؤسسية.</p>
        <ul>
          {LEGACY_LINKS.map((href) => (
            <li key={href}>
              <a href={href}>{href}</a>
            </li>
          ))}
        </ul>
      </div>
      <div className="card">
        <h2 style={{ marginTop: 0 }}>Dealix Founder Console</h2>
        <p>
          <strong>INTELLIGENT DEALS. REAL GROWTH.</strong>
          {" "}
          Saudi B2B Revenue Operating System. Trust-gated, human-approved execution.
        </p>
        <ul>
          {FOUNDER_LINKS.map(([label, href]) => (
            <li key={href}>
              <a href={href}>{label}</a>{" "}
              <code style={{ color: "#64748b" }}>{href}</code>
            </li>
          ))}
        </ul>
      </div>
    </main>
  );
}
