import type { CSSProperties, ReactNode } from "react";
import { semanticColors, spacing } from "../../lib/brand-tokens";

interface SectionHeadingProps {
  eyebrow?: string;
  title: ReactNode;
  subtitle?: ReactNode;
  align?: "start" | "center";
  style?: CSSProperties;
}

export function SectionHeading({
  eyebrow,
  title,
  subtitle,
  align = "start",
  style
}: SectionHeadingProps) {
  const textAlign = align === "center" ? "center" : "start";

  return (
    <header style={{ textAlign, marginBottom: spacing[6], ...style }}>
      {eyebrow ? (
        <div
          style={{
            color: semanticColors.accentPrimary,
            fontSize: 12,
            fontWeight: 700,
            letterSpacing: "0.16em",
            textTransform: "uppercase",
            marginBottom: spacing[2]
          }}
        >
          {eyebrow}
        </div>
      ) : null}
      <h2
        style={{
          margin: 0,
          color: semanticColors.textPrimary,
          fontSize: 30,
          fontWeight: 800,
          lineHeight: 1.2
        }}
      >
        {title}
      </h2>
      {subtitle ? (
        <p
          style={{
            marginTop: spacing[3],
            color: semanticColors.textSecondary,
            fontSize: 16,
            lineHeight: 1.6,
            maxWidth: 640,
            marginInline: align === "center" ? "auto" : 0
          }}
        >
          {subtitle}
        </p>
      ) : null}
    </header>
  );
}

export default SectionHeading;
