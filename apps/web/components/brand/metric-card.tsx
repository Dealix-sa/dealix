import type { CSSProperties } from "react";
import { semanticColors, radii, spacing } from "../../lib/brand-tokens";

interface MetricCardProps {
  label: string;
  value: string | number;
  delta?: string;
  deltaDirection?: "up" | "down" | "flat";
  hint?: string;
  style?: CSSProperties;
}

const deltaColor = (direction: "up" | "down" | "flat") => {
  if (direction === "up") return semanticColors.success;
  if (direction === "down") return semanticColors.danger;
  return semanticColors.textSecondary;
};

const deltaSymbol = (direction: "up" | "down" | "flat") => {
  if (direction === "up") return "▲";
  if (direction === "down") return "▼";
  return "■";
};

export function MetricCard({
  label,
  value,
  delta,
  deltaDirection = "flat",
  hint,
  style
}: MetricCardProps) {
  return (
    <div
      style={{
        background: semanticColors.surface,
        color: semanticColors.textPrimary,
        borderRadius: radii.lg,
        border: `1px solid ${semanticColors.borderSubtle}`,
        padding: spacing[6],
        minWidth: 180,
        ...style
      }}
    >
      <div
        style={{
          color: semanticColors.textSecondary,
          fontSize: 12,
          fontWeight: 600,
          letterSpacing: "0.12em",
          textTransform: "uppercase",
          marginBottom: spacing[2]
        }}
      >
        {label}
      </div>
      <div
        style={{
          fontSize: 36,
          fontWeight: 800,
          lineHeight: 1.1,
          color: semanticColors.accentPrimary
        }}
      >
        {value}
      </div>
      {delta ? (
        <div
          style={{
            marginTop: spacing[2],
            fontSize: 14,
            fontWeight: 600,
            color: deltaColor(deltaDirection)
          }}
        >
          <span aria-hidden style={{ marginInlineEnd: 6 }}>
            {deltaSymbol(deltaDirection)}
          </span>
          {delta}
        </div>
      ) : null}
      {hint ? (
        <div
          style={{
            marginTop: spacing[3],
            fontSize: 12,
            color: semanticColors.textSecondary,
            lineHeight: 1.5
          }}
        >
          {hint}
        </div>
      ) : null}
    </div>
  );
}

export default MetricCard;
