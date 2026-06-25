const metrics = [
  ["100", "research capacity"],
  ["40", "source reviews"],
  ["25", "AI packs"],
  ["10", "founder queue"],
  ["3", "discovery attempts"],
  ["1", "scoped proposal"],
];

const lanes = [
  ["Pain Review", "Review sector, source, and pain hypothesis."],
  ["Priority Queue", "Rank companies by fit and readiness."],
  ["Sales Pack", "Draft, questions, and negotiation notes."],
  ["Brain Decision", "Daily founder decision and next action."],
  ["CRM Queue", "Tasks, notes, and deals after approval."],
  ["Proof Pack", "What changed and what to do next."],
];

const actions = [
  "Open reports/commercial/sales_agent_company_brain/latest.md.",
  "Review top P1 targets first.",
  "Pick three companies for discovery preparation.",
  "Prepare one proposal only after qualification.",
  "Update HubSpot or the deal ledger after every action.",
];

const commands = [
  "python scripts/commercial/run_sales_agent_company_brain_day.py",
  "python scripts/saas/run_commercial_launch_day.py",
  "python -m pytest -q tests/saas/test_sales_agent_company_brain_assets.py",
];

export default function SaasCommandRoomPage() {
  return (
    <main className="grid mx-auto max-w-7xl p-8">
      <section className="card card-gold dot-pattern">
        <p className="eyebrow">Dealix Strategic Command Room</p>
        <h1>Founder commercial command room</h1>
        <p style={{ maxWidth: 900 }}>
          Daily operating room for target review, prioritization, Sales Agent packs, Company Brain decisions,
          CRM queue, and proof work. Mode stays draft-only and founder-review-first.
        </p>
      </section>

      <section className="cards" aria-label="Daily metrics">
        {metrics.map(([value, label]) => (
          <article className="card" key={label}>
            <p className="stat-value">{value}</p>
            <p className="stat-label">{label}</p>
          </article>
        ))}
      </section>

      <section className="card" aria-labelledby="lanes-title">
        <p className="eyebrow">Operating lanes</p>
        <h2 id="lanes-title">From target review to founder decision</h2>
        <div className="cards" style={{ marginTop: "var(--sp-6)" }}>
          {lanes.map(([title, body]) => (
            <article className="card hover-gold" key={title}>
              <h3>{title}</h3>
              <p>{body}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="grid-2">
        <article className="card card-gold">
          <p className="eyebrow">Founder queue</p>
          <h2>Today actions</h2>
          <ul>
            {actions.map((action) => (
              <li key={action}>{action}</li>
            ))}
          </ul>
        </article>
        <article className="card">
          <p className="eyebrow">Run locally</p>
          <h2>Commands</h2>
          {commands.map((command) => (
            <pre key={command} style={{ textAlign: "left" }}>{command}</pre>
          ))}
        </article>
      </section>
    </main>
  );
}
