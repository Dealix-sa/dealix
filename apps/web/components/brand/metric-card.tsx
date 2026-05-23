type MetricCardProps = {
  label: string;
  value: string | number;
  delta?: string;
  trend?: "up" | "down" | "flat";
  source?: string;
  hint?: string;
};

export function MetricCard({ label, value, delta, trend, source, hint }: MetricCardProps) {
  const deltaClass =
    trend === "up"
      ? "dlx-metric-delta--up"
      : trend === "down"
        ? "dlx-metric-delta--down"
        : undefined;

  return (
    <div className="dlx-card">
      <div className="dlx-metric-label">{label}</div>
      <div className="dlx-metric-value">{value}</div>
      {delta && (
        <div className={deltaClass} style={{ fontSize: 13, marginTop: 4 }}>
          {delta}
        </div>
      )}
      {hint && <div className="dlx-muted" style={{ fontSize: 12, marginTop: 8 }}>{hint}</div>}
      {source && (
        <div className="dlx-muted" style={{ fontSize: 11, marginTop: 8, opacity: 0.7 }}>
          source: {source}
        </div>
      )}
    </div>
  );
}
