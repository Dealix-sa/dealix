"use client";

export default function MetricCard({ value, label }: { value: string; label: string }) {
  return (
    <div className="card" style={{ textAlign: "center", padding: "var(--sp-6) var(--sp-4)" }}>
      <div className="stat-value">{value}</div>
      <p className="stat-label">{label}</p>
    </div>
  );
}
