import type { CSSProperties, ReactNode } from "react";
import { semanticColors, radii, spacing, elevation } from "../../lib/brand-tokens";

interface BrandCardProps {
  title?: string;
  eyebrow?: string;
  children: ReactNode;
  accent?: boolean;
  style?: CSSProperties;
}

export function BrandCard({
  title,
  eyebrow,
  children,
  accent = false,
  style
}: BrandCardProps) {
  const borderLeft = accent
    ? `3px solid ${semanticColors.accentPrimary}`
    : undefined;

  return (
    <section
      style={{
        background: semanticColors.surface,
        color: semanticColors.textPrimary,
        borderRadius: radii.lg,
        border: `1px solid ${semanticColors.borderSubtle}`,
        borderLeft,
        padding: spacing[6],
        boxShadow: elevation.md,
        ...style
      }}
    >
      {eyebrow ? (
        <div
          style={{
            color: semanticColors.accentPrimary,
            fontSize: 12,
            fontWeight: 600,
            letterSpacing: "0.12em",
            textTransform: "uppercase",
            marginBottom: spacing[2]
          }}
        >
          {eyebrow}
        </div>
      ) : null}
      {title ? (
        <h3
          style={{
            margin: 0,
            color: semanticColors.textPrimary,
            fontSize: 20,
            fontWeight: 700,
            lineHeight: 1.3,
            marginBottom: spacing[3]
          }}
        >
          {title}
        </h3>
      ) : null}
      <div style={{ color: semanticColors.textSecondary, lineHeight: 1.6 }}>
        {children}
      </div>
    </section>
  );
}

export default BrandCard;
