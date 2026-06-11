export const metadata = {
  title: "Enterprise Readiness — Dealix",
  description: "Security posture, AI governance, human review, data boundaries, and buyer FAQ for enterprise procurement.",
};

const PILLARS = [
  {
    title: "Security posture",
    body: "OIDC + SAML + SCIM + MFA scaffolds ready in the codebase. Privileged audit log on every admin action. TLS everywhere, KSA-region by default.",
    link: "/trust-center",
  },
  {
    title: "AI governance",
    body: "Deterministic by default. LLM-assist is opt-in, per customer, with provider/model/prompt-version logged on every call.",
    link: "/safety",
  },
  {
    title: "Human review",
    body: "Every outbound message — outreach, proposal, invoice, public announcement — passes a human approval gate before it leaves the workspace.",
    link: "/review-queue",
  },
  {
    title: "Data boundaries",
    body: "Customer data stays in customer systems. Dealix processes copies within the SOW scope only. Sub-processor list available on request.",
    link: "/data-room",
  },
  {
    title: "Delivery assurance",
    body: "7-day diagnostic sprint produces a written friction log and proof report. Every deliverable carries written acceptance criteria.",
    link: "/delivery-os",
  },
  {
    title: "Buyer FAQ",
    body: "Plain-language answers to the 12 most common procurement and security questions, in Arabic and English.",
    link: "/resources",
  },
];

const ARTIFACTS = [
  { name: "Security questionnaire", path: "business/enterprise/SECURITY_QUESTIONNAIRE_TEMPLATE.md" },
  { name: "Data boundary statement", path: "business/enterprise/DATA_BOUNDARY_STATEMENT.md" },
  { name: "AI governance statement", path: "business/enterprise/AI_GOVERNANCE_STATEMENT.md" },
  { name: "Human review statement", path: "business/enterprise/HUMAN_REVIEW_STATEMENT.md" },
  { name: "Service level boundaries", path: "business/enterprise/SERVICE_LEVEL_BOUNDARIES.md" },
  { name: "Implementation assurance plan", path: "business/enterprise/IMPLEMENTATION_ASSURANCE_PLAN.md" },
  { name: "Enterprise buyer FAQ (AR)", path: "business/enterprise/ENTERPRISE_BUYER_FAQ_AR.md" },
  { name: "Enterprise buyer FAQ (EN)", path: "business/enterprise/ENTERPRISE_BUYER_FAQ_EN.md" },
];

export default function EnterpriseReadinessPage() {
  return (
    <main className="mx-auto max-w-5xl px-6 py-12">
      <h1 className="text-3xl font-semibold tracking-tight">Enterprise Readiness</h1>
      <p className="mt-3 text-neutral-600">
        Every claim on this page maps to a file in the Dealix repository. Procurement and security teams
        can review the artifacts directly. No marketing wrappers, no unverifiable assertions.
      </p>

      <section className="mt-10 grid gap-5 md:grid-cols-2">
        {PILLARS.map((p) => (
          <article key={p.title} className="rounded-2xl border border-neutral-200 p-6">
            <h2 className="text-lg font-semibold">{p.title}</h2>
            <p className="mt-2 text-sm text-neutral-700">{p.body}</p>
            <a href={p.link} className="mt-3 inline-block text-sm font-medium text-blue-700 hover:underline">
              View →
            </a>
          </article>
        ))}
      </section>

      <section className="mt-12">
        <h2 className="text-xl font-semibold">Buyer-inspectable artifacts</h2>
        <ul className="mt-3 list-disc pl-6 text-sm text-neutral-700">
          {ARTIFACTS.map((a) => (
            <li key={a.path}>
              <span className="font-medium">{a.name}</span> — <code className="text-xs">{a.path}</code>
            </li>
          ))}
        </ul>
      </section>

      <section className="mt-12 rounded-2xl bg-neutral-900 p-8 text-neutral-50">
        <h2 className="text-xl font-semibold">Next step: book a workflow review</h2>
        <p className="mt-2 text-sm text-neutral-300">
          7 days. Founder-led. Written friction log + first proof report. 499 SAR.
        </p>
        <a
          href="/book"
          className="mt-4 inline-block rounded-full bg-white px-5 py-2 text-sm font-medium text-neutral-900"
        >
          Book the diagnostic sprint
        </a>
      </section>
    </main>
  );
}
