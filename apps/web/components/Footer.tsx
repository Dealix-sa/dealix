"use client";

import Link from "next/link";

export default function Footer() {
  return (
    <footer style={{ textAlign: "center", paddingTop: "var(--sp-8)", borderTop: "1px solid rgba(255,255,255,0.07)" }}>
      <p className="navbar-brand" style={{ justifyContent: "center", fontSize: "1.2rem", marginBottom: "var(--sp-3)" }}>
        Dealix
      </p>
      <div style={{ display: "flex", justifyContent: "center", gap: "var(--sp-4)", marginBottom: "var(--sp-4)", flexWrap: "wrap" }}>
        <Link href="/about" style={{ color: "rgba(255,255,255,0.40)", fontWeight: 500, fontSize: "0.82rem" }}>من نحن</Link>
        <Link href="/services" style={{ color: "rgba(255,255,255,0.40)", fontWeight: 500, fontSize: "0.82rem" }}>الخدمات</Link>
        <Link href="/pricing" style={{ color: "rgba(255,255,255,0.40)", fontWeight: 500, fontSize: "0.82rem" }}>التسعير</Link>
        <Link href="/contact" style={{ color: "rgba(255,255,255,0.40)", fontWeight: 500, fontSize: "0.82rem" }}>تواصل معنا</Link>
        <Link href="/book" style={{ color: "rgba(255,255,255,0.40)", fontWeight: 500, fontSize: "0.82rem" }}>احجز مراجعة</Link>
        <Link href="/safety" style={{ color: "rgba(255,255,255,0.40)", fontWeight: 500, fontSize: "0.82rem" }}>الأمان</Link>
        <Link href="/privacy" style={{ color: "rgba(255,255,255,0.40)", fontWeight: 500, fontSize: "0.82rem" }}>الخصوصية</Link>
        <Link href="/terms" style={{ color: "rgba(255,255,255,0.40)", fontWeight: 500, fontSize: "0.82rem" }}>الشروط</Link>
      </div>
      <p style={{ fontSize: "0.82rem", color: "rgba(255,255,255,0.30)" }}>
        © 2026 Dealix · Saudi-first AI Business Transformation ·{" "}
        <Link href="/privacy" style={{ color: "rgba(255,255,255,0.40)", fontWeight: 500 }}>Privacy</Link>
        {" · "}
        <Link href="/terms" style={{ color: "rgba(255,255,255,0.40)", fontWeight: 500 }}>Terms</Link>
      </p>
    </footer>
  );
}
