import type { ReactNode } from "react";

const FOUNDER_NAV = [
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
];

export function FounderShell({ children }: { children: ReactNode }) {
  return (
    <div className="founder-shell">
      <nav className="founder-nav" aria-label="Founder Console">
        <div className="founder-nav-brand">Dealix · Founder Console</div>
        <ul className="founder-nav-list">
          {FOUNDER_NAV.map((item) => (
            <li key={item.href}>
              <a href={item.href}>{item.label}</a>
            </li>
          ))}
        </ul>
      </nav>
      <div className="founder-shell-main">{children}</div>
    </div>
  );
}
