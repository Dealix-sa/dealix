import { startupCommandSnapshot } from "@/lib/startup-command-snapshot";

export default function StartupCommandPage() {
  const data = startupCommandSnapshot;
  return (
    <main className="grid mx-auto max-w-7xl p-8">
      <section className="card card-gold dot-pattern">
        <p className="eyebrow">Dealix Startup Command Center</p>
        <h1>{data.positioning}</h1>
        <p style={{ maxWidth: 900 }}>
          One operating view for products, target priority, founder actions, Company Brain decisions, delivery proof, and trust gates.
        </p>
      </section>

      <section className="cards">
        <article className="card"><p className="stat-value">{data.products.length}</p><p className="stat-label">products</p></article>
        <article className="card"><p className="stat-value">{data.targets_loaded}</p><p className="stat-label">targets loaded</p></article>
        <article className="card"><p className="stat-value">{data.packs_generated}</p><p className="stat-label">packs generated</p></article>
        <article className="card"><p className="stat-value">{data.mode}</p><p className="stat-label">mode</p></article>
      </section>

      <section className="card">
        <p className="eyebrow">Product system</p>
        <h2>Sellable operating systems</h2>
        <div className="cards" style={{ marginTop: "var(--sp-6)" }}>
          {data.products.map((product) => (
            <article className="card hover-gold" key={product.name}>
              <h3>{product.name}</h3>
              <p>{product.first_offer}</p>
              <p>{product.proof}</p>
              <p>{product.setup_range_sar} SAR setup</p>
            </article>
          ))}
        </div>
      </section>

      <section className="card">
        <p className="eyebrow">Priority queue</p>
        <h2>Founder review order</h2>
        <div style={{ overflowX: "auto" }}>
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <tbody>
              {data.priority_queue.map((item) => (
                <tr key={`${item.company_name}-${item.sector}`}>
                  <td style={{ padding: 10 }}>{item.priority}</td>
                  <td style={{ padding: 10 }}>{item.priority_value}</td>
                  <td style={{ padding: 10 }}>{item.company_name}</td>
                  <td style={{ padding: 10 }}>{item.recommended_offer}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <section className="card">
        <p className="eyebrow">Runbook</p>
        <h2>Regenerate command center</h2>
        {data.commands.map((command) => (
          <pre key={command} style={{ textAlign: "left" }}>{command}</pre>
        ))}
      </section>
    </main>
  );
}
