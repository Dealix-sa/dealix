interface MetricCardProps {
  label: string;
  value: string | number;
  delta?: string;
  trend?: "up" | "down" | "flat";
  hint?: string;
}

export function MetricCard({ label, value, delta, trend = "flat", hint }: MetricCardProps) {
  const trendColor =
    trend === "up" ? "var(--dx-status-success)" :
    trend === "down" ? "var(--dx-status-danger)" :
    "var(--dx-text-secondary)";
  const arrow = trend === "up" ? "▲" : trend === "down" ? "▼" : "—";

  return (
    <article className="dx-card" style={{ minWidth: 220 }}>
      <div
        style={{
          color: "var(--dx-text-secondary)",
          fontSize: "0.75rem",
          letterSpacing: "0.12em",
          textTransform: "uppercase",
          marginBottom: 6,
        }}
      >
        {label}
      </div>
      <div className="dx-heading" style={{ fontSize: "2rem", lineHeight: 1.1 }}>
        {value}
      </div>
      {delta ? (
        <div style={{ color: trendColor, fontSize: "0.875rem", marginTop: 6 }}>
          {arrow} {delta}
        </div>
      ) : null}
      {hint ? (
        <div className="dx-muted" style={{ fontSize: "0.75rem", marginTop: 6 }}>
          {hint}
        </div>
      ) : null}
    </article>
  );
}

export default MetricCard;
