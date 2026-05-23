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
    <div className="dealix-metric">
      <div className="dealix-metric-label">{label}</div>
      <div className="dealix-metric-value">{value}</div>
      {hint && <div style={{ color: "var(--dealix-soft-silver)", fontSize: 12, marginTop: 6 }}>{hint}</div>}
    </div>
  );
}
