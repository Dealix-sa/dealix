import type { ReactNode } from "react";
import { DealixLogo } from "../brand/DealixLogo";

export type NavItem = {
  href: string;
  label: string;
  group?: string;
};

export const FOUNDER_CONSOLE_NAV: NavItem[] = [
  { href: "/ceo", label: "CEO", group: "Command" },
  { href: "/sales-cockpit", label: "Sales Cockpit", group: "Command" },
  { href: "/distribution", label: "Distribution", group: "Command" },
  { href: "/growth", label: "Growth", group: "Command" },
  { href: "/marketing", label: "Marketing", group: "Command" },

  { href: "/approvals", label: "Approvals", group: "Trust" },
  { href: "/trust", label: "Trust", group: "Trust" },
  { href: "/audit", label: "Audit", group: "Trust" },
  { href: "/evals", label: "Evals", group: "Trust" },
  { href: "/security", label: "Security", group: "Trust" },

  { href: "/delivery", label: "Delivery", group: "Revenue" },
  { href: "/retention", label: "Retention", group: "Revenue" },
  { href: "/proof", label: "Proof", group: "Revenue" },
  { href: "/finance", label: "Finance", group: "Revenue" },
  { href: "/product", label: "Product", group: "Revenue" },

  { href: "/workers", label: "Workers", group: "Runtime" },
  { href: "/control-plane", label: "Control Plane", group: "Runtime" },
  { href: "/sovereign", label: "Sovereign", group: "Runtime" },
  { href: "/agents", label: "Agents", group: "Runtime" },
];

export function ConsoleShell({
  active,
  children,
}: {
  active?: string;
  children: ReactNode;
}) {
  const groups: string[] = [];
  for (const item of FOUNDER_CONSOLE_NAV) {
    const g = item.group ?? "";
    if (!groups.includes(g)) groups.push(g);
  }

  return (
    <div className="dx-shell">
      <aside className="dx-shell__sidebar">
        <DealixLogo variant="wordmark" height={40} />
        <nav aria-label="Founder Console">
          {groups.map((group) => (
            <div key={group} style={{ marginTop: 20 }}>
              <div
                className="dx-source"
                style={{ paddingLeft: 10, marginBottom: 6 }}
              >
                {group}
              </div>
              <div className="dx-shell__nav">
                {FOUNDER_CONSOLE_NAV.filter((n) => n.group === group).map(
                  (item) => (
                    <a
                      key={item.href}
                      href={item.href}
                      aria-current={active === item.href ? "page" : undefined}
                    >
                      {item.label}
                    </a>
                  )
                )}
              </div>
            </div>
          ))}
        </nav>
      </aside>
      <main className="dx-shell__main">{children}</main>
    </div>
  );
}
