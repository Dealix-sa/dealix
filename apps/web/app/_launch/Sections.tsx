// Reusable server components for the Dealix commercial launch pages.
import Link from "next/link";
import type { ReactNode } from "react";
import {
  CTAS,
  HERO,
  OFFERS,
  PRINCIPLES,
  PROBLEM,
  SOLUTION,
  VERTICALS,
} from "./data";

export function JsonLd({ data }: { data: unknown }) {
  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(data) }}
    />
  );
}

export function LaunchNav() {
  const links = [
    { href: "/commercial", label: "Commercial" },
    { href: "/services", label: "Services" },
    { href: "/pricing", label: "Pricing" },
    { href: "/verticals", label: "Verticals" },
    { href: "/trust", label: "Trust" },
    { href: "/case-method", label: "Case Method" },
    { href: "/media", label: "Media" },
    { href: "/faq", label: "FAQ" },
    { href: "/contact", label: "Contact" },
  ];
  return (
    <nav aria-label="Primary" style={{ display: "flex", gap: "1rem", flexWrap: "wrap", padding: "1rem 0" }}>
      <Link href="/" style={{ fontWeight: 700 }}>Dealix</Link>
      {links.map((l) => (
        <Link key={l.href} href={l.href}>{l.label}</Link>
      ))}
    </nav>
  );
}

export function Hero({ lang = "en" }: { lang?: "en" | "ar" }) {
  const h = HERO[lang];
  return (
    <header style={{ padding: "2rem 0" }} dir={lang === "ar" ? "rtl" : "ltr"}>
      <h1>{h.title}</h1>
      <p>{h.subtitle}</p>
      <CtaStrip />
    </header>
  );
}

export function CtaStrip() {
  return (
    <div style={{ display: "flex", gap: "0.75rem", flexWrap: "wrap", margin: "1rem 0" }}>
      {CTAS.map((c) => (
        <Link
          key={c.id}
          href={c.href}
          data-cta={c.id}
          style={{ padding: "0.6rem 1rem", border: "1px solid currentColor", borderRadius: 8 }}
        >
          {c.en} — {c.ar}
        </Link>
      ))}
    </div>
  );
}

export function PrinciplesRow() {
  return (
    <ul style={{ display: "flex", gap: "1rem", flexWrap: "wrap", listStyle: "none", padding: 0 }}>
      {PRINCIPLES.map((p) => (
        <li key={p.en}><strong>{p.en}</strong> · {p.ar}</li>
      ))}
    </ul>
  );
}

export function ProblemSolution() {
  return (
    <section>
      <h2>The problem — المشكلة</h2>
      <p>{PROBLEM.en}</p>
      <p dir="rtl">{PROBLEM.ar}</p>
      <h2>The solution — الحل</h2>
      <p>{SOLUTION.en}</p>
      <p dir="rtl">{SOLUTION.ar}</p>
    </section>
  );
}

export function VerticalsGrid() {
  return (
    <section>
      <h2>First 5 verticals — أول 5 قطاعات</h2>
      <ul>
        {VERTICALS.map((v) => (
          <li key={v.slug}>
            <Link href={`/verticals/${v.slug}`}>
              <strong>{v.en}</strong> — {v.ar}
            </Link>
            <div>{v.painEn}</div>
            <div dir="rtl">{v.painAr}</div>
          </li>
        ))}
      </ul>
    </section>
  );
}

export function OffersTable() {
  return (
    <section>
      <h2>Offers (SAR) — العروض بالريال</h2>
      <table>
        <thead>
          <tr><th>Offer</th><th>العرض</th><th>Price (SAR)</th></tr>
        </thead>
        <tbody>
          {OFFERS.map((o) => (
            <tr key={o.en}><td>{o.en}</td><td dir="rtl">{o.ar}</td><td>{o.price}</td></tr>
          ))}
        </tbody>
      </table>
      <p>
        AI drafts, ranks, and recommends. The founder reviews, approves, and sends manually.
        The system never sends externally.
      </p>
    </section>
  );
}

export function LaunchFooter() {
  return (
    <footer style={{ marginTop: "3rem", padding: "1rem 0", borderTop: "1px solid currentColor" }}>
      <PrinciplesRow />
      <p>© Dealix — AI Revenue &amp; Operations OS for Saudi and GCC B2B companies.</p>
    </footer>
  );
}

export function LaunchShell({ children }: { children: ReactNode }) {
  return (
    <main style={{ maxWidth: 960, margin: "0 auto", padding: "0 1rem" }}>
      <LaunchNav />
      {children}
      <LaunchFooter />
    </main>
  );
}
