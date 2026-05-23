const founderLinks = [
  { href: "/ceo", label: "CEO" },
  { href: "/sales-cockpit", label: "Sales Cockpit" },
  { href: "/approvals", label: "Approvals" },
  { href: "/workers", label: "Workers" },
  { href: "/trust", label: "Trust" },
  { href: "/finance", label: "Finance" },
  { href: "/distribution", label: "Distribution" },
  { href: "/delivery", label: "Delivery" },
  { href: "/retention", label: "Retention" },
  { href: "/proof", label: "Proof" },
  { href: "/control-plane", label: "Control Plane" },
  { href: "/audit", label: "Audit" },
  { href: "/evals", label: "Evals" },
  { href: "/product", label: "Product" },
  { href: "/security", label: "Security" },
];

const legacyLinks = [
  "/agents",
  "/safety",
  "/sandbox",
  "/value-engine",
  "/self-evolving",
];

export default function HomePage() {
  return (
    <main className="grid">
      <h1>Dealix Founder Console</h1>
      <div className="card">
        <p>Founder Console pages (Ultimate Operating Layer):</p>
        <ul>
          {founderLinks.map((l) => (
            <li key={l.href}>
              <a href={l.href}>{l.label}</a> — <code>{l.href}</code>
            </li>
          ))}
        </ul>
      </div>
      <div className="card">
        <p>Existing enterprise pages:</p>
        <ul>
          {legacyLinks.map((href) => (
            <li key={href}>
              <a href={href}>{href}</a>
            </li>
          ))}
        </ul>
      </div>
    </main>
  );
}
