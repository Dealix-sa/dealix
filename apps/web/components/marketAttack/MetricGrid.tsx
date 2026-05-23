export type Metric = {
  label: string;
  value: string | number;
  hint?: string;
};

export function MetricGrid({ metrics }: { metrics: Metric[] }) {
  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))",
        gap: 12
      }}
    >
      {metrics.map((m) => (
        <div key={m.label} className="card">
          <div style={{ fontSize: 12, color: "#475569" }}>{m.label}</div>
          <div style={{ fontSize: 24, fontWeight: 700 }}>{m.value}</div>
          {m.hint ? (
            <div style={{ fontSize: 12, color: "#64748b" }}>{m.hint}</div>
          ) : null}
        </div>
      ))}
    </div>
  );
}
