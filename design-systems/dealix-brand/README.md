# `design-systems/dealix-brand/`

> Machine-readable companion to [`docs/brand/`](../../docs/brand/).
> The narrative + rationale lives in the docs folder; **this folder is the
> implementation** (JSON for build tools, CSS for direct consumption).

## Files

- `tokens.json` — canonical, machine-readable design tokens (Figma plugins,
  build pipelines, Storybook themes).
- `tokens.css` — CSS custom properties mirroring `tokens.json` 1:1. Drop
  into any HTML page that renders Dealix brand surfaces.
- `README.md` — this file.

## How to use the tokens in code

### In `landing/` (vanilla HTML/CSS)

```html
<!doctype html>
<html lang="en" dir="ltr" data-theme="dark">
  <head>
    <link rel="stylesheet" href="/design-systems/dealix-brand/tokens.css">
    <link rel="stylesheet" href="/landing/styles.css">
  </head>
  <body>
    <h1 style="font: var(--type-display-l-weight) var(--type-display-l-size)/var(--type-display-l-lh) var(--font-display); color: var(--text);">
      Intelligent Deals. Real Growth.
    </h1>
  </body>
</html>
```

### Light-mode containers (within an otherwise dark page)

```html
<aside data-theme="light" class="press-card">
  <!-- everything inside resolves to the light palette -->
</aside>
```

### Arabic block (RTL)

```html
<section lang="ar" dir="rtl">
  <h2>صفقات ذكية. نموّ حقيقي.</h2>
</section>
```

The `[lang="ar"]` selector in `tokens.css` automatically switches to
IBM Plex Sans Arabic and bumps body line-height by 10%.

## Relationship to the operational design system

This folder is the **brand layer**. The **operational layer** lives at
`design-systems/dealix/` and uses a separate Saudi-green palette (`#0A5C36`,
`#C8A86A`) for customer-facing artefacts.

| Folder | Palette anchor | Use it for |
|---|---|---|
| `design-systems/dealix-brand/` (this folder) | Navy / Teal | Marketing, investor, web, GitHub, social |
| `design-systems/dealix/` | Saudi Green / Sand Gold | Customer proof packs, dashboards, executive emails |

The two are deliberately distinct. Don't merge their tokens, and don't
import one into the other.

## Editing tokens

Every change must update **all three** of:

1. `tokens.json` (this folder)
2. `tokens.css` (this folder)
3. `docs/brand/DESIGN_TOKENS.md` (rationale + human reference)

A future CI script will auto-generate `tokens.css` from `tokens.json`. Until
then, keep them in sync by hand and call out any drift in PR review.
