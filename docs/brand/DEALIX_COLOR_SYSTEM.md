# Dealix Color System

> Colour is policy. Tokens live in `docs/brand/brand-tokens.json`.

## 1. Roles

| Role | Token | Hex | Notes |
|---|---|---|---|
| Background — primary | `color.bg.primary` | `#0B1220` | Default page background |
| Background — surface | `color.bg.surface` | `#0F1726` | Cards, nav |
| Background — elevated | `color.bg.elevated` | `#162038` | Modals, popovers |
| Background — inverse | `color.bg.inverse` | `#FFFFFF` | Light-mode print only |
| Accent — primary | `color.accent.primary` | `#00D1A1` | Brand action, focus |
| Accent — hover | `color.accent.hover` | `#00B388` | Hover state |
| Accent — muted | `color.accent.muted` | `#0E3A30` | Filled chip backgrounds |
| Text — primary | `color.text.primary` | `#FFFFFF` | Body |
| Text — secondary | `color.text.secondary` | `#B2BBC6` | Labels, captions |
| Text — muted | `color.text.muted` | `#7C8895` | Disabled UI only |
| Text — inverse | `color.text.inverse` | `#0B1220` | On accent buttons |
| Border — subtle | `color.border.subtle` | `#1B2536` | Card edge |
| Border — strong | `color.border.strong` | `#2A3753` | Active card edge |
| Status — success | `color.status.success` | `#00D1A1` | Success badge |
| Status — warning | `color.status.warning` | `#F2B33D` | Warning badge |
| Status — danger | `color.status.danger` | `#FF6B6B` | Error / blocked |
| Status — info | `color.status.info` | `#5AC8FA` | Info badge |

## 2. Composition rules

- Default the page to `bg.primary`.
- Group content into `bg.surface` cards with `border.subtle` (1 px).
- Use accent **only** for action, brand, and state. Never decorate.
- Never apply two adjacent accent-saturated surfaces.

## 3. Accessibility

| Pair | Minimum ratio | Use |
|---|---|---|
| `text.primary` on `bg.primary` | ≥ 12 : 1 | body |
| `text.secondary` on `bg.primary` | ≥ 4.5 : 1 | labels |
| `text.muted` on `bg.primary` | ≥ 3 : 1 | disabled |
| `accent.primary` on `bg.primary` | ≥ 4.5 : 1 | links |
| `text.primary` on `accent.primary` | ≥ 4.5 : 1 | buttons |

Verifier: `scripts/verify_brand_system.py`.

## 4. Light mode

Light mode is reserved for **PDF exports** of invoices, contracts, NDAs and printed proposals. It uses:

| Role | Hex |
|---|---|
| Background | `#FFFFFF` |
| Surface | `#F4F6FB` |
| Text | `#0B1220` |
| Secondary | `#3D4A5C` |
| Accent | `#00B388` |

## 5. Forbidden combinations

- Accent text on accent background.
- Accent text on warning or danger background.
- Text muted on text muted (low contrast).
- Brand colour in any photographic colour treatment.
