import type { JSX } from "react";

type StatusKind = "ok" | "warn" | "risk" | "info";

interface StatusBadgeProps {
  status: StatusKind;
  label: string;
}

export function StatusBadge({ status, label }: StatusBadgeProps): JSX.Element {
  return <span className={`dealix-status dealix-status-${status}`}>{label}</span>;
}
