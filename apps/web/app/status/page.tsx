const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "https://api.dealix.me";

const checks = [
  {
    title: "API health",
    description: "Primary backend health endpoint for live operations.",
    href: `${apiUrl}/health`
  },
  {
    title: "Control plane",
    description: "Internal operating surface for Dealix workflows.",
    href: "/control-plane"
  },
  {
    title: "Safety layer",
    description: "Approval-first and policy-governed execution surface.",
    href: "/safety"
  }
];

export default function StatusPage() {
  return (
    <main className="grid">
      <section className="card">
        <p className="eyebrow">Live operations</p>
        <h1>Dealix status</h1>
        <p>
          هذه الصفحة تجمع أهم نقاط التشغيل العامة للدومين والـ API. استخدمها كبداية سريعة بعد أي نشر أو تغيير DNS/TLS.
        </p>
      </section>

      <section className="cards" aria-label="Operational checks">
        {checks.map((check) => (
          <article className="card" key={check.href}>
            <h2>{check.title}</h2>
            <p>{check.description}</p>
            <a href={check.href}>Open check</a>
          </article>
        ))}
      </section>
    </main>
  );
}
