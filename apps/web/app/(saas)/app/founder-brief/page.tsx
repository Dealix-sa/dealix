import { founderDailyBriefSnapshot } from "@/lib/founder-daily-brief-snapshot";

export default function FounderBriefPage() {
  const data = founderDailyBriefSnapshot;
  return (
    <main className="grid mx-auto max-w-7xl p-8">
      <section className="card card-gold dot-pattern">
        <p className="eyebrow">Dealix Founder Daily Brief</p>
        <h1>Daily executive decision desk</h1>
        <p style={{ maxWidth: 900 }}>{data.executive_decision}</p>
      </section>

      <section className="cards">
        <article className="card"><p className="stat-value">{data.targets_loaded}</p><p className="stat-label">targets</p></article>
        <article className="card"><p className="stat-value">{data.packs_generated}</p><p className="stat-label">packs</p></article>
        <article className="card"><p className="stat-value">{data.founder_actions.length}</p><p className="stat-label">actions</p></article>
        <article className="card"><p className="stat-value">{data.mode}</p><p className="stat-label">mode</p></article>
      </section>

      <section className="grid-2">
        <article className="card card-gold">
          <p className="eyebrow">Today actions</p>
          <h2>Founder queue</h2>
          <ul>
            {data.founder_actions.map((action) => <li key={action}>{action}</li>)}
          </ul>
        </article>
        <article className="card">
          <p className="eyebrow">Hard rules</p>
          <h2>Execution guardrails</h2>
          <ul>
            {data.hard_rules.map((rule) => <li key={rule}>{rule}</li>)}
          </ul>
        </article>
      </section>
    </main>
  );
}
