type MetricProps = {
  label: string;
  value: number | string;
};

export function FounderMetric({ label, value }: MetricProps) {
  return (
    <div className="founder-metric">
      <p className="founder-metric__label">{label}</p>
      <p className="founder-metric__value">{value}</p>
    </div>
  );
}
