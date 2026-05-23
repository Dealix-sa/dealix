// Dealix Brand Tokens — generated source-of-truth for UI.
// Mirror of docs/brand/brand-tokens.json. Update both in sync.

export const DealixBrand = {
  wordmark: "DEALIX",
  tagline: "INTELLIGENT DEALS. REAL GROWTH.",
  positioning: "Saudi B2B Revenue Operating System",
  colors: {
    deepNavy: "#0B1220",
    emeraldTeal: "#00D1A1",
    softSilver: "#B2BBC6",
    slate: "#0F1726",
    white: "#FFFFFF",
    border: "#1f2a3a",
    danger: "#ef4444",
    warning: "#f59e0b",
  },
  pillars: [
    "Built on Trust",
    "Driven by Growth",
    "Closing Deals",
    "Focused on Results",
    "Global Mindset, Local Impact",
  ],
  typography: {
    heading: "Inter, 'IBM Plex Sans Arabic', system-ui, sans-serif",
    body: "Inter, 'IBM Plex Sans Arabic', system-ui, sans-serif",
    mono: "ui-monospace, SFMono-Regular, Menlo, monospace",
  },
  radius: { sm: "6px", md: "10px", lg: "14px", pill: "9999px" },
} as const;

export type DealixBrandTokens = typeof DealixBrand;
