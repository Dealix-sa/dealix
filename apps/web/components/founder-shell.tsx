import type { ReactNode } from "react";
import { DealixLogo } from "./brand/dealix-logo";

type NavItem = { href: string; label: string };
type NavGroup = { group: string; items: NavItem[] };

const NAV: NavGroup[] = [
  {
    group: "Founder / CEO",
    items: [
      { href: "/ceo", label: "CEO Command Center" },
      { href: "/ceo-os", label: "CEO Operating System" },
      { href: "/founder-leverage", label: "Founder Leverage" },
      { href: "/strategy", label: "Strategy Scorecard" },
      { href: "/capital-allocation", label: "Capital Allocation" },
      { href: "/advisor", label: "Advisor / Board" },
    ],
  },
  {
    group: "Revenue Factory",
    items: [
      { href: "/sales-cockpit", label: "Sales Cockpit" },
      { href: "/deal-desk", label: "Deal Desk" },
      { href: "/approvals", label: "Approvals" },
      { href: "/revenue-intelligence", label: "Revenue Intelligence" },
      { href: "/finance", label: "Finance" },
      { href: "/finance-ops", label: "Finance Ops" },
    ],
  },
  {
    group: "Market Attack",
    items: [
      { href: "/market-attack", label: "Market Attack" },
      { href: "/distribution", label: "Distribution" },
      { href: "/campaigns", label: "Campaigns" },
      { href: "/sales-assets", label: "Sales Assets" },
      { href: "/authority", label: "Authority" },
      { href: "/launch", label: "Launch" },
    ],
  },
  {
    group: "Scale / Moat",
    items: [
      { href: "/moat", label: "Moat Scorecard" },
      { href: "/playbooks", label: "Playbooks" },
      { href: "/proof-library", label: "Proof Library" },
      { href: "/partner-ecosystem", label: "Partner Ecosystem" },
      { href: "/productization", label: "Productization" },
      { href: "/customer-success", label: "Customer Success" },
      { href: "/delivery", label: "Delivery" },
      { href: "/retention", label: "Retention" },
    ],
  },
  {
    group: "Trust & AI",
    items: [
      { href: "/trust", label: "Trust" },
      { href: "/ai-governance", label: "AI Governance" },
      { href: "/workers", label: "Workers / Machines" },
      { href: "/proof", label: "Proof System" },
      { href: "/data", label: "Data" },
      { href: "/experiments", label: "Experiments" },
      { href: "/security", label: "Security" },
      { href: "/audit", label: "Audit" },
      { href: "/metrics", label: "Metrics" },
      { href: "/legal", label: "Legal" },
      { href: "/settings", label: "Settings" },
    ],
  },
];

export function FounderShell({ children }: { children: ReactNode }) {
  return (
    <div className="dlx-shell">
      <aside className="dlx-sidebar">
        <div className="dlx-logo">
          <DealixLogo />
        </div>
        {NAV.map((group) => (
          <div key={group.group}>
            <div className="dlx-nav-group">{group.group}</div>
            {group.items.map((item) => (
              <a key={item.href} href={item.href}>
                {item.label}
              </a>
            ))}
          </div>
        ))}
      </aside>
      <main className="dlx-main">{children}</main>
    </div>
  );
}
