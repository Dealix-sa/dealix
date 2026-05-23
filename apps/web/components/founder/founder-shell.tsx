import type { ReactNode } from "react";

const NAV_LINKS: Array<{ href: string; label: string }> = [
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
  { href: "/security", label: "Security" }
];

export interface FounderShellProps {
  title: string;
  source?: string;
  subtitle?: string;
  children: ReactNode;
}

export function FounderShell({ title, source, subtitle, children }: FounderShellProps) {
  return (
    <main className="grid" style={{ gap: 16, padding: 24 }}>
      <header className="card" style={{ display: "grid", gap: 8 }}>
        <strong style={{ letterSpacing: 0.5, color: "#64748b" }}>DEALIX · FOUNDER CONSOLE</strong>
        <h1 style={{ margin: 0 }}>{title}</h1>
        {subtitle ? <p style={{ margin: 0, color: "#475569" }}>{subtitle}</p> : null}
        {source ? (
          <span
            style={{
              fontSize: 12,
              alignSelf: "flex-start",
              padding: "2px 8px",
              borderRadius: 999,
              background: source === "runtime" ? "#dcfce7" : "#fef3c7",
              color: source === "runtime" ? "#166534" : "#92400e"
            }}
          >
            source: {source}
          </span>
        ) : null}
      </header>

      <nav
        className="card"
        style={{
          display: "flex",
          gap: 12,
          flexWrap: "wrap"
        }}
      >
        {NAV_LINKS.map((link) => (
          <a key={link.href} href={link.href} style={{ color: "#0f172a", textDecoration: "none" }}>
            {link.label}
          </a>
        ))}
      </nav>

      <section className="grid" style={{ gap: 16 }}>
        {children}
      </section>

      <footer className="card" style={{ fontSize: 12, color: "#64748b" }}>
        AI prepares. Humans approve. Never claim production unless verifiers pass.
      </footer>
    </main>
  );
}

export function MetricGrid({ items }: { items: Array<{ label: string; value: string | number }> }) {
  return (
    <div
      className="grid"
      style={{
        gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))",
        gap: 12
      }}
    >
      {items.map((item) => (
        <div key={item.label} className="card">
          <div style={{ fontSize: 12, color: "#64748b" }}>{item.label}</div>
          <div style={{ fontSize: 24, fontWeight: 600 }}>{item.value}</div>
        </div>
      ))}
    </div>
  );
}

export function DataTable({
  columns,
  rows
}: {
  columns: string[];
  rows: Array<Record<string, unknown>>;
}) {
  if (rows.length === 0) {
    return (
      <div className="card" style={{ color: "#64748b" }}>
        No rows. (Bootstrap private ops + run a worker to populate.)
      </div>
    );
  }
  return (
    <div className="card" style={{ overflowX: "auto" }}>
      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr>
            {columns.map((c) => (
              <th
                key={c}
                style={{
                  textAlign: "left",
                  padding: "8px 12px",
                  borderBottom: "1px solid #e2e8f0",
                  fontSize: 12,
                  color: "#64748b"
                }}
              >
                {c}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, idx) => (
            <tr key={idx}>
              {columns.map((c) => (
                <td
                  key={c}
                  style={{
                    padding: "8px 12px",
                    borderBottom: "1px solid #f1f5f9",
                    fontSize: 13
                  }}
                >
                  {String(row[c] ?? "")}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
