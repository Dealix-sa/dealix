/**
 * DEALIX Design Tokens
 * Single source of truth for brand colors, typography, spacing, and animation.
 * Use these in TypeScript/React code. CSS consumers use globals.css variables.
 */

export const brand = {
  colors: {
    // ── Core brand palette ──────────────────────────────────────────────
    navy:   "#0B1220",   // Deep Navy     — primary background, trust
    slate:  "#0F1726",   // Slate         — card surfaces
    teal:   "#00D1A1",   // Emerald Teal  — primary CTA, growth accent
    silver: "#B2BBC6",   // Soft Silver   — secondary text, chrome
    white:  "#FFFFFF",   // White         — text on dark

    // ── Teal scale ──────────────────────────────────────────────────────
    tealScale: {
      50:  "#e0fff8",
      100: "#b3ffee",
      200: "#80ffe3",
      300: "#4dffd7",
      400: "#26edbe",
      500: "#00D1A1",   // brand teal
      600: "#00a880",
      700: "#007d60",
      800: "#005240",
      900: "#002820",
    },

    // ── Navy scale ──────────────────────────────────────────────────────
    navyScale: {
      50:  "#e8eaf0",
      100: "#c5cadc",
      200: "#9ea8c6",
      300: "#7787b0",
      400: "#5a6ca0",
      500: "#3d5191",
      600: "#2d3c72",
      700: "#1e2854",
      800: "#111a38",
      900: "#0B1220",   // brand navy
      950: "#070c18",
    },

    // ── Silver scale ────────────────────────────────────────────────────
    silverScale: {
      50:  "#f8f9fa",
      100: "#eef0f3",
      200: "#dde1e6",
      300: "#c8cfd8",
      400: "#B2BBC6",   // brand silver
      500: "#97a2b0",
      600: "#788797",
      700: "#5c6b7a",
      800: "#424e5a",
      900: "#2a323b",
    },

    // ── Semantic ─────────────────────────────────────────────────────────
    semantic: {
      success:    "#00D1A1",   // teal
      warning:    "#F5A623",
      error:      "#E53E3E",
      info:       "#3B82F6",
    },
  },

  typography: {
    fontFamily: {
      display:  ["Sora", "Space Grotesk", "IBM Plex Sans Arabic", "system-ui"],
      body:     ["Manrope", "Plus Jakarta Sans", "IBM Plex Sans Arabic", "system-ui"],
      arabic:   ["IBM Plex Sans Arabic", "Noto Sans Arabic", "system-ui"],
      mono:     ["JetBrains Mono", "ui-monospace", "monospace"],
    },
    fontSize: {
      xs:   "0.75rem",    //  12px
      sm:   "0.875rem",   //  14px
      base: "1rem",       //  16px
      lg:   "1.125rem",   //  18px
      xl:   "1.25rem",    //  20px
      "2xl":"1.5rem",     //  24px
      "3xl":"1.875rem",   //  30px
      "4xl":"2.25rem",    //  36px
      "5xl":"3rem",       //  48px
    },
    fontWeight: {
      light:    300,
      regular:  400,
      medium:   500,
      semibold: 600,
      bold:     700,
      extrabold:800,
    },
    lineHeight: {
      tight:   1.25,
      snug:    1.375,
      normal:  1.5,
      relaxed: 1.625,
      loose:   1.75,   // Arabic body — extra room for diacritics
    },
  },

  spacing: {
    // 4px base grid
    1:  "4px",
    2:  "8px",
    3:  "12px",
    4:  "16px",
    6:  "24px",
    8:  "32px",
    12: "48px",
    16: "64px",
    24: "96px",
  },

  borderRadius: {
    sm:   "6px",
    md:   "8px",
    lg:   "12px",
    xl:   "16px",
    full: "9999px",
  },

  shadow: {
    teal:  "0 0 24px rgba(0, 209, 161, 0.10), 0 1px 3px rgba(0,0,0,0.35)",
    navy:  "0 0 24px rgba(11, 18, 32, 0.60), 0 1px 3px rgba(0,0,0,0.35)",
    card:  "0 2px 8px rgba(0,0,0,0.25)",
  },

  animation: {
    duration: {
      fast:   "150ms",
      normal: "250ms",
      slow:   "400ms",
    },
    easing: {
      standard: "cubic-bezier(0.4, 0, 0.2, 1)",
      enter:    "cubic-bezier(0, 0, 0.2, 1)",
      exit:     "cubic-bezier(0.4, 0, 1, 1)",
    },
  },
} as const;

export type BrandColor = typeof brand.colors;
