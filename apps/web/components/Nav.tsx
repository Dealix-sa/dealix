"use client";

import Link from "next/link";

const links = [
  { href: "/", label: "الرئيسية" },
  { href: "/about", label: "من نحن" },
  { href: "/services", label: "الخدمات" },
  { href: "/pricing", label: "التسعير" },
  { href: "/contact", label: "تواصل" },
];

export default function Nav() {
  return (
    <nav className="navbar" aria-label="Primary navigation">
      <Link href="/" className="navbar-brand" aria-label="Dealix Home">
        Dealix
      </Link>
      <ul className="navbar-links" role="list">
        {links.map((l) => (
          <li key={l.href}>
            <Link href={l.href}>{l.label}</Link>
          </li>
        ))}
      </ul>
      <div className="actions" style={{ marginTop: 0 }}>
        <Link href="/book" style={{ minHeight: 38, padding: "0 18px", fontSize: "0.82rem" }}>
          احجز مراجعة تشغيلية
        </Link>
      </div>
    </nav>
  );
}
