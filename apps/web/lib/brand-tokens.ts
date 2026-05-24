// Dealix Brand Tokens
// Deep Navy + Soft Silver palette, WCAG 2.2 AA compliant pairings.

export const brand = {
  name: "Dealix",
  tagline: "Revenue Intelligence for Saudi B2B",
  palette: {
    deepNavy: "#0B1B2E",
    deepNavyAlt: "#10243C",
    softSilver: "#D6DCE4",
    paper: "#F5F7FA",
    ink: "#0F172A",
    mutedInk: "#475569",
    accent: "#3B82F6",
    success: "#16A34A",
    warning: "#D97706",
    danger: "#DC2626",
    gridLine: "#1E2E45",
  },
  typography: {
    family: 'Inter, "IBM Plex Sans Arabic", system-ui, -apple-system, sans-serif',
    weight: { regular: 400, medium: 500, semibold: 600, bold: 700 },
    scale: {
      display: "32px",
      h1: "24px",
      h2: "20px",
      h3: "16px",
      body: "14px",
      label: "12px",
    },
  },
  radius: { sm: "6px", md: "10px", lg: "14px", xl: "20px" },
  spacing: { xs: "4px", sm: "8px", md: "12px", lg: "16px", xl: "24px", "2xl": "32px" },
  shadow: {
    card: "0 1px 2px rgba(11,27,46,0.08), 0 4px 12px rgba(11,27,46,0.06)",
  },
  layout: { maxWidth: "1240px", sidebarWidth: "260px" },
} as const;

export type Brand = typeof brand;
