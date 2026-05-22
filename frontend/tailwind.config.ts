import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        // Arabic-first (bilingual RTL support)
        arabic: ["'IBM Plex Sans Arabic'", "'Noto Sans Arabic'", "sans-serif"],
        // DEALIX brand display — Sora preferred, Space Grotesk fallback
        display: ["'Sora'", "'Space Grotesk'", "'Noto Sans Arabic'", "sans-serif"],
        // Body copy
        sans: ["'Manrope'", "'Plus Jakarta Sans'", "'Noto Sans Arabic'", "system-ui", "sans-serif"],
        mono: ["'JetBrains Mono'", "monospace"],
      },
      colors: {
        // ── DEALIX Brand Palette ────────────────────────────────────────
        // Deep Navy — trust, professionalism, primary background
        navy: {
          50:  "#e8eaf0",
          100: "#c5cadc",
          200: "#9ea8c6",
          300: "#7787b0",
          400: "#5a6ca0",
          500: "#3d5191",
          600: "#2d3c72",
          700: "#1e2854",
          800: "#111a38",
          900: "#0B1220",   // brand: Deep Navy
          950: "#070c18",
        },
        // Emerald Teal — growth, intelligence, primary CTA
        teal: {
          50:  "#e0fff8",
          100: "#b3ffee",
          200: "#80ffe3",
          300: "#4dffd7",
          400: "#26edbe",
          500: "#00D1A1",   // brand: Emerald Teal
          600: "#00a880",
          700: "#007d60",
          800: "#005240",
          900: "#002820",
          950: "#001410",
        },
        // Soft Silver — premium secondary text and UI chrome
        silver: {
          50:  "#f8f9fa",
          100: "#eef0f3",
          200: "#dde1e6",
          300: "#c8cfd8",
          400: "#B2BBC6",   // brand: Soft Silver
          500: "#97a2b0",
          600: "#788797",
          700: "#5c6b7a",
          800: "#424e5a",
          900: "#2a323b",
          950: "#151a1f",
        },
        // Slate — card surfaces, slightly lighter than navy
        slate: {
          50:  "#eaecf0",
          100: "#c9cdd8",
          200: "#a5abbe",
          300: "#8089a4",
          400: "#626d8e",
          500: "#465179",
          600: "#313c5e",
          700: "#1e2944",
          800: "#0F1726",   // brand: Slate
          900: "#0a1020",
          950: "#05080f",
        },
        // ── Semantic / shadcn UI tokens ─────────────────────────────────
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        chart: {
          "1": "hsl(var(--chart-1))",
          "2": "hsl(var(--chart-2))",
          "3": "hsl(var(--chart-3))",
          "4": "hsl(var(--chart-4))",
          "5": "hsl(var(--chart-5))",
        },
        sidebar: {
          DEFAULT: "hsl(var(--sidebar-background))",
          foreground: "hsl(var(--sidebar-foreground))",
          primary: "hsl(var(--sidebar-primary))",
          "primary-foreground": "hsl(var(--sidebar-primary-foreground))",
          accent: "hsl(var(--sidebar-accent))",
          "accent-foreground": "hsl(var(--sidebar-accent-foreground))",
          border: "hsl(var(--sidebar-border))",
          ring: "hsl(var(--sidebar-ring))",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      keyframes: {
        "accordion-down": {
          from: { height: "0" },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: "0" },
        },
        "fade-in": {
          from: { opacity: "0", transform: "translateY(8px)" },
          to: { opacity: "1", transform: "translateY(0)" },
        },
        "slide-in-right": {
          from: { opacity: "0", transform: "translateX(20px)" },
          to: { opacity: "1", transform: "translateX(0)" },
        },
        // DEALIX brand pulse — teal glow on CTA elements
        "pulse-teal": {
          "0%, 100%": { boxShadow: "0 0 0 0 rgba(0, 209, 161, 0.35)" },
          "50%":       { boxShadow: "0 0 0 10px rgba(0, 209, 161, 0)" },
        },
        shimmer: {
          "0%":   { backgroundPosition: "-1000px 0" },
          "100%": { backgroundPosition: "1000px 0" },
        },
        "teal-line": {
          "0%":   { transform: "scaleX(0)", opacity: "0" },
          "100%": { transform: "scaleX(1)", opacity: "1" },
        },
      },
      animation: {
        "accordion-down":  "accordion-down 0.2s ease-out",
        "accordion-up":    "accordion-up 0.2s ease-out",
        "fade-in":         "fade-in 0.4s ease-out forwards",
        "slide-in-right":  "slide-in-right 0.3s ease-out",
        "pulse-teal":      "pulse-teal 2s infinite",
        shimmer:           "shimmer 2s infinite linear",
        "teal-line":       "teal-line 0.6s ease-out forwards",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
};

export default config;
