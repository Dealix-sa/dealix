import type { CSSProperties } from "react";
import { semanticColors, radii, spacing } from "../../lib/brand-tokens";

type StatusKind = "ok" | "warn" | "error" | "info" | "muted";

interface StatusBadgeProps {
  kind?: StatusKind;
  children: string;
  style?: CSSProperties;
}

const KIND_TO_BG: Record<StatusKind, string> = {
  ok: "rgba(0, 209, 161, 0.16)",
  warn: "rgba(246, 183, 60, 0.16)",
  error: "rgba(255, 92, 122, 0.16)",
  info: "rgba(178, 187, 198, 0.18)",
  muted: "rgba(178, 187, 198, 0.10)"
};

const KIND_TO_FG: Record<StatusKind, string> = {
  ok: semanticColors.success,
  warn: semanticColors.warning,
  error: semanticColors.danger,
  info: semanticColors.textPrimary,
  muted: semanticColors.textSecondary
};

const KIND_TO_GLYPH: Record<StatusKind, string> = {
  ok: "●",
  warn: "▲",
  error: "■",
  info: "◆",
  muted: "○"
};

export function StatusBadge({
  kind = "info",
  children,
  style
}: StatusBadgeProps) {
  return (
    <span
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: 6,
        background: KIND_TO_BG[kind],
        color: KIND_TO_FG[kind],
        borderRadius: radii.pill,
        padding: `${spacing[1]} ${spacing[3]}`,
        fontSize: 12,
        fontWeight: 600,
        letterSpacing: "0.06em",
        ...style
      }}
      role="status"
      aria-label={`${kind}: ${children}`}
    >
      <span aria-hidden style={{ fontSize: 9, lineHeight: 1 }}>
        {KIND_TO_GLYPH[kind]}
      </span>
      {children}
    </span>
  );
}

export default StatusBadge;
