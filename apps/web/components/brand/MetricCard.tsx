type Direction = "up" | "down" | "flat";

export function MetricCard({
  label,
  value,
  delta,
  direction = "flat",
  helper,
}: {
  label: string;
  value: string | number;
  delta?: string;
  direction?: Direction;
  helper?: string;
}) {
  const deltaClass =
    direction === "up"
      ? "dx-metric__delta dx-metric__delta--up"
      : direction === "down"
      ? "dx-metric__delta dx-metric__delta--down"
      : "dx-metric__delta";

  return (
    <div className="dx-card">
      <div className="dx-metric">
        <span className="dx-metric__label">{label}</span>
        <span className="dx-metric__value">{value}</span>
        {delta ? <span className={deltaClass}>{delta}</span> : null}
        {helper ? (
          <span className="dx-metric__label" style={{ textTransform: "none" }}>
            {helper}
          </span>
        ) : null}
      </div>
    </div>
  );
}
