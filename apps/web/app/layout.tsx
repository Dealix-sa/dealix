import "./globals.css";
import "../styles/brand.css";
import type { ReactNode } from "react";
import { DealixLogo } from "../components/brand/dealix-logo";
import { brand } from "../lib/brand-tokens";

export const metadata = {
  title: "Dealix — Intelligent Deals. Real Growth.",
  description:
    "Saudi B2B Revenue Operating System for intelligent deal flow, founder-approved growth, and trust-gated AI execution.",
};

const NAV: Array<{ href: string; label: string }> = [
  { href: "/", label: "Overview" },
  { href: "/ceo", label: "CEO" },
  { href: "/sales-cockpit", label: "Sales" },
  { href: "/distribution", label: "Distribution" },
  { href: "/approvals", label: "Approvals" },
  { href: "/workers", label: "Workers" },
  { href: "/trust", label: "Trust" },
  { href: "/finance", label: "Finance" },
  { href: "/delivery", label: "Delivery" },
  { href: "/retention", label: "Retention" },
  { href: "/proof", label: "Proof" },
  { href: "/control-plane", label: "Control Plane" },
  { href: "/audit", label: "Audit" },
  { href: "/evals", label: "Evals" },
  { href: "/product", label: "Product" },
  { href: "/marketing", label: "Marketing" },
  { href: "/growth", label: "Growth" },
  { href: "/security", label: "Security" },
  { href: "/sovereign", label: "Sovereign" },
];

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="ar" dir="ltr">
      <body className="dx-shell">
        <header
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            padding: "16px 24px",
            borderBottom: "1px solid var(--dx-border)",
            background: "var(--dx-bg-surface)",
            position: "sticky",
            top: 0,
            zIndex: 10,
          }}
        >
          <a href="/" style={{ textDecoration: "none" }}>
            <DealixLogo variant="full" height={32} showTagline />
          </a>
          <div
            className="dx-muted"
            style={{
              fontSize: "0.72rem",
              letterSpacing: "0.2em",
              textTransform: "uppercase",
              maxWidth: 520,
              textAlign: "right",
            }}
          >
            {brand.positioning}
          </div>
        </header>
        <div style={{ display: "grid", gridTemplateColumns: "240px 1fr", minHeight: "calc(100vh - 70px)" }}>
          <nav
            style={{
              borderRight: "1px solid var(--dx-border)",
              background: "var(--dx-bg-surface)",
              padding: "20px 12px",
            }}
            aria-label="Founder Console"
          >
            <div
              className="dx-muted"
              style={{
                fontSize: "0.7rem",
                letterSpacing: "0.18em",
                textTransform: "uppercase",
                padding: "0 12px 8px 12px",
              }}
            >
              Founder Console
            </div>
            <ul style={{ listStyle: "none", padding: 0, margin: 0, display: "grid", gap: 2 }}>
              {NAV.map((n) => (
                <li key={n.href}>
                  <a
                    href={n.href}
                    style={{
                      display: "block",
                      padding: "8px 12px",
                      borderRadius: 8,
                      color: "var(--dx-text)",
                      textDecoration: "none",
                      fontSize: "0.95rem",
                    }}
                  >
                    {n.label}
                  </a>
                </li>
              ))}
            </ul>
          </nav>
          <main style={{ padding: 24 }}>{children}</main>
        </div>
        <footer
          style={{
            padding: "16px 24px",
            borderTop: "1px solid var(--dx-border)",
            background: "var(--dx-bg-surface)",
            color: "var(--dx-text-secondary)",
            fontSize: "0.75rem",
            display: "flex",
            justifyContent: "space-between",
          }}
        >
          <span>© {new Date().getFullYear()} Dealix. {brand.tagline}</span>
          <span>Trust-gated · Founder-approved · Saudi B2B Revenue OS</span>
        </footer>
      </body>
    </html>
  );
}
