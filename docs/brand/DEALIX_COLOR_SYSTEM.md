# DEALIX Color System

> Wordmark: **DEALIX**
> Tagline: **INTELLIGENT DEALS. REAL GROWTH.**

This document defines the Dealix color system: the five canonical colors,
their roles, their contrast behavior, and where each one is allowed to
appear. Token values are mirrored in `brand-tokens.json`,
`apps/web/lib/brand-tokens.ts`, and `apps/web/styles/brand.css`. Edit those
files only after this document has been updated.

---

## 1. The five colors

| Token | Name | Hex | Role |
| --- | --- | --- | --- |
| `deep_navy` | Deep Navy | `#0B1220` | Primary background |
| `slate` | Slate | `#0F1726` | Secondary surface |
| `emerald_teal` | Emerald Teal | `#00D1A1` | Primary accent / action |
| `soft_silver` | Soft Silver | `#B2BBC6` | Muted text, hairlines |
| `white` | White | `#FFFFFF` | Primary text on dark, reversed surface |

Anything outside this set is off-brand unless it is a state color (danger,
warning) or a semantic data color used inside a chart — see sections 6 and 7.

---

## 2. Why this palette

The palette is built around two ideas:

1. **Enterprise restraint.** Deep Navy and Slate carry the weight of a
   serious enterprise product. They give the user the visual cue that this
   is not a consumer toy.
2. **A single accent with intent.** Emerald Teal is the only chromatic
   color in the palette. Every appearance of teal is meaningful: a CTA, a
   live status, a growth signal, the swoosh in the mark. Because teal is
   scarce, it is always read as "the thing that matters here".

Soft Silver carries the muted body text and the structural hairlines. White
carries the primary text on dark surfaces. There is no purple, no orange, no
secondary brand accent, no gradient brand color. That restraint is the
brand.

---

## 3. Color roles

| Role | Token | Where it appears |
| --- | --- | --- |
| `background` | Deep Navy `#0B1220` | App background, marketing hero |
| `surface` | Slate `#0F1726` | Cards, modals, table rows |
| `primary` | Emerald Teal `#00D1A1` | Primary CTAs, active states, growth signals |
| `secondary` | Soft Silver `#B2BBC6` | Secondary buttons, muted icons |
| `text_primary` | White `#FFFFFF` | Body text on dark surfaces |
| `text_muted` | Soft Silver `#B2BBC6` | Captions, helper text |
| `border` | `#1f2a3a` | 1 px hairlines on dark surfaces |
| `danger` | `#ef4444` | Errors, destructive confirms |
| `warning` | `#f59e0b` | Warning chips, attention states |
| `success` | Emerald Teal `#00D1A1` | Success states (intentionally same as primary) |

The state colors (`danger`, `warning`) are utility colors. They are not
brand colors and do not appear in marketing surfaces.

---

## 4. Surface model

Dealix surfaces are layered. Each layer has a fixed color.

| Layer | Color | Example |
| --- | --- | --- |
| L0 | Deep Navy | Page background |
| L1 | Slate | Card, modal |
| L2 | Slate + 4% white overlay | Nested card, hover row |
| L3 | Slate + 8% white overlay | Selected row, tooltip |
| Reverse | White | Print, PDF body |

Designers should not introduce a new layer color. If a new layer is needed,
it is achieved by an overlay percentage, not by a new hex value.

---

## 5. Contrast and WCAG AA

All canonical color pairs must clear WCAG AA for the text size they carry.
The table below records the measured contrast ratios for the canonical
pairs.

| Foreground | Background | Ratio | WCAG AA (normal) | WCAG AA (large) |
| --- | --- | --- | --- | --- |
| White `#FFFFFF` | Deep Navy `#0B1220` | ~18.3:1 | Pass | Pass |
| White `#FFFFFF` | Slate `#0F1726` | ~16.1:1 | Pass | Pass |
| Soft Silver `#B2BBC6` | Deep Navy `#0B1220` | ~10.0:1 | Pass | Pass |
| Soft Silver `#B2BBC6` | Slate `#0F1726` | ~8.9:1 | Pass | Pass |
| Emerald Teal `#00D1A1` | Deep Navy `#0B1220` | ~9.7:1 | Pass | Pass |
| Emerald Teal `#00D1A1` | Slate `#0F1726` | ~8.5:1 | Pass | Pass |
| Deep Navy `#0B1220` | White `#FFFFFF` | ~18.3:1 | Pass | Pass |
| Deep Navy `#0B1220` | Soft Silver `#B2BBC6` | ~7.4:1 | Pass | Pass |

Pairs to **avoid** because they fail or barely clear:

| Foreground | Background | Notes |
| --- | --- | --- |
| Soft Silver `#B2BBC6` | White `#FFFFFF` | Too low contrast for body text |
| Emerald Teal `#00D1A1` | White `#FFFFFF` | ~2:1 — fails AA. Use Deep Navy instead. |
| Soft Silver `#B2BBC6` | Emerald Teal `#00D1A1` | Insufficient separation. |

When in doubt, run the pair through a contrast checker. Where the pair is
borderline, push the foreground to white or the background to Deep Navy.

---

## 6. Teal on white — a special rule

Emerald Teal `#00D1A1` is bright. On white, it has a contrast ratio of
roughly 2:1, which fails WCAG AA for text. Therefore:

- On white surfaces, **never** set body text in teal.
- On white surfaces, teal may appear as a non-text accent: an icon stroke,
  a chart bar, a thin underline on a hover state. The accessible label
  carrying the meaning must be in Deep Navy or near-black.
- On white surfaces, the primary CTA uses **Deep Navy as the button
  background** and white text — not teal. Teal is reserved for the dark
  surfaces where it earns its contrast.

---

## 7. Data and chart colors

When charts need more than one color, extend the palette deterministically:

| Series | Color | Notes |
| --- | --- | --- |
| 1 (primary) | Emerald Teal `#00D1A1` | Headline series |
| 2 | Soft Silver `#B2BBC6` | Comparison series |
| 3 | White `#FFFFFF` | Tertiary on dark |
| 4 | `#7AB8FF` | Cool blue, used sparingly |
| 5 | `#F5C26B` | Warm amber, used sparingly |

Series 4 and 5 are **not** brand colors. They exist only inside charts and
never appear in marketing or UI chrome.

---

## 8. Usage by surface

| Surface | Background | Primary text | Accent | Notes |
| --- | --- | --- | --- | --- |
| Marketing site (default) | Deep Navy | White | Emerald Teal | Hero on Deep Navy |
| Marketing site (white sections) | White | Deep Navy | Deep Navy | Teal as icon accent only |
| Product app | Deep Navy / Slate | White | Emerald Teal | Layered surfaces |
| Sales deck cover | Deep Navy | White | Emerald Teal | Mark + tagline |
| Sales deck body | White or Slate | Deep Navy or White | Emerald Teal | Pick one and hold it |
| Proposal cover | Deep Navy | White | Emerald Teal | |
| Proposal body | White | Deep Navy | Deep Navy | High-print contrast |
| Sector report | White | Deep Navy | Deep Navy | Print-grade |
| Email body | White | Deep Navy | Deep Navy | Maximize deliverability |
| Email signature | White | Deep Navy | Emerald Teal in mark only | |
| OG cards | Deep Navy | White | Emerald Teal | |

The rule of thumb: **dark surfaces use teal as the accent; light surfaces
use Deep Navy as the accent and reserve teal for the mark and small icons.**

---

## 9. Tokens and code wiring

All colors are exposed as design tokens.

### 9.1 JSON
`docs/brand/brand-tokens.json` is the source of truth.

### 9.2 TypeScript
`apps/web/lib/brand-tokens.ts` mirrors the JSON. Components import from
this file, never from a string literal.

### 9.3 CSS custom properties
`apps/web/styles/brand.css` exposes the tokens as CSS variables:

```css
:root {
  --dealix-bg: #0B1220;
  --dealix-surface: #0F1726;
  --dealix-primary: #00D1A1;
  --dealix-text: #FFFFFF;
  --dealix-muted: #B2BBC6;
}
```

Any new component must consume these variables. A component that
hard-codes a hex value other than for a clearly documented exception
(e.g. a state color) will fail brand review.

---

## 10. Forbidden colors

The following colors are explicitly forbidden in any Dealix surface:

- Pure black (`#000000`) on screen — Deep Navy reads as black with
  reduced eye strain.
- Bright primary blue (`#0066FF`, `#1E40AF`, etc.) — too close to legacy
  enterprise software palettes.
- Pure green (`#00FF00`, `#22C55E` at full saturation) — clashes with
  Emerald Teal.
- Saturated red except as the danger state color.
- Any gradient as a brand surface color.

---

## 11. Dark mode and light mode

Dealix is dark-first. The product app and marketing site default to the
Deep Navy / Slate surface model. A light mode exists for print, PDF
exports, and embedded views (e.g. a Dealix report viewed inside a
customer's portal). Light mode flips the surface model:

| Layer | Dark mode | Light mode |
| --- | --- | --- |
| L0 background | Deep Navy | White |
| L1 surface | Slate | `#F3F5F8` |
| L2 surface | Slate + 4% white | `#E7EBF0` |
| Primary text | White | Deep Navy |
| Muted text | Soft Silver | `#4A5563` |
| Accent | Emerald Teal | Deep Navy (text), Emerald Teal (icon) |

Light mode is not the default. A user does not toggle into light mode
casually — it is selected explicitly for an export context.

---

## 12. Bilingual note — العربية

نظام الألوان مبني على خمسة ألوان فقط: أزرق كحلي عميق، وسليت، وأخضر زمردي،
وفضّي ناعم، وأبيض. الأخضر الزمردي هو لون الإشارة الوحيد، ويُستخدم لتمييز
ما يهم: زرّ التنفيذ، الحالة الحيّة، إشارة النمو. على الأسطح البيضاء لا
يستخدم الأخضر للنص، بل للأيقونات فقط، ويُستبدل في زرّ التنفيذ بلون كحلي
عميق لضمان التباين. كل ثنائية لونية في الواجهة يجب أن تجتاز معيار WCAG AA
على الأقل.
