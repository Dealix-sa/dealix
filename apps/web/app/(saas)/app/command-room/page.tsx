import { commercialCommandSnapshot } from "@/lib/commercial-command-snapshot";

export default function SaasCommandRoomPage() {
  const data = commercialCommandSnapshot;
  return (
    <main className="grid mx-auto max-w-7xl p-8">
      <section className="card card-gold dot-pattern">
        <p className="eyebrow">Dealix Command Room</p>
        <h1>Founder commercial operating room</h1>
        <p style={{ maxWidth: 900 }}>
          Control room for account review, prioritization, company packs, founder actions, and proof work.
        </p>
      </section>

      <section className="cards">
        <article className="card"><p className="stat-value">{data.targetsLoaded}</p><p className="stat-label">targets loaded</p></article>
        <article className="card"><p className="stat-value">{data.packsGenerated}</p><p className="stat-label">packs generated</p></article>
        <article className="card"><p className="stat-value">{data.priorityQueue.length}</p><p className="stat-label">queue items</p></article>
        <article className="card"><p className="stat-value">{data.mode}</p><p className="stat-label">mode</p></article>
      </section>

      <section className="card">
        <p className="eyebrow">Founder queue</p>
        <h2>Top accounts</h2>
        <div style={{ overflowX: "auto" }}>
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <tbody>
              {data.priorityQueue.map((item) => (
                <tr key={`${item.company_name}-${item.sector}`}>
                  <td style={{ padding: 10 }}>{item.priority}</td>
                  <td style={{ padding: 10 }}>{item.priority_value}</td>
                  <td style={{ padding: 10 }}>{item.company_name}</td>
                  <td style={{ padding: 10 }}>{item.sector}</td>
                  <td style={{ padding: 10 }}>{item.recommended_offer}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <section className="card">
        <p className="eyebrow">Run locally</p>
        <h2>Regenerate command room data</h2>
        {data.commands.map((command) => (
          <pre key={command} style={{ textAlign: "left" }}>{command}</pre>
        ))}
      </section>
    </main>
  );
}
