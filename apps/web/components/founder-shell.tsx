import type { ReactNode } from "react";

const NAV: Array<{ href: string; label: string }> = [
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

export function FounderShell({
  title,
  source,
  children,
}: {
  title: string;
  source?: string;
  children: ReactNode;
}) {
  return (
    <main className="grid">
      <header className="card">
        <h1 style={{ margin: 0 }}>{title}</h1>
        <p style={{ margin: "8px 0 0", color: "#475569" }}>
          Source: <code>{source ?? "unknown"}</code> · Founder Console
        </p>
      </header>
      <nav className="card" aria-label="Founder Console navigation">
        <ul style={{ display: "flex", flexWrap: "wrap", gap: 8, listStyle: "none", padding: 0, margin: 0 }}>
          {NAV.map((item) => (
            <li key={item.href}>
              <a href={item.href} style={{ textDecoration: "none", padding: "6px 10px", border: "1px solid #cbd5e1", borderRadius: 8 }}>
                {item.label}
              </a>
            </li>
          ))}
        </ul>
      </nav>
      <section className="grid">{children}</section>
    </main>
  );
}

export function SourceBadge({ source }: { source?: string }) {
  const color = source === "fallback" ? "#b45309" : source === "private_ops" ? "#15803d" : "#1d4ed8";
  return (
    <span style={{ background: color, color: "#fff", padding: "2px 8px", borderRadius: 999, fontSize: 12 }}>
      {source ?? "unknown"}
    </span>
  );
}
