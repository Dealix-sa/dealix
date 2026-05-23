// Dealix brand tokens — single source of truth for the web app.
// Mirrors docs/brand/brand-tokens.json. Keep them in sync.

export const dealixBrand = {
  name: "Dealix",
  wordmark: "DEALIX",
  taglineEn: "Intelligent Deals. Real Growth.",
  taglineAr: "صفقات ذكية. نمو حقيقي.",
  positioning:
    "Saudi B2B Revenue Operating System for intelligent deal flow, founder-approved growth, and trust-gated AI execution.",
  pillars: [
    "Built on Trust",
    "Driven by Growth",
    "Closing Deals",
    "Focused on Results",
    "Global Mindset, Local Impact",
  ],
} as const;

export const dealixColors = {
  deepNavy:    "#0B1220",
  emeraldTeal: "#00D1A1",
  softSilver:  "#B2BBC6",
  slate:       "#0F1726",
  white:       "#FFFFFF",

  bg:            "#0B1220",
  surface:       "#0F1726",
  surfaceAlt:    "#121C30",
  border:        "#1B2740",
  textPrimary:   "#FFFFFF",
  textSecondary: "#B2BBC6",
  accent:        "#00D1A1",
  accentPressed: "#00B98D",
  success:       "#00D1A1",
  warning:       "#F2C84B",
  danger:        "#FF5A5F",
  info:          "#5AB0FF",
} as const;

export const dealixTypography = {
  latin:  'Inter, system-ui, -apple-system, "Segoe UI", Roboto, sans-serif',
  arabic: '"IBM Plex Sans Arabic", "Noto Sans Arabic", Tahoma, sans-serif',
  scale: {
    display: "44px",
    h1: "32px",
    h2: "24px",
    h3: "18px",
    body: "15px",
    small: "13px",
    caption: "12px",
  },
} as const;

export const dealixRadius = {
  sm: "6px",
  md: "10px",
  lg: "14px",
  xl: "20px",
  pill: "999px",
} as const;

export const dealixShadow = {
  card:    "0 1px 2px rgba(0,0,0,0.25), 0 4px 12px rgba(0,0,0,0.18)",
  raised:  "0 6px 24px rgba(0,0,0,0.30)",
  focus:   "0 0 0 3px rgba(0,209,161,0.35)",
} as const;

export type DealixColor = keyof typeof dealixColors;
