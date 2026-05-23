import type { ReactNode } from "react";

const links: ReadonlyArray<readonly [string, string]> = [
  ["/ceo", "CEO"],
  ["/sales-cockpit", "Sales"],
  ["/approvals", "Approvals"],
  ["/workers", "Workers"],
  ["/trust", "Trust"],
  ["/finance", "Finance"],
  ["/distribution", "Distribution"],
  ["/delivery", "Delivery"],
  ["/retention", "Retention"],
  ["/proof", "Proof"],
];

type FounderShellProps = {
  children: ReactNode;
  title?: string;
};

export function FounderShell({ children, title }: FounderShellProps) {
  return (
    <div className="founder-shell">
      <aside className="founder-sidebar">
        <h2>Dealix Founder</h2>
        <nav className="founder-nav" aria-label="Founder Console">
          {links.map(([href, label]) => (
            <a key={href} href={href}>
              {label}
            </a>
          ))}
        </nav>
      </aside>
      <main className="founder-main">
        {title ? <h1>{title}</h1> : null}
        {children}
      </main>
    </div>
  );
}
