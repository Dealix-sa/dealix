import type { ReactNode } from "react";
import "../styles/brand.css";
import { DealixLogo } from "./brand/dealix-logo";

const NAV = [
  ["CEO", "/ceo"],
  ["Sales", "/sales-cockpit"],
  ["Approvals", "/approvals"],
  ["Workers", "/workers"],
  ["Trust", "/trust"],
  ["Finance", "/finance"],
  ["Distribution", "/distribution"],
  ["Delivery", "/delivery"],
  ["Retention", "/retention"],
  ["Proof", "/proof"],
  ["Control", "/control-plane"],
  ["Audit", "/audit"],
  ["Evals", "/evals"],
  ["Product", "/product"],
  ["Security", "/security"],
  ["Sovereign", "/sovereign"],
  ["Growth", "/growth"],
  ["Marketing", "/marketing"],
  ["Customer Success", "/customer-success"],
  ["Finance Ops", "/finance-ops"],
  ["Data", "/data"],
  ["Experiments", "/experiments"],
] as const;

export function FounderShell({ children, title }: { children: ReactNode; title?: string }) {
  return (
    <div className="dealix-shell">
      <header className="dealix-header">
        <DealixLogo size={28} showTagline />
        <span className="dealix-badge ok">Founder Console</span>
      </header>
      <nav className="dealix-nav" aria-label="Founder navigation">
        {NAV.map(([label, href]) => (
          <a key={href} href={href}>
            {label}
          </a>
        ))}
      </nav>
      <main className="dealix-main">
        {title && <h1 className="dealix-section-heading" style={{ fontSize: 24 }}>{title}</h1>}
        {children}
      </main>
    </div>
  );
}
