import type { CSSProperties, ReactNode } from "react";
import { semanticColors, radii, spacing } from "../../lib/brand-tokens";

type Variant = "primary" | "ghost";

interface CtaButtonProps {
  href?: string;
  variant?: Variant;
  children: ReactNode;
  ariaLabel?: string;
  style?: CSSProperties;
}

export function CtaButton({
  href,
  variant = "primary",
  children,
  ariaLabel,
  style
}: CtaButtonProps) {
  const baseStyle: CSSProperties = {
    display: "inline-flex",
    alignItems: "center",
    justifyContent: "center",
    fontWeight: 700,
    fontSize: 16,
    padding: `${spacing[3]} ${spacing[6]}`,
    borderRadius: radii.md,
    textDecoration: "none",
    cursor: "pointer",
    transition: "filter 200ms ease, border-color 200ms ease, color 200ms ease",
    ...style
  };

  const variantStyle: CSSProperties =
    variant === "primary"
      ? {
          background: semanticColors.accentPrimary,
          color: semanticColors.accentOnAccent,
          border: "none"
        }
      : {
          background: "transparent",
          color: semanticColors.textPrimary,
          border: `1px solid ${semanticColors.borderStrong}`
        };

  const combinedStyle = { ...baseStyle, ...variantStyle };

  if (href) {
    return (
      <a href={href} aria-label={ariaLabel} style={combinedStyle}>
        {children}
      </a>
    );
  }
  return (
    <button type="button" aria-label={ariaLabel} style={combinedStyle}>
      {children}
    </button>
  );
}

export default CtaButton;
