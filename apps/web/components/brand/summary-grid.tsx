import type { JSX } from "react";
import { MetricCard } from "./metric-card";

interface MetricLike {
  label: string;
  value: string | number;
  delta?: string;
}

interface SummaryGridProps {
  metrics: MetricLike[];
  emptyMessage?: string;
}

export function SummaryGrid({
  metrics,
  emptyMessage = "No data yet — falls back when the private ops root is empty.",
}: SummaryGridProps): JSX.Element {
  if (!metrics || metrics.length === 0) {
    return <div className="dealix-empty">{emptyMessage}</div>;
  }
  return (
    <div className="dealix-grid dealix-grid--4">
      {metrics.map((m) => (
        <MetricCard key={m.label} value={m.value} label={m.label} delta={m.delta} />
      ))}
    </div>
  );
}
