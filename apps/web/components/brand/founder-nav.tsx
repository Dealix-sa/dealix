import { DealixLogo } from "./dealix-logo";

const NAV_ITEMS = [
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
  { href: "/control-plane", label: "Control Plane" },
  { href: "/audit", label: "Audit" },
  { href: "/evals", label: "Evals" },
  { href: "/product", label: "Product" },
  { href: "/security", label: "Security" },
  { href: "/sovereign", label: "Sovereign" },
  { href: "/growth", label: "Growth" },
  { href: "/marketing", label: "Marketing" },
];

export function FounderNav({ currentPath }: { currentPath?: string }) {
  return (
    <header style={{ marginBottom: 16 }}>
      <div style={{ display: "flex", alignItems: "center", gap: 16, padding: "12px 0" }}>
        <a href="/" aria-label="Dealix home" style={{ textDecoration: "none" }}>
          <DealixLogo height={28} withTagline />
        </a>
        <span className="dlx-pill dlx-pill--accent">Founder Console</span>
      </div>
      <nav className="dlx-nav" aria-label="Founder console navigation">
        {NAV_ITEMS.map((item) => (
          <a
            key={item.href}
            href={item.href}
            aria-current={currentPath === item.href ? "page" : undefined}
          >
            {item.label}
          </a>
        ))}
      </nav>
    </header>
  );
}
