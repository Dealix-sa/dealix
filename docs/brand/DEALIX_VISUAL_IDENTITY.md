# DEALIX Visual Identity

> Wordmark: **DEALIX**
> Tagline: **INTELLIGENT DEALS. REAL GROWTH.**

This document describes the visual identity of Dealix: what the mark is made
of, how it is constructed, and how it must be placed. It is the upstream
source for `DEALIX_LOGO_USAGE.md`, which covers the do/don't surface.

The visual identity is dark, sober, and operator-grade. It exists to make
Saudi enterprise buyers comfortable signing a contract with us — not to win
design awards.

---

## 1. The mark — what it is made of

The Dealix mark is a single composition with four embedded elements:

1. **D monogram.** A geometric, slightly rounded uppercase D. It is the
   structural anchor of the mark. The D is drawn on a 24-unit grid, with the
   stem at 4 units wide and the bowl traced from a 16-unit radius.
2. **Growth arrow.** An upward arrow embedded in the negative space of the D.
   The arrow rises from the baseline to the upper-right quadrant of the D.
   It carries the second pillar — "Driven by Growth" — into the form itself.
3. **Revenue bars.** Three vertical bars of increasing height, set inside the
   bowl of the D, behind the growth arrow. They evoke a small bar chart and
   carry the "Focused on Results" pillar.
4. **Teal swoosh.** A narrow Emerald Teal (`#00D1A1`) stroke that arcs from
   the top-right of the D, curves over the growth arrow, and resolves at the
   wordmark. It is the only chromatic accent in the mark. Everything else is
   in the monochrome navy/white range.

The mark is read at a glance as a single character with motion inside it. It
is not four separate icons sitting next to each other.

---

## 2. The wordmark

The wordmark is **DEALIX**, set in Inter Bold, all caps, with letter-spacing
tuned to `0.06em`. The wordmark sits to the right of the monogram in the
primary lockup, with a gap equal to the cap height of the wordmark.

The wordmark is never set in a serif typeface, never set in lowercase, and
never set in a typeface other than Inter (or, where Inter is not technically
available, a near-identical geometric sans).

---

## 3. The tagline

The tagline is **INTELLIGENT DEALS. REAL GROWTH.** It is set in Inter Medium,
all caps, with letter-spacing `0.12em`. It is placed under the wordmark,
left-aligned to the wordmark, at a type size between 38% and 50% of the
wordmark cap height.

The tagline is optional in product UI. It is mandatory on the marketing site
hero, the sales deck cover, the proposal cover, and the email signature
header.

---

## 4. Construction grid

The mark is built on a 24-unit grid. The clear-space envelope is computed
from the grid, not from the pixel size of the rendered mark.

| Element | Grid units |
| --- | --- |
| Mark height | 24 |
| Mark width | 22 |
| Stem width (D) | 4 |
| Bowl radius (D) | 16 |
| Arrow stem width | 2.5 |
| Revenue bar widths | 2, 2, 2 |
| Revenue bar heights | 6, 9, 12 |
| Teal swoosh stroke | 2 |

Designers should not rebuild the mark from scratch. The canonical SVG lives
in `assets/brand/source/` and is the only file allowed for production.

---

## 5. Clear-space

Clear-space is the minimum empty area around the mark. Nothing — text,
border, image edge — may enter that area.

- **Minimum clear-space** on all four sides equals the height of the **D**
  stem in the mark (i.e. 4 grid units, or about 16.7% of the mark height).
- **Preferred clear-space** is double the minimum.
- On dark backgrounds, clear-space is calculated from the visible edge of the
  white/silver part of the mark, not from the teal swoosh tail.

---

## 6. Scale

| Use | Minimum height | Recommended height |
| --- | --- | --- |
| Favicon, app icon | 16 px | 32 px+ |
| Web nav | 24 px | 32 px |
| Email signature | 28 px | 36 px |
| Document header | 32 px | 48 px |
| Deck cover | 80 px | 120 px+ |
| Billboard / event backdrop | 240 px | 480 px+ |

Below 16 px, switch to the **monogram-only** lockup. Below 12 px, do not use
the mark at all — use the wordmark in plain text instead.

---

## 7. Placement rules

- **Default placement** is top-left in LTR layouts and top-right in RTL
  layouts. Logical CSS properties (`margin-inline-start`) handle this
  automatically in the web app.
- The mark is **left-aligned in LTR**, **right-aligned in RTL**. It is not
  mirrored — the D stays a D — but its anchor moves.
- On hero sections, the mark may sit centered above a centered headline. It
  must not float in the middle of a busy image.
- The mark is never tilted, never animated except by the teal swoosh
  pulsing once on first paint (optional), and never set on a photograph
  without a navy or slate overlay at 80%+ opacity to preserve contrast.

---

## 8. Lockups

The mark exists in five sanctioned lockups. Anything else is bespoke and
must be approved by the brand director.

1. **Primary horizontal.** Monogram + wordmark + (optional) tagline.
2. **Stacked.** Monogram above wordmark, with the tagline below. Used on
   deck covers and printed materials.
3. **Monogram-only.** The D mark alone. Used in tight UI corners, app icons,
   favicons.
4. **Wordmark-only.** DEALIX in Inter Bold, no monogram. Used when the
   surface is already obviously Dealix (e.g. inside the product) and the
   monogram would be redundant.
5. **Mono partner lockup.** Monogram + wordmark + a thin vertical rule + a
   partner mark, all in white-on-navy. Used in co-branded artifacts.

---

## 9. Color rendering of the mark

The mark has three sanctioned color renderings:

- **Primary.** White monogram + white wordmark + Emerald Teal swoosh on Deep
  Navy or Slate background.
- **Reverse.** Deep Navy monogram + Deep Navy wordmark + Emerald Teal
  swoosh on White background.
- **Monochrome.** Single color (white, navy, or black) for the entire mark
  including the swoosh. Used where teal printing is not possible (e.g.
  fax-grade documents, embroidery, regulator submissions in B/W).

Never recolor the swoosh to anything other than Emerald Teal `#00D1A1` —
unless the entire mark is monochrome.

---

## 10. Backgrounds the mark may sit on

| Background | Allowed | Notes |
| --- | --- | --- |
| Deep Navy `#0B1220` | Yes | Primary surface |
| Slate `#0F1726` | Yes | Secondary surface |
| White `#FFFFFF` | Yes | Use Reverse rendering |
| Soft Silver `#B2BBC6` | No | Insufficient contrast for white mark |
| Emerald Teal `#00D1A1` | No | Mark and accent collide |
| Photograph | Conditional | Requires navy 80%+ overlay |
| Gradient | No | Reads as decorative; off-brand |

---

## 11. Motion (when the mark animates)

The mark is mostly static. The one sanctioned motion is a single,
quarter-second teal swoosh sweep on first paint of a hero surface. The sweep
runs left-to-right in LTR and right-to-left in RTL. It does not loop and is
disabled when the user has `prefers-reduced-motion: reduce`.

---

## 12. File formats and source of truth

Canonical sources live in `assets/brand/source/`:

- `dealix-mark.svg` — the primary mark
- `dealix-mark-mono.svg` — monochrome variant
- `dealix-wordmark.svg` — wordmark only
- `dealix-monogram.svg` — monogram only
- `dealix-favicon.svg` — favicon master

Exports (PNG, ICO, JPG) are derived from these sources. Never hand-edit an
export; regenerate it from source.

---

## 13. Bilingual note — العربية

شعار دِيليكس هو حرف **D** هندسي يحمل في فضائه السلبي سهماً صاعداً وثلاثة
أعمدة إيراد، تنتهي بقوس أخضر تركوازي. الكلمة "DEALIX" تكتب باللاتينية فقط
بخط Inter Bold، ولا تُترجم بصرياً. عند العرض في واجهات RTL يبقى الشعار بصيغته
الأصلية، لكن موضعه ينتقل إلى أعلى يمين الشاشة. الاستخدامات والأبعاد محددة
في `DEALIX_LOGO_USAGE.md`.
