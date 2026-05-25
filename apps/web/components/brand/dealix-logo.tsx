import type { CSSProperties } from "react";
import { DEALIX_BRAND, colors } from "../../lib/brand-tokens";

type Variant = "lockup" | "wordmark" | "icon";

interface DealixLogoProps {
  variant?: Variant;
  withTagline?: boolean;
  height?: number;
  ariaLabel?: string;
  style?: CSSProperties;
}

const fallbackStyle = (height: number, variant: Variant): CSSProperties => ({
  display: "inline-flex",
  alignItems: "center",
  gap: variant === "lockup" ? 12 : 0,
  height,
  lineHeight: 1,
  fontFamily:
    'Inter, "IBM Plex Sans Arabic", system-ui, -apple-system, sans-serif'
});

// Inline SVG fallback for the D monogram. Vector — looks crisp at any size.
function IconMonogram({ size }: { size: number }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 64 64"
      role="img"
      aria-label="Dealix monogram"
      xmlns="http://www.w3.org/2000/svg"
    >
      <rect x="0" y="0" width="64" height="64" rx="14" fill={colors.deepNavy} />
      {/* D outline */}
      <path
        d="M14 12 H32 C44 12 50 20 50 32 C50 44 44 52 32 52 H14 Z"
        fill="none"
        stroke={colors.white}
        strokeWidth="3.5"
        strokeLinejoin="round"
      />
      {/* Revenue bars */}
      <rect x="20" y="36" width="3.5" height="10" fill={colors.softSilver} />
      <rect x="26" y="30" width="3.5" height="16" fill={colors.softSilver} />
      <rect x="32" y="24" width="3.5" height="22" fill={colors.white} />
      {/* Growth arrow */}
      <path
        d="M18 42 L42 18 M42 18 L34 18 M42 18 L42 26"
        fill="none"
        stroke={colors.emeraldTeal}
        strokeWidth="3"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      {/* Teal swoosh */}
      <path
        d="M10 56 C 22 50, 42 50, 56 44"
        fill="none"
        stroke={colors.emeraldTeal}
        strokeWidth="3"
        strokeLinecap="round"
      />
    </svg>
  );
}

function Wordmark({ height }: { height: number }) {
  return (
    <span
      style={{
        fontSize: height * 0.72,
        fontWeight: 800,
        letterSpacing: "0.06em",
        color: colors.white,
        lineHeight: 1
      }}
    >
      {DEALIX_BRAND.wordmark}
    </span>
  );
}

function Tagline({ height }: { height: number }) {
  return (
    <span
      style={{
        fontSize: height * 0.28,
        fontWeight: 500,
        letterSpacing: "0.08em",
        color: colors.softSilver,
        textTransform: "uppercase",
        lineHeight: 1.2,
        marginTop: 4
      }}
    >
      {DEALIX_BRAND.taglineLockup}
    </span>
  );
}

export function DealixLogo({
  variant = "lockup",
  withTagline = true,
  height = 40,
  ariaLabel,
  style
}: DealixLogoProps) {
  const monogramSize = variant === "icon" ? height : Math.round(height * 0.95);
  const label =
    ariaLabel ??
    (variant === "icon"
      ? "Dealix"
      : `Dealix — ${DEALIX_BRAND.tagline}`);

  if (variant === "icon") {
    return (
      <span
        role="img"
        aria-label={label}
        style={{ display: "inline-flex", lineHeight: 0, ...style }}
      >
        <IconMonogram size={height} />
      </span>
    );
  }

  if (variant === "wordmark") {
    return (
      <span
        role="img"
        aria-label={label}
        style={{ ...fallbackStyle(height, "wordmark"), ...style }}
      >
        <Wordmark height={height} />
      </span>
    );
  }

  // lockup
  return (
    <span
      role="img"
      aria-label={label}
      style={{ ...fallbackStyle(height, "lockup"), ...style }}
    >
      <IconMonogram size={monogramSize} />
      <span style={{ display: "inline-flex", flexDirection: "column" }}>
        <Wordmark height={height} />
        {withTagline ? <Tagline height={height} /> : null}
      </span>
    </span>
  );
}

export default DealixLogo;
