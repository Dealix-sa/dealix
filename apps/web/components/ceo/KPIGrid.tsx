import type { Counter } from "../../lib/types";

export function KPIGrid({ title, counters }: { title: string; counters: Counter[] }) {
  return (
    <div className="card">
      <h2>{title}</h2>
      <div className="metric-grid">
        {counters.map((c) => (
          <div key={c.label} className="kpi">
            <div className="label">{c.label}</div>
            <div className="value">{c.value}</div>
            {c.hint ? <div className="hint">{c.hint}</div> : null}
          </div>
        ))}
      </div>
    </div>
  );
}
