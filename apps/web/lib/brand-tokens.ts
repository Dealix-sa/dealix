// Dealix brand tokens (typed). Source of truth: docs/brand/brand-tokens.json.
// Keep these in sync. Do not hardcode brand colors elsewhere.

export const brand = {
  wordmark: "DEALIX",
  tagline: "INTELLIGENT DEALS. REAL GROWTH.",
  taglineAr: "صفقات ذكية. نمو حقيقي.",
  pillars: [
    "Built on Trust",
    "Driven by Growth",
    "Closing Deals",
    "Focused on Results",
    "Global Mindset, Local Impact",
  ] as const,
} as const;

export const color = {
  deepNavy: "#0B1220",
  emeraldTeal: "#00D1A1",
  softSilver: "#B2BBC6",
  slate: "#0F1726",
  white: "#FFFFFF",

  surfacePage: "#0B1220",
  surfacePanel: "#0F1726",
  surfaceCard: "#111B2E",
  surfaceCardAlt: "#142039",
  border: "#1E2A44",
  borderStrong: "#2B3A5A",

  textPrimary: "#FFFFFF",
  textSecondary: "#B2BBC6",
  textMuted: "#8693A6",
  textInverse: "#0B1220",
  textAccent: "#00D1A1",

  success: "#00D1A1",
  info: "#3A9CFF",
  warning: "#F5B547",
  danger: "#F26D6D",

  approvalA1: "#00D1A1",
  approvalA2: "#F5B547",
  approvalA3: "#F26D6D",
} as const;

export const radius = {
  sm: "6px",
  md: "10px",
  lg: "14px",
  xl: "20px",
  pill: "999px",
} as const;

export const space = {
  xs: "4px",
  sm: "8px",
  md: "12px",
  lg: "16px",
  xl: "24px",
  xxl: "32px",
  xxxl: "48px",
} as const;

export const font = {
  sans: 'Inter, "IBM Plex Sans Arabic", system-ui, -apple-system, sans-serif',
  mono: '"JetBrains Mono", "IBM Plex Mono", ui-monospace, SFMono-Regular, monospace',
} as const;

export type BrandColor = keyof typeof color;
export type ApprovalClass = "A1" | "A2" | "A3";

export const approvalColor = (cls: ApprovalClass): string => {
  if (cls === "A1") return color.approvalA1;
  if (cls === "A2") return color.approvalA2;
  return color.approvalA3;
};
