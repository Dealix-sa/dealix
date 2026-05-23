/**
 * Dealix brand tokens (typed mirror of docs/brand/brand-tokens.json).
 * The JSON file is the single source of truth; this module exposes a
 * strongly typed view for the web app.
 */

export const brandTokens = {
  name: "Dealix",
  tagline: "INTELLIGENT DEALS. REAL GROWTH.",
  colors: {
    deepNavy: "#0B1220",
    emeraldTeal: "#00D1A1",
    softSilver: "#B2BBC6",
    slate: "#0F1726",
    white: "#FFFFFF",
  },
  typography: {
    wordmarkFamily: "Inter, system-ui, sans-serif",
    headingFamily: "Inter, system-ui, sans-serif",
    bodyFamily: "Inter, system-ui, sans-serif",
    weights: { regular: 400, medium: 500, semibold: 600, bold: 700 },
  },
  pillars: [
    "Built on Trust",
    "Driven by Growth",
    "Closing Deals",
    "Focused on Results",
    "Global Mindset, Local Impact",
  ],
  spacing: { xs: "4px", sm: "8px", md: "16px", lg: "24px", xl: "32px", xxl: "48px" },
  radius: { sm: "6px", md: "10px", lg: "14px" },
  shadow: {
    sm: "0 1px 3px rgba(0,0,0,0.18)",
    md: "0 6px 14px rgba(0,0,0,0.28)",
  },
} as const;

export type BrandTokens = typeof brandTokens;
