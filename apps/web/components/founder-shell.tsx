import type { ReactNode } from "react";
import { DEALIX_BRAND, semanticColors, spacing, radii } from "../lib/brand-tokens";
import { DealixLogo } from "./brand/dealix-logo";

interface NavItem {
  href: string;
  label: string;
}

const NAV: NavItem[] = [
  { href: "/founder/ceo", label: "CEO" },
  { href: "/founder/sales", label: "Sales" },
  { href: "/founder/approvals", label: "Approvals" },
  { href: "/founder/workers", label: "Workers" },
  { href: "/founder/trust", label: "Trust" },
  { href: "/founder/finance", label: "Finance" },
  { href: "/founder/distribution", label: "Distribution" },
  { href: "/founder/delivery", label: "Delivery" },
  { href: "/founder/retention", label: "Retention" },
  { href: "/founder/proof", label: "Proof" },
  { href: "/founder/control", label: "Control" },
  { href: "/founder/audit", label: "Audit" },
  { href: "/founder/evals", label: "Evals" },
  { href: "/founder/product", label: "Product" },
  { href: "/founder/security", label: "Security" },
  { href: "/founder/sovereign", label: "Sovereign" }
];

interface FounderShellProps {
  active?: string;
  children: ReactNode;
}

export function FounderShell({ active, children }: FounderShellProps) {
  return (
    <div
      style={{
        minHeight: "100vh",
        background: semanticColors.backgroundPrimary,
        color: semanticColors.textPrimary,
        fontFamily:
          'Inter, "IBM Plex Sans Arabic", system-ui, -apple-system, sans-serif',
        display: "grid",
        gridTemplateColumns: "260px 1fr"
      }}
    >
      <aside
        style={{
          background: semanticColors.backgroundSecondary,
          borderInlineEnd: `1px solid ${semanticColors.borderSubtle}`,
          padding: spacing[6],
          display: "flex",
          flexDirection: "column",
          gap: spacing[6]
        }}
      >
        <div style={{ display: "flex", flexDirection: "column", gap: spacing[2] }}>
          <DealixLogo variant="lockup" withTagline={false} height={36} />
          <span
            style={{
              fontSize: 12,
              letterSpacing: "0.12em",
              textTransform: "uppercase",
              color: semanticColors.textSecondary
            }}
          >
            {DEALIX_BRAND.tagline}
          </span>
        </div>

        <nav aria-label="Founder navigation">
          <ul style={{ listStyle: "none", padding: 0, margin: 0, display: "grid", gap: spacing[1] }}>
            {NAV.map((item) => {
              const isActive = active === item.href || active === item.label;
              return (
                <li key={item.href}>
                  <a
                    href={item.href}
                    style={{
                      display: "block",
                      padding: `${spacing[2]} ${spacing[3]}`,
                      borderRadius: radii.md,
                      color: isActive
                        ? semanticColors.accentOnAccent
                        : semanticColors.textPrimary,
                      background: isActive
                        ? semanticColors.accentPrimary
                        : "transparent",
                      fontWeight: isActive ? 700 : 500,
                      textDecoration: "none",
                      fontSize: 14
                    }}
                  >
                    {item.label}
                  </a>
                </li>
              );
            })}
          </ul>
        </nav>

        <div
          style={{
            marginTop: "auto",
            padding: spacing[4],
            border: `1px solid ${semanticColors.borderSubtle}`,
            borderRadius: radii.md,
            background: "rgba(0, 209, 161, 0.06)",
            fontSize: 12,
            lineHeight: 1.5,
            color: semanticColors.textSecondary
          }}
        >
          <strong style={{ color: semanticColors.textPrimary }}>Trust note.</strong>
          <br />
          Every outbound action is founder-approved. Kill switch is one click away.
        </div>
      </aside>

      <main
        style={{
          padding: spacing[8],
          display: "grid",
          gap: spacing[6],
          alignContent: "start"
        }}
      >
        {children}
      </main>
    </div>
  );
}

export default FounderShell;
