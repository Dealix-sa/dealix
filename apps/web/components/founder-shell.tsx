import type { ReactNode } from "react";

const links: Array<[string, string]> = [
  ["/ceo", "CEO"],
  ["/sales-cockpit", "Sales"],
  ["/approvals", "Approvals"],
  ["/workers", "Workers"],
  ["/trust", "Trust"],
  ["/finance", "Finance"],
  ["/distribution", "Distribution"],
  ["/delivery", "Delivery"],
  ["/retention", "Retention"],
  ["/proof", "Proof"]
];

export function FounderShell({ children }: { children: ReactNode }) {
  return (
    <div className="founder-shell">
      <aside className="founder-shell__nav">
        <h2 className="founder-shell__title">Dealix Founder</h2>
        <p className="founder-shell__subtitle">Internal Command Layer</p>
        <nav className="founder-shell__links">
          {links.map(([href, label]) => (
            <a key={href} href={href} className="founder-shell__link">
              {label}
            </a>
          ))}
        </nav>
      </aside>
      <section className="founder-shell__main">{children}</section>
    </div>
  );
}
