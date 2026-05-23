# DEALIX Typography

**Owner:** Brand Lead
**Source of truth:** `docs/brand/brand-tokens.json`

## Primary type family

**Inter** (system-ui, sans-serif fallback chain).

Inter is the wordmark, heading, and body family. It ships with broad weight coverage and high screen legibility at small sizes. The system-ui fallback ensures graceful degradation on devices without Inter installed.

CSS stack:

```
font-family: "Inter", system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
```

## Arabic fallback

For Arabic body and headings, fall back to a high-quality Arabic family with matching x-height and weight balance:

```
font-family: "Inter", "IBM Plex Sans Arabic", "Noto Sans Arabic", "SF Arabic", system-ui, sans-serif;
```

- Headings in Arabic should use IBM Plex Sans Arabic or Noto Sans Arabic at weight 600.
- Body in Arabic should use the same families at weight 400.
- Line-height for Arabic body is 1.7 (vs 1.5 for Latin) to accommodate diacritics.

## Type scale

Base size: 16px. Modular scale: 1.250 (major third).

| Step | Size | Line-height | Weight | Use |
|---|---|---|---|---|
| Display | 48px | 1.1 | 700 | Hero, deck cover |
| H1 | 39px | 1.2 | 700 | Page title |
| H2 | 31px | 1.25 | 600 | Section heading |
| H3 | 25px | 1.3 | 600 | Subsection |
| H4 | 20px | 1.4 | 600 | Card title |
| Body large | 18px | 1.6 | 400 | Lead paragraph |
| Body | 16px | 1.6 | 400 | Default body |
| Body small | 14px | 1.5 | 400 | Captions, table cells |
| Micro | 12px | 1.4 | 500 | Labels, eyebrows |

## Weights

Use only these weights:

- Regular 400
- Medium 500
- Semibold 600
- Bold 700

No Light, no Thin, no Black, no Italic Bold. Italic is reserved for emphasis at body weight only.

## Tracking

| Use | Tracking |
|---|---|
| Display | -20 |
| H1 | -10 |
| H2 / H3 | -5 |
| Body | 0 |
| Micro / eyebrow | +50 (uppercase) |

## Hierarchy rules

1. One Display per surface. Two competing Displays read as noise.
2. Skip levels only one step (H1 to H3) at most. Skipping creates structural ambiguity.
3. Body text is never set below 14px on screen.
4. Body text on Deep Navy uses Soft Silver `#B2BBC6` or White `#FFFFFF`, not pure Emerald Teal.

## Tabular numbers

Use Inter's `tnum` OpenType feature for any column of numbers (pricing tables, scorecards, ledgers):

```
font-feature-settings: "tnum" 1;
```

## RTL handling

When rendering Arabic and Latin in the same surface:

- Wrap Arabic blocks in `dir="rtl"` and Latin blocks in `dir="ltr"`.
- Mirror padding and margin tokens at the layout level, not the type level.
- Do not force-align mixed content; let the bidi algorithm handle it.

See `DEALIX_ACCESSIBILITY_GUIDE.md` for full RTL guidance.

## Failure mode

- Arabic body rendered in Inter only (no Arabic glyph coverage — falls to default browser font).
- Display set at body size, creating two H1 reads on one surface.
- Italic used for entire paragraphs.
- Tabular numbers turned off in a pricing table, producing column drift.

## Recovery path

1. Replace with the correct token from the type scale.
2. Add the Arabic font stack if Arabic glyphs are missing.
3. Re-render and re-export.

## Disclaimer

Typography choices carry the same brand-promise weight as color. A misset proposal is a trust signal — and it points the wrong way.
