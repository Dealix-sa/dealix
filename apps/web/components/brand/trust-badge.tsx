import type { JSX } from "react";

interface TrustBadgeProps {
  label?: string;
}

export function TrustBadge({ label = "Trust-Gated" }: TrustBadgeProps): JSX.Element {
  return (
    <span className="dealix-trust-badge">
      <span className="dealix-trust-badge__dot" />
      {label}
    </span>
  );
}
