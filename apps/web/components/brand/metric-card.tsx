import type { JSX } from "react";

interface MetricCardProps {
  value: string | number;
  label: string;
  delta?: string;
  deltaDirection?: "up" | "down" | "flat";
}

export function MetricCard({
  value,
  label,
  delta,
  deltaDirection = "up",
}: MetricCardProps): JSX.Element {
  return (
    <div className="dealix-metric">
      <span className="dealix-metric__label">{label}</span>
      <span className="dealix-metric__value">{value}</span>
      {delta ? (
        <span
          className={`dealix-metric__delta${
            deltaDirection === "down" ? " dealix-metric__delta--down" : ""
          }`}
        >
          {delta}
        </span>
      ) : null}
    </div>
  );
}
