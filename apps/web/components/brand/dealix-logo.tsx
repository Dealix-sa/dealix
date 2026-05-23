import { DealixBrand } from "../../lib/brand-tokens";

type DealixLogoProps = {
  size?: number;
  showTagline?: boolean;
  monochrome?: boolean;
};

export function DealixLogo({ size = 28, showTagline = true, monochrome = false }: DealixLogoProps) {
  const teal = monochrome ? DealixBrand.colors.white : DealixBrand.colors.emeraldTeal;
  const silver = DealixBrand.colors.softSilver;
  const white = DealixBrand.colors.white;
  return (
    <div style={{ display: "inline-flex", alignItems: "center", gap: 10 }}>
      <svg
        width={size}
        height={size}
        viewBox="0 0 64 64"
        aria-label="Dealix monogram"
        role="img"
      >
        <rect x="0" y="0" width="64" height="64" rx="12" fill={DealixBrand.colors.slate} />
        <path
          d="M14 14 H34 a16 16 0 0 1 16 16 v4 a16 16 0 0 1 -16 16 H14 z"
          fill="none"
          stroke={white}
          strokeWidth="4"
        />
        <path d="M20 46 L46 18" stroke={teal} strokeWidth="4" strokeLinecap="round" />
        <path d="M40 18 L48 18 L48 26" stroke={teal} strokeWidth="4" strokeLinecap="round" fill="none" />
        <rect x="22" y="36" width="4" height="8" fill={teal} />
        <rect x="28" y="32" width="4" height="12" fill={teal} />
        <rect x="34" y="28" width="4" height="16" fill={teal} />
      </svg>
      <div style={{ display: "flex", flexDirection: "column", lineHeight: 1 }}>
        <span
          style={{
            fontWeight: 800,
            letterSpacing: "0.18em",
            color: white,
            fontSize: Math.round(size * 0.6),
          }}
        >
          {DealixBrand.wordmark}
        </span>
        {showTagline && (
          <span
            style={{
              color: silver,
              fontSize: Math.max(9, Math.round(size * 0.28)),
              letterSpacing: "0.18em",
              marginTop: 4,
              textTransform: "uppercase",
            }}
          >
            {DealixBrand.tagline}
          </span>
        )}
      </div>
    </div>
  );
}
