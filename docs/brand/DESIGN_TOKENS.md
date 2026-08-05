# Dealix Brand — Design Tokens

> **Source of truth:** [`design-systems/dealix-brand/tokens.json`](../../design-systems/dealix-brand/tokens.json)
> · [`design-systems/dealix-brand/tokens.css`](../../design-systems/dealix-brand/tokens.css)
>
> This file is the **human-readable** reference. The JSON and CSS files are
> the **machine-readable** equivalents — they must stay in sync. If you edit
> one, edit all three.

---

## How tokens flow

```
docs/brand/DESIGN_TOKENS.md         (this file — readable spec, rationale)
design-systems/dealix-brand/tokens.json   (Figma / build pipelines / Storybook)
design-systems/dealix-brand/tokens.css    (drop into landing/, dashboard/, frontend/)
```

Any new token must be added in all three places in the same PR.

---

## 1. Colour tokens

### 1.1 Brand anchors

| Token | Hex | Notes |
|---|---|---|
| `color.brand.navy` | `#0B1220` | Primary dark surface |
| `color.brand.teal` | `#00D1A1` | On-dark accent only — fails AA on white |
| `color.brand.silver` | `#B2BBC6` | On-dark muted — fails AA on white |
| `color.brand.slate` | `#0F1726` | Alt dark surface |
| `color.brand.white` | `#FFFFFF` | |

### 1.2 Functional extensions

| Token | Hex | Notes |
|---|---|---|
| `color.brand.teal-ink` | `#007A5C` | Teal accent for light backgrounds — AA pass (5.3:1 on white) |
| `color.text.muted-light` | `#6B7480` | Muted body on light — AA pass (4.6:1 on white) |
| `color.surface.tint-navy` | `#E8EBF1` | Light-mode alt surface (1.5% navy tint) |

### 1.3 State

| Token | Hex |
|---|---|
| `color.state.success` | `#10B981` |
| `color.state.warn` | `#F59E0B` |
| `color.state.danger` | `#EF4444` |
| `color.state.info` | `#60A5FA` |

### 1.4 Semantic aliases (recommended for app code)

Code should reach for **semantic** names, not raw brand names — that way a
future theme swap (say, a light-mode dashboard) doesn't require a global
find-and-replace.

| Alias | Resolves to (dark mode) | Resolves to (light mode) |
|---|---|---|
| `bg.surface` | `color.brand.navy` | `color.brand.white` |
| `bg.surface-alt` | `color.brand.slate` | `color.surface.tint-navy` |
| `text.primary` | `color.brand.white` | `color.brand.navy` |
| `text.muted` | `color.brand.silver` | `color.text.muted-light` |
| `accent.primary` | `color.brand.teal` | `color.brand.teal-ink` |
| `accent.contrast` | `color.brand.navy` (on teal) | `color.brand.white` (on teal-ink) |

---

## 2. Typography tokens

### 2.1 Families

| Token | Stack |
|---|---|
| `font.display` | `"Space Grotesk", system-ui, -apple-system, "Segoe UI", sans-serif` |
| `font.ui` | `"Inter", system-ui, -apple-system, "Segoe UI", sans-serif` |
| `font.ar` | `"IBM Plex Sans Arabic", system-ui, "Geeza Pro", "Tahoma", sans-serif` |
| `font.mono` | `"JetBrains Mono", ui-monospace, "SF Mono", "Cascadia Code", monospace` |

### 2.2 Type scale

| Token | Size | Line-height | Weight | Family |
|---|---|---|---|---|
| `type.display.xl` | 64 px / 4 rem | 1.05 | 700 | display |
| `type.display.l` | 48 px / 3 rem | 1.10 | 700 | display |
| `type.display.m` | 36 px / 2.25 rem | 1.15 | 600 | display |
| `type.heading.l` | 28 px / 1.75 rem | 1.25 | 600 | display |
| `type.heading.m` | 22 px / 1.375 rem | 1.30 | 600 | ui |
| `type.heading.s` | 18 px / 1.125 rem | 1.35 | 600 | ui |
| `type.body.l` | 18 px / 1.125 rem | 1.55 | 400 | ui |
| `type.body.m` | 16 px / 1 rem | 1.55 | 400 | ui |
| `type.body.s` | 14 px / 0.875 rem | 1.50 | 400 | ui |
| `type.mono.m` | 14 px / 0.875 rem | 1.50 | 500 | mono |

Arabic line-height multiplier: **× 1.10** of the value above (handled by
`[lang="ar"] *` rule in `tokens.css`).

---

## 3. Spacing tokens

Spacing follows a 4 px base. Use the named tokens — never type raw pixel
values into a stylesheet.

| Token | Value | Use |
|---|---|---|
| `space.0` | 0 | reset |
| `space.1` | 4 px | hairline gaps inside chips |
| `space.2` | 8 px | icon→label, chip padding |
| `space.3` | 12 px | input row gaps |
| `space.4` | 16 px | paragraph rhythm, card inner padding |
| `space.5` | 24 px | section breathing inside a card |
| `space.6` | 32 px | between cards |
| `space.7` | 48 px | between major page regions |
| `space.8` | 64 px | hero top/bottom padding |
| `space.9` | 96 px | section breaks on the landing page |

---

## 4. Radius tokens

| Token | Value | Use |
|---|---|---|
| `radius.sm` | 6 px | chips, input fields |
| `radius.md` | 10 px | buttons, badges |
| `radius.lg` | 14 px | cards, modals |
| `radius.xl` | 20 px | hero cards, feature blocks |
| `radius.full` | 9999 px | pill buttons, avatars |

---

## 5. Shadow tokens

Shadows in the brand layer are **subtle** — Dealix is calm, not flashy.

| Token | Value (on dark) | Use |
|---|---|---|
| `shadow.sm` | `0 1px 2px rgba(0,0,0,0.20)` | resting cards, dividers |
| `shadow.md` | `0 4px 12px rgba(0,0,0,0.25)` | hovered card, dropdown |
| `shadow.lg` | `0 16px 40px rgba(0,0,0,0.35)` | modal, command palette |
| `shadow.glow.teal` | `0 0 24px rgba(0,209,161,0.25)` | CTA hover, hero accent — sparingly |

`shadow.glow.teal` is the **only** decorative glow allowed. Use it on the
primary CTA hover state, on the hero arrow accent, and nowhere else.

---

## 6. Motion tokens

| Token | Value | Use |
|---|---|---|
| `motion.duration.fast` | 120 ms | hover state, focus ring |
| `motion.duration.base` | 200 ms | button press, chip toggle |
| `motion.duration.slow` | 320 ms | modal open, drawer slide |
| `motion.easing.standard` | `cubic-bezier(0.2, 0, 0, 1)` | default for any UI movement |
| `motion.easing.entrance` | `cubic-bezier(0.0, 0, 0.2, 1)` | element appearing on screen |
| `motion.easing.exit` | `cubic-bezier(0.4, 0, 1, 1)` | element leaving |

Respect `prefers-reduced-motion: reduce` — disable all non-essential
animation when the user opts out.

---

## 7. Breakpoint tokens

Mobile-first. All breakpoints are min-width.

| Token | Value | Notes |
|---|---|---|
| `bp.sm` | 560 px | switch from stacked KPIs to side-by-side |
| `bp.md` | 720 px | introduce side-rails, sticky table headers |
| `bp.lg` | 1024 px | landing-page two-column layout |
| `bp.xl` | 1280 px | wide hero, max content width |
| `bp.2xl` | 1536 px | dashboard-grade multi-column |

---

## 8. Z-index tokens

Use a small, named scale — never `z-index: 9999`.

| Token | Value | Use |
|---|---|---|
| `z.base` | 0 | content |
| `z.raised` | 10 | hovered card, sticky table header |
| `z.dropdown` | 20 | menus, popovers |
| `z.overlay` | 30 | sheet, drawer |
| `z.modal` | 40 | modal dialogue |
| `z.toast` | 50 | notifications |
| `z.tooltip` | 60 | tooltips (always on top) |

---

## 9. Token export workflow

1. Edit `design-systems/dealix-brand/tokens.json` (canonical machine source).
2. Re-generate `tokens.css` (a sibling CSS file mirroring the JSON 1:1).
3. Update this `DESIGN_TOKENS.md` if any token name, value, or rationale changes.
4. PR description must list which of the three files moved and why.

A small Python script (not yet committed; track as future work) will
auto-generate `tokens.css` from `tokens.json` in CI. Until then, keep them
in sync by hand.
