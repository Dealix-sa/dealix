// FounderShell — the chrome that wraps every founder console page.
// Keeps the navigation in one place so adding a new page only requires
// editing the NAV array below.

import Link from "next/link";
import type { Route } from "next";
import type { ReactNode } from "react";

type NavItem = { href: Route; label: string; group: string };

const NAV: NavItem[] = [
  { href: "/ceo", label: "CEO", group: "Pulse" },
  { href: "/sales-cockpit", label: "Sales Cockpit", group: "Pulse" },
  { href: "/approvals", label: "Approvals", group: "Pulse" },
  { href: "/workers", label: "Workers", group: "Runtime" },
  { href: "/trust", label: "Trust", group: "Runtime" },
  { href: "/audit", label: "Audit", group: "Runtime" },
  { href: "/finance", label: "Finance", group: "Revenue" },
  { href: "/distribution", label: "Distribution", group: "Revenue" },
  { href: "/delivery", label: "Delivery", group: "Revenue" },
  { href: "/retention", label: "Retention", group: "Revenue" },
  { href: "/proof", label: "Proof", group: "Revenue" },
  { href: "/control-plane", label: "Control Plane", group: "Governance" },
  { href: "/evals", label: "Evals", group: "Governance" },
  { href: "/product", label: "Product", group: "Governance" },
  { href: "/security", label: "Security", group: "Governance" },
  { href: "/sovereign", label: "Sovereign", group: "Governance" },
];

export function FounderShell({
  title,
  source,
  children,
}: {
  title: string;
  source?: string;
  children: ReactNode;
}) {
  const groups = Array.from(new Set(NAV.map((n) => n.group)));
  return (
    <div className="founder-shell">
      <aside className="founder-nav">
        <header className="brand">
          <strong>Dealix</strong>
          <span className="muted">Founder Console</span>
        </header>
        {groups.map((g) => (
          <section key={g} className="nav-group">
            <h3>{g}</h3>
            <ul>
              {NAV.filter((n) => n.group === g).map((n) => (
                <li key={n.href}>
                  <Link href={n.href}>{n.label}</Link>
                </li>
              ))}
            </ul>
          </section>
        ))}
      </aside>
      <main className="founder-main">
        <header className="page-header">
          <h1>{title}</h1>
          {source ? (
            <span className={`source source-${source}`}>source: {source}</span>
          ) : null}
        </header>
        {source === "fallback" ? (
          <div className="banner banner-warn">
            <strong>Fallback data.</strong> The internal API isn&apos;t wired or
            the private runtime is empty. This view is NOT production-ready.
            Run <code>make bootstrap-runtime</code> then restart the API.
          </div>
        ) : null}
        <div className="page-body">{children}</div>
      </main>
    </div>
  );
}

export function KV({ k, v }: { k: string; v: string | number | null | undefined }) {
  return (
    <div className="kv">
      <span className="k">{k}</span>
      <span className="v">{v ?? "—"}</span>
    </div>
  );
}
