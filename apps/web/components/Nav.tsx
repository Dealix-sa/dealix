"use client";

import Link from "next/link";

const links = [
  { href: "/", label: "الرئيسية" },
  { href: "/sales-machine", label: "آلة المبيعات" },
  { href: "/offers", label: "العروض" },
  { href: "/pricing", label: "التسعير" },
  { href: "/book", label: "احجز مراجعة" },
];

// Live operational surfaces (admin- or tenant-authenticated by route).
const commandLinks = [
  { href: "/founder/command-room", label: "غرفة القيادة" },
  { href: "/commercial-intelligence", label: "الذكاء التجاري" },
  { href: "/approvals", label: "الموافقات" },
  { href: "/evidence", label: "سجل الإثبات" },
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
        <li aria-hidden="true" style={{ opacity: 0.35 }}>·</li>
        {commandLinks.map((l) => (
          <li key={l.href}>
            <Link href={l.href}>{l.label}</Link>
          </li>
        ))}
      </ul>
      <div className="actions" style={{ marginTop: 0 }}>
        <Link href="/founder/command-room" className="btn btn-ghost" style={{ minHeight: 38, padding: "0 16px", fontSize: "0.82rem" }}>
          غرفة القيادة
        </Link>
        <Link href="/book" style={{ minHeight: 38, padding: "0 18px", fontSize: "0.82rem" }}>
          احجز مراجعة تشغيلية
        </Link>
      </div>
    </nav>
  );
}
