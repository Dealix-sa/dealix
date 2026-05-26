const siteUrl = process.env.NEXT_PUBLIC_SITE_URL ?? "https://dealix.me";

const productAreas = [
  {
    title: "Revenue OS",
    description: "Lead acquisition, ICP scoring, outreach, pipeline visibility, and Saudi B2B growth workflows.",
    href: "/control-plane"
  },
  {
    title: "Agent Governance",
    description: "Approval-first AI execution with audit trails, safety gates, and no blind external commitments.",
    href: "/agents"
  },
  {
    title: "Trust & Safety",
    description: "PDPL-aware controls, approval classes, evidence packs, and live operational guardrails.",
    href: "/safety"
  },
  {
    title: "Value Engine",
    description: "Business-value tracking, executive dashboards, proof curation, and operational scorecards.",
    href: "/value-engine"
  }
];

const operationalLinks = [
  ["Control plane", "/control-plane"],
  ["Agents", "/agents"],
  ["Approvals", "/approvals"],
  ["Safety", "/safety"],
  ["Sandbox", "/sandbox"],
  ["Value engine", "/value-engine"],
  ["Self-evolving OS", "/self-evolving"]
];

const structuredData = {
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  name: "Dealix",
  applicationCategory: "BusinessApplication",
  operatingSystem: "Web",
  url: siteUrl,
  description:
    "Saudi-first B2B revenue, growth, and compliance engine with approval-first AI execution.",
  areaServed: {
    "@type": "Country",
    name: "Saudi Arabia"
  },
  offers: {
    "@type": "Offer",
    priceCurrency: "SAR",
    availability: "https://schema.org/InStock"
  },
  publisher: {
    "@type": "Organization",
    name: "Dealix",
    url: siteUrl
  }
};

export default function HomePage() {
  return (
    <main className="grid">
      <script
        type="application/ld+json"
        suppressHydrationWarning
        dangerouslySetInnerHTML={{ __html: JSON.stringify(structuredData) }}
      />

      <section className="card" aria-labelledby="hero-title">
        <p className="eyebrow">Saudi-first · Approval-first · Revenue-focused</p>
        <h1 id="hero-title">Dealix Enterprise Control Plane</h1>
        <p>
          Dealix is a Saudi B2B revenue, growth, and compliance engine for teams that need AI assistance without losing policy control, auditability, or human approval on critical moves.
        </p>
        <div className="actions" aria-label="Primary actions">
          <a href="/control-plane">Open control plane</a>
          <a href="/safety">Review safety layer</a>
        </div>
      </section>

      <section aria-labelledby="areas-title">
        <h2 id="areas-title">Core operating areas</h2>
        <div className="cards">
          {productAreas.map((area) => (
            <article className="card" key={area.href}>
              <h3>{area.title}</h3>
              <p>{area.description}</p>
              <a href={area.href}>Open {area.title}</a>
            </article>
          ))}
        </div>
      </section>

      <section className="card" aria-labelledby="ops-title">
        <h2 id="ops-title">Operational surfaces</h2>
        <p>Use these internal surfaces to inspect agents, approvals, safety, sandbox behavior, and value tracking.</p>
        <ul>
          {operationalLinks.map(([label, href]) => (
            <li key={href}>
              <a href={href}>{label}</a>
            </li>
          ))}
        </ul>
      </section>
    </main>
  );
}
