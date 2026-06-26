"use client";

import Link from "next/link";

const links = [
  { href: "/", label: "الرئيسية" },
  { href: "/war-room", label: "غرفة الحرب" },
  { href: "/command-center", label: "Command Center" },
  { href: "/services", label: "خدماتنا" },
  { href: "/offers", label: "العروض" },
  { href: "/pricing", label: "التسعير" },
  { href: "/book", label: "احجز مراجعة" },
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
