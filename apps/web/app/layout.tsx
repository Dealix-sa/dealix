import "./globals.css";
import type { ReactNode } from "react";

const navLinks = [
  { href: "/ceo", label: "CEO" },
  { href: "/sales-cockpit", label: "Sales" },
  { href: "/approvals", label: "Approvals" },
  { href: "/distribution", label: "Distribution" },
  { href: "/workers", label: "Workers" },
  { href: "/trust", label: "Trust" },
  { href: "/finance", label: "Finance" },
];

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="ar">
      <body>
        <nav className="dx-nav" aria-label="Dealix founder console">
          <a href="/" style={{ fontWeight: 600 }}>
            Dealix
          </a>
          {navLinks.map((link) => (
            <a key={link.href} href={link.href}>
              {link.label}
            </a>
          ))}
        </nav>
        {children}
      </body>
    </html>
  );
}
