/**
 * Dealix Brand Tokens — single source of truth for the Founder Console.
 *
 * Mirror of `docs/brand/brand-tokens.json`. Edit both together; the brand
 * verifier (`scripts/verify_brand_system.py`) checks that the JSON and
 * this file stay in sync.
 */

export const brand = {
  name: "DEALIX",
  tagline: "INTELLIGENT DEALS. REAL GROWTH.",
  pillars: [
    "Built on Trust",
    "Driven by Growth",
    "Closing Deals",
    "Focused on Results",
    "Global Mindset, Local Impact",
  ] as const,
  positioning:
    "Saudi B2B Revenue Operating System for intelligent deal flow, founder-approved growth, and trust-gated AI execution.",
} as const;

export const color = {
  bg: {
    primary:  "#0B1220",
    surface:  "#0F1726",
    elevated: "#162038",
    inverse:  "#FFFFFF",
  },
  accent: {
    primary: "#00D1A1",
    hover:   "#00B388",
    muted:   "#0E3A30",
  },
  text: {
    primary:   "#FFFFFF",
    secondary: "#B2BBC6",
    muted:     "#7C8895",
    inverse:   "#0B1220",
  },
  border: {
    subtle: "#1B2536",
    strong: "#2A3753",
    accent: "#00D1A1",
  },
  status: {
    success: "#00D1A1",
    warning: "#F2B33D",
    danger:  "#FF6B6B",
    info:    "#5AC8FA",
  },
} as const;

export const font = {
  family: {
    display: "'Inter Tight', 'IBM Plex Sans Arabic', system-ui, sans-serif",
    body:    "Inter, 'IBM Plex Sans Arabic', system-ui, sans-serif",
    mono:    "'JetBrains Mono', ui-monospace, SFMono-Regular, monospace",
  },
  weight: { regular: 400, medium: 500, semibold: 600, bold: 700 } as const,
  size: {
    xs:  "0.75rem",
    sm:  "0.875rem",
    md:  "1rem",
    lg:  "1.125rem",
    xl:  "1.25rem",
    "2xl": "1.5rem",
    "3xl": "1.875rem",
    "4xl": "2.25rem",
    "5xl": "3rem",
    "6xl": "3.75rem",
  } as const,
  lineHeight: { tight: 1.2, snug: 1.35, normal: 1.5, relaxed: 1.65 } as const,
} as const;

export const radius = {
  xs:   "4px",
  sm:   "8px",
  md:   "12px",
  lg:   "16px",
  xl:   "24px",
  pill: "9999px",
} as const;

export const spacing = {
  0: "0px",  1: "4px",  2: "8px",  3: "12px",
  4: "16px", 5: "20px", 6: "24px", 8: "32px",
  10: "40px", 12: "48px", 16: "64px", 20: "80px", 24: "96px",
} as const;

export const shadow = {
  sm:     "0 1px 2px rgba(0,0,0,0.4)",
  md:     "0 4px 12px rgba(0,0,0,0.45)",
  lg:     "0 16px 40px rgba(0,0,0,0.55)",
  accent: "0 0 0 1px rgba(0,209,161,0.35), 0 8px 24px rgba(0,209,161,0.18)",
} as const;

export const motion = {
  duration: { fast: "120ms", base: "200ms", slow: "320ms" } as const,
  easing: {
    standard: "cubic-bezier(.2,.8,.2,1)",
    entrance: "cubic-bezier(.16,.84,.44,1)",
    exit:     "cubic-bezier(.4,.0,.84,.16)",
  } as const,
} as const;

export type BrandColor = typeof color;
export type BrandFont = typeof font;

export const tokens = { brand, color, font, radius, spacing, shadow, motion } as const;
export default tokens;
