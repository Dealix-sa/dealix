"use client";

import Link from "next/link";

export default function Footer() {
  return (
    <footer style={{ textAlign: "center", paddingTop: "var(--sp-8)", borderTop: "1px solid rgba(255,255,255,0.07)" }}>
      <p className="navbar-brand" style={{ justifyContent: "center", fontSize: "1.2rem", marginBottom: "var(--sp-3)" }}>
        Dealix
      </p>
      <div style={{ display: "flex", justifyContent: "center", gap: "var(--sp-4)", marginBottom: "var(--sp-4)", flexWrap: "wrap" }}>
        <Link href="/sales-machine" style={{ color: "rgba(255,255,255,0.40)", fontWeight: 500, fontSize: "0.82rem" }}>آلة المبيعات</Link>
        <Link href="/offers" style={{ color: "rgba(255,255,255,0.40)", fontWeight: 500, fontSize: "0.82rem" }}>العروض</Link>
        <Link href="/pricing" style={{ color: "rgba(255,255,255,0.40)", fontWeight: 500, fontSize: "0.82rem" }}>التسعير</Link>
        <Link href="/book" style={{ color: "rgba(255,255,255,0.40)", fontWeight: 500, fontSize: "0.82rem" }}>احجز مراجعة</Link>
        <Link href="/safety" style={{ color: "rgba(255,255,255,0.40)", fontWeight: 500, fontSize: "0.82rem" }}>الأمان</Link>
      </div>
      <p style={{ fontSize: "0.82rem", color: "rgba(255,255,255,0.30)" }}>
        © 2026 Dealix · Saudi-first AI Revenue Operations ·{" "}
        <Link href="/safety" style={{ color: "rgba(255,255,255,0.40)", fontWeight: 500 }}>Safety</Link>
        {" · "}
        <a href="https://github.com/Dealix-sa/dealix" style={{ color: "rgba(255,255,255,0.40)", fontWeight: 500 }}>GitHub</a>
      </p>
    </footer>
  );
}
