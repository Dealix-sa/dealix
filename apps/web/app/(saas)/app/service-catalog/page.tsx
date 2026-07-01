import { serviceCatalogSnapshot } from "@/lib/service-catalog-snapshot";

export default function ServiceCatalogPage() {
  const data = serviceCatalogSnapshot;
  return (
    <main className="grid mx-auto max-w-7xl p-8">
      <section className="card card-gold dot-pattern">
        <p className="eyebrow">Dealix Service Catalog</p>
        <h1>17 Offerings — Single Source of Truth</h1>
        <p style={{ maxWidth: 900 }}>
          Canonical offering registry (Wave 13). All pricing is an estimate range.
          Every offering enforces <code>no_live_send</code> and <code>no_live_charge</code>.
        </p>
      </section>

      <section className="cards">
        <article className="card">
          <p className="stat-value">{data.total_offerings}</p>
          <p className="stat-label">total offerings</p>
        </article>
        <article className="card">
          <p className="stat-value">{data.funnel_offerings.length}</p>
          <p className="stat-label">core funnel</p>
        </article>
        <article className="card">
          <p className="stat-value">{data.transformation_offerings.length}</p>
          <p className="stat-label">enterprise OS</p>
        </article>
      </section>

      <section className="card card-gold">
        <p className="eyebrow">Core Funnel (7 offerings)</p>
        <h2>From Free to Executive</h2>
        <div className="cards" style={{ marginTop: "var(--sp-6)" }}>
          {data.funnel_offerings.map((o) => (
            <article className="card hover-gold" key={o.id}>
              <p className="eyebrow">{o.customer_journey_stage}</p>
              <h3>{o.name_en}</h3>
              <p style={{ fontSize: "0.8rem", color: "var(--color-text-muted)" }}>{o.name_ar}</p>
              <p className="stat-value" style={{ fontSize: "1.4rem" }}>
                {o.price_sar === 0 ? "Free" : `${o.price_sar.toLocaleString()} SAR`}
              </p>
              <p style={{ fontSize: "0.8rem" }}>{o.kpi_commitment_en}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="card">
        <p className="eyebrow">Enterprise Transformation OS (10 offerings)</p>
        <h2>Sector-Scale Systems</h2>
        <ul style={{ marginTop: "var(--sp-4)" }}>
          {data.transformation_offerings.map((o) => (
            <li key={o.id} style={{ marginBottom: "var(--sp-3)" }}>
              <strong>{o.name_en}</strong>
              {" — "}
              <span style={{ color: "var(--color-text-muted)" }}>{o.name_ar}</span>
              <br />
              <span style={{ fontSize: "0.85rem" }}>
                {"price_sar_max" in o
                  ? `${o.price_sar.toLocaleString()}–${(o as any).price_sar_max.toLocaleString()} SAR setup`
                  : `${o.price_sar.toLocaleString()} SAR`}
                {" · "}
                {o.duration_days > 0 ? `${o.duration_days} days` : "ongoing"}
              </span>
            </li>
          ))}
        </ul>
      </section>

      <section className="card">
        <p className="eyebrow">Hard Gates</p>
        <h2>Immutable across all 17 offerings</h2>
        <ul style={{ marginTop: "var(--sp-4)", columns: 2 }}>
          {data.funnel_offerings[0]?.hard_gates.map((gate) => (
            <li key={gate} style={{ color: "var(--color-success)", fontFamily: "monospace" }}>
              {gate}
            </li>
          ))}
        </ul>
      </section>
    </main>
  );
}
