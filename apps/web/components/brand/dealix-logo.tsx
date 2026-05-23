import type { CSSProperties } from "react";

type DealixLogoProps = {
  variant?: "full" | "mark" | "wordmark";
  height?: number;
  withTagline?: boolean;
  style?: CSSProperties;
};

const NAVY = "#0B1220";
const TEAL = "#00D1A1";
const SILVER = "#B2BBC6";

export function DealixLogo({
  variant = "full",
  height = 32,
  withTagline = false,
  style,
}: DealixLogoProps) {
  if (variant === "mark") {
    return <DealixMark height={height} style={style} />;
  }

  const markSize = height;
  const wordmarkSize = Math.round(height * 0.7);
  const taglineSize = Math.round(height * 0.32);

  return (
    <span
      role="img"
      aria-label="Dealix — Intelligent Deals. Real Growth."
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: 10,
        ...style,
      }}
    >
      {variant === "full" && <DealixMark height={markSize} />}
      <span style={{ display: "inline-flex", flexDirection: "column", lineHeight: 1.1 }}>
        <span
          style={{
            fontSize: wordmarkSize,
            fontWeight: 800,
            letterSpacing: "0.04em",
            color: "var(--dlx-text-primary, #FFFFFF)",
          }}
        >
          DEALIX
        </span>
        {withTagline && (
          <span
            style={{
              fontSize: taglineSize,
              color: SILVER,
              letterSpacing: "0.06em",
              textTransform: "uppercase",
            }}
          >
            Intelligent Deals. Real Growth.
          </span>
        )}
      </span>
    </span>
  );
}

function DealixMark({
  height = 32,
  style,
}: {
  height?: number;
  style?: CSSProperties;
}) {
  return (
    <svg
      role="img"
      aria-label="Dealix mark"
      viewBox="0 0 64 64"
      width={height}
      height={height}
      style={style}
    >
      <title>Dealix monogram with growth arrow and revenue bars</title>
      <rect x="2" y="2" width="60" height="60" rx="14" fill={NAVY} />
      <path
        d="M14 16h18a16 16 0 0 1 16 16v0a16 16 0 0 1-16 16H14V16z"
        fill="none"
        stroke={SILVER}
        strokeWidth="3"
      />
      <rect x="18" y="38" width="4"  height="10" fill={TEAL} />
      <rect x="26" y="32" width="4"  height="16" fill={TEAL} />
      <rect x="34" y="26" width="4"  height="22" fill={TEAL} />
      <path
        d="M16 24 L40 14 L44 18 L36 20 L34 16"
        fill="none"
        stroke={TEAL}
        strokeWidth="3"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <path
        d="M14 54 Q34 60 54 50"
        fill="none"
        stroke={TEAL}
        strokeWidth="2"
        strokeLinecap="round"
        opacity="0.7"
      />
    </svg>
  );
}
