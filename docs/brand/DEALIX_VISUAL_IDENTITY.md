# Dealix Visual Identity

> Companion to `DEALIX_BRAND_SYSTEM.md`. This file documents the **visual rules**.
> Tokens live in `docs/brand/brand-tokens.json` and `apps/web/lib/brand-tokens.ts`.

## 1. Core composition

| Element | Spec |
|---|---|
| Default background | `#0B1220` (Deep Navy) |
| Surface | `#0F1726` (Slate) |
| Accent | `#00D1A1` (Emerald Teal) |
| Body text | `#FFFFFF` |
| Secondary text | `#B2BBC6` (Soft Silver) |

All visual surfaces default to dark mode. Light mode is reserved for documents that are printed or rendered as PDF for legal use (invoices, contracts, NDAs).

## 2. Layout grid

- Base unit: 4 px.
- Page gutter: 24 px on desktop, 16 px on mobile.
- Content max-width: 1200 px for marketing, 1320 px for console.
- 12-column flexible grid; never break the gutter for decorative bleeds.

## 3. Surfaces hierarchy

1. `bg.primary` — page background.
2. `bg.surface` — cards, navigation, footers.
3. `bg.elevated` — modal, popovers, top-level dashboards.
4. Accent surfaces only as state (focus, active row, hovered link).

## 4. Hero composition

- Eyebrow in accent teal, uppercase, 0.24em tracking.
- Title in display weight 700, -0.01em letterspacing.
- Sub-line in `text.secondary`, max-width 620 px.
- Primary CTA in solid accent, secondary CTA as ghost.

## 5. Data visualisation

- Categorical palette derived from accent: `#00D1A1`, `#5AC8FA`, `#F2B33D`, `#FF6B6B`, `#B2BBC6`, `#7C8895`.
- Always include a textual summary alongside any chart.
- Charts must respect colour-blind safe pairs; do not encode meaning by colour alone.

## 6. Photography & illustration

- Photography is rare. When used, must include a navy overlay at 40 % opacity to preserve text contrast.
- Illustration uses line-art at 1.5 stroke, accent teal as a single highlight.
- No generic stock imagery.

## 7. Brand collateral

- Sales deck cover always uses the **full lockup** with tagline.
- Proposal cover uses the **compact lockup** plus customer name.
- LinkedIn header uses the **mark + wordmark** with positioning sub-line.
- Invoice header uses **wordmark only** on white background.
