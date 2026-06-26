import { commercialLaunchControlSnapshot } from "@/lib/commercial-launch-control-snapshot";

export default function CommercialLaunchPage() {
  const data = commercialLaunchControlSnapshot;
  return (
    <main className="grid mx-auto max-w-7xl p-8">
      <section className="card card-gold dot-pattern">
        <p className="eyebrow">Dealix Commercial Launch Control</p>
        <h1>{data.verdict}</h1>
        <p style={{ maxWidth: 900 }}>
          Founder-led commercial launch view for products, sprint packages, reports, proof metrics, and merge order.
        </p>
      </section>

      <section className="cards">
        <article className="card"><p className="stat-value">{data.launch_products.length}</p><p className="stat-label">products</p></article>
        <article className="card"><p className="stat-value">{data.commercial_sprint_packages.length}</p><p className="stat-label">packages</p></article>
        <article className="card"><p className="stat-value">{data.targets_loaded}</p><p className="stat-label">targets</p></article>
        <article className="card"><p className="stat-value">{data.packs_generated}</p><p className="stat-label">packs</p></article>
      </section>

      <section className="grid-2">
        <article className="card card-gold">
          <p className="eyebrow">Launch products</p>
          <h2>What Dealix sells now</h2>
          <ul>{data.launch_products.map((item) => <li key={item}>{item}</li>)}</ul>
        </article>
        <article className="card">
          <p className="eyebrow">Founder next actions</p>
          <h2>Execution queue</h2>
          <ul>{data.founder_next_actions.map((item) => <li key={item}>{item}</li>)}</ul>
        </article>
      </section>

      <section className="card">
        <p className="eyebrow">Sprint packages</p>
        <h2>Commercial packages</h2>
        <div className="cards" style={{ marginTop: "var(--sp-6)" }}>
          {data.commercial_sprint_packages.map((item) => (
            <article className="card hover-gold" key={item.name}>
              <h3>{item.name}</h3>
              <p>{item.duration}</p>
              <p>{item.price_range_sar} SAR</p>
              <p>{item.goal}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="grid-2">
        <article className="card">
          <p className="eyebrow">Merge order</p>
          <h2>Release sequence</h2>
          <ul>{data.merge_order.map((item) => <li key={item}>{item}</li>)}</ul>
        </article>
        <article className="card">
          <p className="eyebrow">Guardrails</p>
          <h2>Launch rules</h2>
          <ul>{data.launch_guardrails.map((item) => <li key={item}>{item}</li>)}</ul>
        </article>
      </section>
    </main>
  );
}
