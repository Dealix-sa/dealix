import { StatusBadge } from "./status-badge";

export function TrustBadge({ approved = false, label }: { approved?: boolean; label?: string }) {
  return (
    <StatusBadge tone={approved ? "ok" : "warn"}>
      {label ?? (approved ? "Trust-Gated · Approved" : "Trust-Gated · Awaiting Approval")}
    </StatusBadge>
  );
}
