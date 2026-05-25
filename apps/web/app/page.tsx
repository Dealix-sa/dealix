const founderLinks = [
  { href: "/ceo", label: "CEO Command Center", desc: "Top action + 15 panels." },
  { href: "/sales-cockpit", label: "Sales Cockpit", desc: "Funnel + follow-ups + payment queue." },
  { href: "/approvals", label: "Approval Center", desc: "ALLOW · DENY · ESCALATE inbox." },
  { href: "/distribution", label: "Distribution", desc: "Channels × sectors × experiments." },
  { href: "/workers", label: "Workers", desc: "Revenue factory health." },
  { href: "/trust", label: "Trust", desc: "Policy decisions + audit + flags." },
  { href: "/finance", label: "Finance", desc: "Cash · MRR · pipeline · runway." },
];

const internalLinks = [
  { href: "/control-plane", label: "Control Plane" },
  { href: "/agents", label: "Agents" },
  { href: "/safety", label: "Safety" },
  { href: "/sandbox", label: "Sandbox" },
  { href: "/value-engine", label: "Value Engine" },
  { href: "/self-evolving", label: "Self-Evolving" },
];

export default function HomePage() {
  return (
    <main className="grid">
      <h1>Dealix Founder Console</h1>
      <div className="card">
        <h2>Founder P0 Surfaces</h2>
        <p>كل سطح يخدم قرار واحد لليوم. أي عمل خارجي يمرّ عبر Approval Center.</p>
        <ul>
          {founderLinks.map((link) => (
            <li key={link.href}>
              <a href={link.href}>
                <strong>{link.label}</strong>
              </a>{" "}
              — {link.desc}
            </li>
          ))}
        </ul>
      </div>
      <div className="card">
        <h2>Internal control plane</h2>
        <ul>
          {internalLinks.map((link) => (
            <li key={link.href}>
              <a href={link.href}>{link.label}</a>
            </li>
          ))}
        </ul>
      </div>
    </main>
  );
}
