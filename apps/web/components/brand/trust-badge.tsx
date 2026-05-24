import { StatusBadge } from "./status-badge";

export function TrustBadge({ approved }: { approved: boolean }) {
  return approved ? (
    <StatusBadge tone="ok">Trust gate · approved</StatusBadge>
  ) : (
    <StatusBadge tone="warn">Trust gate · pending approval</StatusBadge>
  );
}
