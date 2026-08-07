"use client";

import Link from "next/link";

export default function CTA({ href, label, secondary }: { href: string; label: string; secondary?: string }) {
  return (
    <div className="actions" style={{ marginTop: "var(--sp-6)" }}>
      <Link href={href}>{label}</Link>
      {secondary && <Link href={secondary} style={{ minHeight: 46 }}>تعرف أكثر</Link>}
    </div>
  );
}
