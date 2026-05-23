import { color } from "../../lib/brand-tokens";

type Variant = "full" | "compact" | "mark" | "wordmark";

interface DealixLogoProps {
  variant?: Variant;
  height?: number;
  showTagline?: boolean;
  monochrome?: boolean;
  title?: string;
}

/**
 * Inline SVG implementation of the Dealix mark + wordmark.
 * Source spec: docs/brand/DEALIX_LOGO_USAGE.md.
 */
export function DealixLogo({
  variant = "full",
  height = 36,
  showTagline = false,
  monochrome = false,
  title = "Dealix",
}: DealixLogoProps) {
  const accent = monochrome ? color.text.primary : color.accent.primary;
  const text   = color.text.primary;
  const muted  = color.text.secondary;

  const mark = (
    <svg
      viewBox="0 0 56 56"
      width={height}
      height={height}
      role="img"
      aria-label={title}
    >
      <defs>
        <linearGradient id="dxGrad" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%"  stopColor={accent} />
          <stop offset="100%" stopColor={monochrome ? text : "#5AC8FA"} />
        </linearGradient>
      </defs>
      {/* D shape */}
      <path
        d="M10 8 H26 C40 8 48 17 48 28 C48 39 40 48 26 48 H10 Z M18 16 V40 H26 C34 40 40 35 40 28 C40 21 34 16 26 16 Z"
        fill={text}
      />
      {/* Growth arrow cutting through */}
      <path
        d="M14 42 L30 26 L38 32 L48 18"
        stroke="url(#dxGrad)"
        strokeWidth="3.2"
        strokeLinecap="round"
        strokeLinejoin="round"
        fill="none"
      />
      <polygon points="46,14 50,14 50,18" fill={accent} />
      {/* Revenue bars beneath */}
      <rect x="14" y="46" width="4"  height="2" rx="1" fill={accent} opacity="0.55" />
      <rect x="22" y="44" width="4"  height="4" rx="1" fill={accent} opacity="0.75" />
      <rect x="30" y="42" width="4"  height="6" rx="1" fill={accent} />
    </svg>
  );

  const wordmark = (
    <span
      style={{
        fontFamily: "'Inter Tight', 'IBM Plex Sans Arabic', system-ui, sans-serif",
        fontWeight: 800,
        fontSize: Math.round(height * 0.72),
        letterSpacing: "0.08em",
        color: text,
        lineHeight: 1,
      }}
    >
      DEALIX
    </span>
  );

  const tagline = showTagline ? (
    <span
      style={{
        display: "block",
        fontFamily: "Inter, 'IBM Plex Sans Arabic', system-ui, sans-serif",
        fontSize: Math.max(10, Math.round(height * 0.22)),
        letterSpacing: "0.22em",
        color: muted,
        marginTop: 4,
        textTransform: "uppercase",
      }}
    >
      Intelligent Deals. Real Growth.
    </span>
  ) : null;

  if (variant === "mark") return mark;
  if (variant === "wordmark") return <div>{wordmark}{tagline}</div>;

  return (
    <div style={{ display: "inline-flex", alignItems: "center", gap: 12 }}>
      {mark}
      <div>
        {wordmark}
        {tagline}
      </div>
    </div>
  );
}

export default DealixLogo;
