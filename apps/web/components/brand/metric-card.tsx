export function MetricCard({
  label,
  value,
  hint,
}: {
  label: string;
  value: string | number;
  hint?: string;
}) {
  return (
    <div className="dlx-card" style={{ marginBottom: 0 }}>
      <div className="dlx-metric">
        <span className="dlx-metric-value">{value}</span>
        <span className="dlx-metric-label">{label}</span>
      </div>
      {hint ? <div className="dlx-source">{hint}</div> : null}
    </div>
  );
}
