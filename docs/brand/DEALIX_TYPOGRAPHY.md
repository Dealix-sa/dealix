# DEALIX Typography

> Wordmark: **DEALIX**
> Tagline: **INTELLIGENT DEALS. REAL GROWTH.**

This document defines the Dealix type system: the typefaces, the scale, the
bilingual stack, and the rules that make English and Arabic feel like the
same brand. Token values live in `brand-tokens.json` and
`apps/web/lib/brand-tokens.ts`.

---

## 1. The type stack

Dealix uses a two-script type stack: Latin and Arabic.

| Script | Primary face | Fallbacks |
| --- | --- | --- |
| Latin | **Inter** | system-ui, sans-serif |
| Arabic | **IBM Plex Sans Arabic** | system-ui, sans-serif |
| Monospace | ui-monospace | SFMono-Regular, Menlo, monospace |

The CSS stack:

```css
font-family: Inter, "IBM Plex Sans Arabic", system-ui, sans-serif;
```

The browser picks the appropriate face per character: Inter for Latin
glyphs, IBM Plex Sans Arabic for Arabic glyphs. The stack is intentional —
do not reorder it, and do not introduce additional faces without brand
director approval.

---

## 2. Why these typefaces

**Inter** is a workhorse geometric sans designed for screen legibility. It
ships with tabular figures, contextual alternates, and a complete weight
range. It carries the operator-grade aesthetic Dealix needs.

**IBM Plex Sans Arabic** is built on the same skeleton as Inter's siblings
in the IBM Plex family. It pairs visually with Inter and supports Naskh-
style Arabic with consistent stroke contrast. It avoids the calligraphic
flourish of Diwani or Thuluth, which would clash with the sober
enterprise tone.

Together, they give a bilingual surface that does not feel like two
products bolted together.

---

## 3. The scale

The type scale is a single ramp shared between Latin and Arabic. Sizes are
in pixels at 1× device pixel ratio.

| Token | Size | Line height | Use |
| --- | --- | --- | --- |
| `caption` | 12 px | 16 px | Captions, table footnotes |
| `xs` | 13 px | 18 px | Labels, helper text |
| `sm` | 14 px | 20 px | Secondary body |
| `base` | 16 px | 24 px | Body text |
| `md` | 18 px | 26 px | Lead body |
| `lg` | 20 px | 28 px | Section sub-heading |
| `xl` | 24 px | 32 px | Section heading |
| `2xl` | 28 px | 36 px | Page heading |
| `3xl` | 32 px | 40 px | Hero sub-heading |
| `4xl` | 40 px | 48 px | Hero heading (desktop) |
| `5xl` | 56 px | 64 px | Hero heading (oversize) |

The scale is opinionated. Do not introduce a 15 px size because "it looks
right" — pick the nearest token instead. If a use case truly demands a new
size, propose it to brand director with a justification.

---

## 4. Weights

| Weight | Inter | IBM Plex Sans Arabic | Use |
| --- | --- | --- | --- |
| 400 (Regular) | Inter Regular | Plex Arabic Regular | Body text |
| 500 (Medium) | Inter Medium | Plex Arabic Medium | Strong body, labels |
| 600 (Semibold) | Inter Semibold | Plex Arabic Semibold | Sub-headings, buttons |
| 700 (Bold) | Inter Bold | Plex Arabic Bold | Headings, wordmark |

Italic is **not** part of the system. Arabic does not have a true italic;
to keep Latin and Arabic visually aligned, we use weight (not slant) to
emphasize.

---

## 5. Bilingual rules

### 5.1 Direction
- The page direction is set on the `<html dir>` attribute.
- Arabic is `dir="rtl"` and Latin is `dir="ltr"`.
- A bilingual block (Arabic above English, or English above Arabic)
  inherits the page direction unless explicitly overridden with a
  `dir` attribute on the block.

### 5.2 Numerals
- Arabic prose uses **Arabic-Indic numerals** (٠١٢٣٤٥٦٧٨٩) where
  natural.
- Tables, dashboards, KPIs, dates, and any machine-readable surface use
  **ASCII numerals** (0123456789) so they stay sortable and copy-
  pasteable.
- Currency: SAR amounts in body copy can use either form depending on
  the script; in tables, always ASCII.

### 5.3 Line height
Arabic glyphs sit higher in the line-box than Latin glyphs. Use the same
numerical line-height as Latin (per the scale above) — the IBM Plex
Sans Arabic face has been measured to sit correctly inside that ramp.
Do not pad Arabic blocks with extra line-height.

### 5.4 Letter-spacing
- Latin headings: `0.01em` to `0.02em` (tight).
- Arabic headings: `0em` (Arabic does not benefit from positive
  tracking; it harms legibility).
- The wordmark "DEALIX" is the exception: `0.06em`, Latin only.

### 5.5 Mixing scripts in one sentence
When an Arabic sentence contains a Latin term (e.g. "Dealix"), do **not**
wrap the Latin term in italics or quotes by default. It will pick up the
Latin face from the stack automatically. Use quotes only for genuine
direct quotation.

---

## 6. RTL practicalities

- Use logical CSS properties (`margin-inline-start`, `padding-inline-end`,
  `inset-inline-start`) so layout mirrors automatically.
- Icons that carry directional meaning (arrows, chevrons) must mirror in
  RTL. Decorative icons (logo glyphs, abstract shapes) do not mirror.
- The Dealix mark itself does not mirror — the D stays a D — but its
  anchor moves to the right edge of the layout.
- The growth arrow inside the monogram does not mirror. It always points
  up-and-right.

---

## 7. Typographic surfaces

### 7.1 Marketing site
- Hero heading: `4xl` to `5xl`, Inter Bold, white on Deep Navy.
- Hero sub-heading: `xl`, Inter Medium, Soft Silver.
- Body: `base` to `md`, Inter Regular, white.
- Section heading: `2xl`, Inter Semibold.

### 7.2 Product app
- Page title: `2xl`, Inter Semibold.
- Section heading: `lg`, Inter Semibold.
- Body: `sm` to `base`, Inter Regular.
- Captions and labels: `xs`, Inter Medium, Soft Silver.
- Tabular figures enabled (`font-variant-numeric: tabular-nums`) in
  tables and KPI cards.

### 7.3 Sales deck
- Slide title: `4xl`, Inter Bold.
- Sub-title: `xl`, Inter Medium.
- Body: `md`, Inter Regular.
- Quote: `lg`, Inter Medium, italic-free.

### 7.4 Proposal
- Section heading: `2xl`, Inter Semibold.
- Body: `base`, Inter Regular.
- Pricing: `xl`, Inter Bold.
- Footnotes: `xs`, Inter Regular, Soft Silver.

### 7.5 Sector report
- Report title: `4xl`, Inter Bold.
- Section heading: `2xl`, Inter Semibold.
- Body: `base`, Inter Regular.
- Methodology and disclosure: `xs`, Inter Regular.

### 7.6 Email
- Subject (rendered by the client): no control.
- Body: 16 px Inter Regular (with system fallbacks for clients that
  strip web fonts).
- Signature wordmark image: PNG export at 2× resolution.

---

## 8. Loading fonts

- Self-host Inter and IBM Plex Sans Arabic. Do not link to Google Fonts
  in production for privacy reasons (PDPL compliance).
- Use `font-display: swap` for graceful fallback to system fonts.
- Subset Inter to Latin + Latin Extended; subset Plex Arabic to Arabic
  + common punctuation. Subsetting cuts payload by roughly 60%.
- Preload the regular and semibold weights only; the rest can lazy-load.

---

## 9. Accessibility

- Body text never goes below 14 px on production surfaces.
- Captions at 12 px must clear WCAG AA contrast — see
  `DEALIX_COLOR_SYSTEM.md`.
- Heading hierarchy follows HTML semantics: one `h1` per page, `h2`
  for top-level sections, `h3` for sub-sections. Do not skip levels
  for visual styling.
- Arabic accessibility: ensure the `lang="ar"` attribute is set on
  Arabic blocks so screen readers select the correct voice.

---

## 10. Forbidden uses

- Do **not** apply text shadows for "depth".
- Do **not** use letter-spacing > 0.06em in body text.
- Do **not** use all-caps for body copy in either script.
- Do **not** mix Inter with another sans (Roboto, Open Sans, Helvetica,
  Arial) in the same surface.
- Do **not** substitute IBM Plex Sans Arabic with Tajawal, Cairo, or
  Almarai. They are good faces — they are not Dealix.
- Do **not** render Arabic in a Latin font (it will fall through to
  Notos at best, mojibake at worst).

---

## 11. Bilingual note — العربية

نظام الطباعة مبني على خطّي Inter للحروف اللاتينية و IBM Plex Sans Arabic
للحروف العربية. هذان الخطّان متوافقان بصرياً ويعطيان السطح اللغوي المختلط
شعور وحدة واحدة. السلّم المقاسي مشترك بين اللغتين: لا نضيف فراغاً إضافياً
للنص العربي. الأرقام في النص الجاري يمكن أن تكون عربية-هندية (٠١٢٣)، أما
في الجداول ولوحات القيادة فتُكتب بالأرقام اللاتينية (0123) لضمان قابلية
الفرز والنسخ. الاتجاه الافتراضي للعربية هو RTL، ونستخدم خصائص CSS منطقية
(`margin-inline-start`، `padding-inline-end`) ليتم الانعكاس تلقائياً.

---

## 12. Token reference

```json
{
  "typography": {
    "heading": "Inter, 'IBM Plex Sans Arabic', system-ui, sans-serif",
    "body":    "Inter, 'IBM Plex Sans Arabic', system-ui, sans-serif",
    "mono":    "ui-monospace, SFMono-Regular, Menlo, monospace"
  }
}
```

Any code path that sets a font family must read from this token. If a
component hard-codes `"Inter, sans-serif"` and skips Plex Arabic, it
will fail brand review and may render Arabic in a fallback face.
