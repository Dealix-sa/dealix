// Founder Console v4 — shared shell. Every live page renders inside
// this shell so freshness, source, and a "live" badge are always
// visible. Pages without a source timestamp are not considered live.

import type { ReactNode } from "react";

type FreshnessProps = {
  source?: string | null;
  lastUpdated?: string | null;
  error?: string | null;
};

export function FreshnessBadge({ source, lastUpdated, error }: FreshnessProps) {
  if (error) {
    return (
      <span
        className="card"
        style={{
          display: "inline-block",
          padding: "4px 10px",
          background: "#fef2f2",
          borderColor: "#fecaca",
          color: "#991b1b",
          fontSize: 12
        }}
      >
        runtime offline · {error}
      </span>
    );
  }
  if (!source || !lastUpdated) {
    return (
      <span
        className="card"
        style={{
          display: "inline-block",
          padding: "4px 10px",
          background: "#fef9c3",
          borderColor: "#fde68a",
          color: "#854d0e",
          fontSize: 12
        }}
      >
        no source bound
      </span>
    );
  }
  return (
    <span
      className="card"
      style={{
        display: "inline-block",
        padding: "4px 10px",
        background: "#ecfdf5",
        borderColor: "#a7f3d0",
        color: "#065f46",
        fontSize: 12
      }}
    >
      live · {source} · {lastUpdated}
    </span>
  );
}

type FounderShellProps = {
  title: string;
  subtitle?: string;
  source?: string | null;
  lastUpdated?: string | null;
  error?: string | null;
  children: ReactNode;
};

export function FounderShell({
  title,
  subtitle,
  source,
  lastUpdated,
  error,
  children
}: FounderShellProps) {
  return (
    <main className="grid" style={{ maxWidth: 1100, margin: "0 auto" }}>
      <header
        className="card"
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          gap: 16,
          flexWrap: "wrap"
        }}
      >
        <div>
          <h1 style={{ margin: 0 }}>{title}</h1>
          {subtitle ? (
            <p style={{ margin: "4px 0 0", color: "#475569" }}>{subtitle}</p>
          ) : null}
        </div>
        <FreshnessBadge source={source} lastUpdated={lastUpdated} error={error} />
      </header>
      {children}
    </main>
  );
}

type StatProps = {
  label: string;
  value: string | number;
  hint?: string;
};

export function Stat({ label, value, hint }: StatProps) {
  return (
    <div className="card" style={{ minWidth: 160 }}>
      <div style={{ fontSize: 12, color: "#64748b" }}>{label}</div>
      <div style={{ fontSize: 28, fontWeight: 600, marginTop: 4 }}>{value}</div>
      {hint ? (
        <div style={{ fontSize: 12, color: "#94a3b8", marginTop: 4 }}>{hint}</div>
      ) : null}
    </div>
  );
}
