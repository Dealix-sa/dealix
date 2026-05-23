# Dealix Typography

Dealix is bilingual (Arabic + English) by default. The type system supports both with a single, calibrated stack.

## 1. Type stack

### English / Latin

| Role          | Family                  | Weight        | Notes                                |
|---------------|-------------------------|---------------|--------------------------------------|
| Display       | `Inter`                 | 700, 800      | Heroes, section titles, KPI numbers  |
| Body          | `Inter`                 | 400, 500      | Default body text                    |
| Mono          | `JetBrains Mono`        | 400, 600      | Code, IDs, run logs                  |

### Arabic

| Role          | Family                  | Weight        | Notes                                |
|---------------|-------------------------|---------------|--------------------------------------|
| Display       | `IBM Plex Sans Arabic`  | 600, 700      | Heroes, section titles               |
| Body          | `IBM Plex Sans Arabic`  | 400, 500      | Default body text                    |

### CSS fallback stack

```css
font-family: Inter, "IBM Plex Sans Arabic", system-ui, -apple-system, "Segoe UI",
             "Helvetica Neue", Arial, sans-serif;
```

For mono:

```css
font-family: "JetBrains Mono", ui-monospace, "Cascadia Mono", Menlo,
             Consolas, monospace;
```

## 2. Type scale

A modular scale with 1.25 ratio, anchored at 16px body.

| Token        | Size       | Line-height | Use                                |
|--------------|------------|-------------|------------------------------------|
| `text-xs`    | 12px       | 1.4         | Captions, legal, footnotes         |
| `text-sm`    | 14px       | 1.5         | UI labels, metadata                |
| `text-base`  | 16px       | 1.6         | Default body                       |
| `text-lg`    | 18px       | 1.55        | Lead paragraphs                    |
| `text-xl`    | 20px       | 1.4         | Sub-section titles                 |
| `text-2xl`   | 24px       | 1.3         | Card titles, page sub-headings     |
| `text-3xl`   | 30px       | 1.25        | Section titles                     |
| `text-4xl`   | 36px       | 1.2         | Hero sub-line                      |
| `text-5xl`   | 48px       | 1.15        | Hero headline (mobile)             |
| `text-6xl`   | 60px       | 1.1         | Hero headline (desktop)            |

## 3. Tagline treatment

The canonical tagline is `Intelligent Deals. Real Growth.` and inside the brand lockup it appears as `INTELLIGENT DEALS. REAL GROWTH.` (uppercase, letter-spaced).

When used in copy:

- Always exactly `Intelligent Deals. Real Growth.` — capitalisation, spacing, and the period are part of the brand.
- Never localise to a different English form ("Smart deals", "Intelligent dealings").
- Arabic localisation: `صفقات ذكية. نمو حقيقي.` — same rules apply.

## 4. Hierarchy rules

- **One H1 per page.** It must contain a brand pillar word: *Trust*, *Growth*, *Deals*, *Results*, or the tagline itself.
- **H2** opens each major section.
- **Body** is `text-base` on dark; never lighter than Soft Silver against Deep Navy.
- **Numbers** (KPIs, prices, percentages) use the display weight (700–800) and the accent colour (Emerald Teal) to draw the eye.

## 5. RTL / LTR

- Set `dir` on the `<html>` element based on the active locale. Default is `ar`.
- Mirror layout (paddings, alignments) automatically — do not hard-code `text-align: left`.
- Numbers, prices, and timestamps remain LTR even inside RTL paragraphs.

## 6. Accessibility

- Body line-length: **45–75 characters** for English, **40–65 characters** for Arabic.
- Body line-height: never below 1.5.
- Letter-spacing: do not tighten body text below 0.

## 7. Loading & FOUT

- Load Inter and IBM Plex Sans Arabic with `font-display: swap` to avoid FOIT.
- Preload the body weight (400) of both families.
- Fallback (system-ui / Segoe UI) is acceptable; the design degrades gracefully.
