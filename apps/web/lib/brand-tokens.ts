// Dealix Brand Tokens — single source of truth (TypeScript)
// Mirrored in docs/brand/brand-tokens.json and apps/web/styles/brand.css.
// Any change here must be reflected in both mirrors. The brand verifier
// enforces consistency between the three.

export const DEALIX_BRAND = {
  name: "Dealix",
  wordmark: "DEALIX",
  tagline: "Intelligent Deals. Real Growth.",
  taglineLockup: "INTELLIGENT DEALS. REAL GROWTH.",
  taglineAr: "صفقات ذكية. نمو حقيقي.",
  pillars: [
    "Built on Trust",
    "Driven by Growth",
    "Closing Deals",
    "Focused on Results",
    "Global Mindset, Local Impact"
  ] as const
} as const;

export const colors = {
  deepNavy: "#0B1220",
  emeraldTeal: "#00D1A1",
  softSilver: "#B2BBC6",
  slate: "#0F1726",
  white: "#FFFFFF",
  amber: "#F6B73C",
  red: "#FF5C7A"
} as const;

export const semanticColors = {
  backgroundPrimary: colors.deepNavy,
  backgroundSecondary: colors.slate,
  surface: colors.slate,
  accentPrimary: colors.emeraldTeal,
  accentOnAccent: colors.deepNavy,
  textPrimary: colors.white,
  textSecondary: colors.softSilver,
  borderSubtle: "rgba(178, 187, 198, 0.18)",
  borderStrong: "rgba(178, 187, 198, 0.42)",
  success: colors.emeraldTeal,
  warning: colors.amber,
  danger: colors.red,
  muted: colors.slate
} as const;

export const typography = {
  fontDisplay:
    'Inter, "IBM Plex Sans Arabic", system-ui, -apple-system, "Segoe UI", "Helvetica Neue", Arial, sans-serif',
  fontBody:
    'Inter, "IBM Plex Sans Arabic", system-ui, -apple-system, "Segoe UI", "Helvetica Neue", Arial, sans-serif',
  fontMono:
    '"JetBrains Mono", ui-monospace, "Cascadia Mono", Menlo, Consolas, monospace',
  scale: {
    xs: "12px",
    sm: "14px",
    base: "16px",
    lg: "18px",
    xl: "20px",
    "2xl": "24px",
    "3xl": "30px",
    "4xl": "36px",
    "5xl": "48px",
    "6xl": "60px"
  },
  weight: {
    regular: 400,
    medium: 500,
    semibold: 600,
    bold: 700,
    extrabold: 800
  }
} as const;

export const radii = {
  none: "0",
  sm: "6px",
  md: "10px",
  lg: "16px",
  xl: "20px",
  pill: "999px"
} as const;

export const spacing = {
  0: "0",
  1: "4px",
  2: "8px",
  3: "12px",
  4: "16px",
  5: "20px",
  6: "24px",
  8: "32px",
  10: "40px",
  12: "48px",
  16: "64px"
} as const;

export const elevation = {
  none: "none",
  sm: "0 1px 2px rgba(0, 0, 0, 0.18)",
  md: "0 4px 12px rgba(0, 0, 0, 0.24)",
  lg: "0 10px 32px rgba(0, 0, 0, 0.32)"
} as const;

export const motion = {
  durationFast: "120ms",
  durationBase: "200ms",
  durationSlow: "320ms",
  easingStandard: "cubic-bezier(0.2, 0, 0, 1)",
  easingEnter: "cubic-bezier(0, 0, 0, 1)",
  easingExit: "cubic-bezier(0.4, 0, 1, 1)"
} as const;

export type BrandColorToken = keyof typeof colors;
export type BrandSemanticToken = keyof typeof semanticColors;

const tokens = {
  brand: DEALIX_BRAND,
  colors,
  semanticColors,
  typography,
  radii,
  spacing,
  elevation,
  motion
};

export default tokens;
