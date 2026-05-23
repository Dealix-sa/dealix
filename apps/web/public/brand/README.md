# Dealix Brand Assets — Web Public

This folder holds **runtime-served** brand assets for the Next.js web app (`apps/web/`).

## Expected files

| File                              | Use                                  |
|-----------------------------------|--------------------------------------|
| `dealix-lockup.svg`               | Primary lockup (light text on dark)  |
| `dealix-lockup-onwhite.svg`       | Primary lockup (dark text on light)  |
| `dealix-icon.svg`                 | D monogram only (favicon, app icon)  |
| `dealix-wordmark.svg`             | Wordmark only                        |
| `og-card.png`                     | 1200×630 social/share image          |
| `favicon.ico`                     | Browser favicon                      |

## Manual step

Until the SVG/PNG exports from `assets/brand/source/dealix-brand-board.jpeg`
are placed here, the React `DealixLogo` component renders an **inline SVG
fallback** (D monogram + Emerald Teal swoosh + wordmark "DEALIX"). This
fallback is brand-accurate and ships fine to production.

Once the approved exports are placed here, update
`apps/web/components/brand/dealix-logo.tsx` to prefer the `<img>` form
when the SVG exists.

## Do not commit large binaries

PNGs > 200 KB should be optimised (e.g. with `oxipng`) before commit.
SVGs are preferred.
