import type { JSX, ReactNode } from "react";
import Link from "next/link";
import { DealixLogo } from "./brand/dealix-logo";
import { TrustBadge } from "./brand/trust-badge";

interface NavLink {
  href: string;
  label: string;
}

const NAV_LINKS: NavLink[] = [
  { href: "/ceo", label: "CEO" },
  { href: "/sales-cockpit", label: "Sales" },
  { href: "/approvals", label: "Approvals" },
  { href: "/workers", label: "Workers" },
  { href: "/trust", label: "Trust" },
  { href: "/finance", label: "Finance" },
  { href: "/distribution", label: "Distribution" },
  { href: "/delivery", label: "Delivery" },
  { href: "/retention", label: "Retention" },
  { href: "/proof", label: "Proof" },
  { href: "/control-plane", label: "Control" },
  { href: "/audit", label: "Audit" },
  { href: "/evals", label: "Evals" },
  { href: "/product", label: "Product" },
  { href: "/security", label: "Security" },
  { href: "/sovereign", label: "Sovereign" },
  { href: "/growth", label: "Growth" },
  { href: "/marketing", label: "Marketing" },
  { href: "/customer-success", label: "Customer Success" },
  { href: "/finance-ops", label: "Finance Ops" },
];

interface FounderShellProps {
  children: ReactNode;
  active?: string;
}

export function FounderShell({ children, active }: FounderShellProps): JSX.Element {
  return (
    <div className="dealix-shell">
      <aside className="dealix-shell__sidebar">
        <div className="dealix-shell__brand">
          <DealixLogo size="md" />
          <span className="dealix-shell__tagline">Intelligent Deals. Real Growth.</span>
        </div>
        <nav className="dealix-shell__nav" aria-label="Founder console">
          {NAV_LINKS.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              style={
                active && active === link.href
                  ? { background: "rgba(0, 209, 161, 0.12)", color: "#FFFFFF" }
                  : undefined
              }
            >
              {link.label}
            </Link>
          ))}
        </nav>
      </aside>
      <div className="dealix-shell__main">
        <header className="dealix-shell__topbar">
          <div style={{ fontSize: 12, color: "var(--dealix-soft-silver)" }}>Founder Console</div>
          <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
            <TrustBadge />
            <span
              style={{
                width: 28,
                height: 28,
                borderRadius: "50%",
                background: "rgba(0, 209, 161, 0.15)",
                border: "1px solid rgba(0, 209, 161, 0.4)",
                display: "inline-flex",
                alignItems: "center",
                justifyContent: "center",
                fontSize: 11,
                fontWeight: 600,
                color: "#00D1A1",
              }}
            >
              D
            </span>
          </div>
        </header>
        <main className="dealix-shell__content">{children}</main>
      </div>
    </div>
  );
}
