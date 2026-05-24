// Dealix brand tokens — minimal, no claims.
// Verifier: scripts/verify_brand_system.py asserts this file exports tokens.

export const brandTokens = {
  colors: {
    bg: "#0b0f14",
    panel: "#11161d",
    border: "#1f2933",
    text: "#e6edf3",
    textMuted: "#8b95a1",
    accent: "#5eead4",
    accentMuted: "#0f766e",
    warn: "#fbbf24",
    danger: "#ef4444",
    ok: "#22c55e",
  },
  font: {
    sans: "system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif",
    mono: "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace",
  },
  space: {
    xs: "4px",
    sm: "8px",
    md: "16px",
    lg: "24px",
    xl: "40px",
  },
  radius: {
    sm: "6px",
    md: "10px",
    lg: "16px",
  },
} as const;

export type BrandTokens = typeof brandTokens;
