# Dealix Logo Usage

## 1. Variants and when to use each

| Variant | File | When to use |
|---|---|---|
| **Full signature** | `assets/brand/logo/dealix-logo-full.svg` | Landing hero, decks, proposal cover, social card, founder console header. |
| **Mark only** | `assets/brand/icon/dealix-mark.svg` | Favicon, app icon, avatar, compact nav, footer. |
| **Wordmark only** | `assets/brand/wordmark/dealix-wordmark.svg` | Documents where the mark would compete with diagrams. |
| **Monochrome dark** | `assets/brand/monochrome/dealix-mark-mono.svg` | Print on white, embossing, single-color contexts. |

## 2. Component vs asset

Inside the web app, prefer the React component:

```tsx
import { DealixLogo } from "@/components/brand/dealix-logo";

<DealixLogo height={32} withTagline />     // full lockup
<DealixLogo variant="wordmark" height={28} />
<DealixLogo variant="mark" height={24} />
```

Use the SVG files when generating PDFs, slides, social cards, or
e-mail signatures.

## 3. Locked file naming

```
dealix-logo-full.svg       → full signature (default)
dealix-mark.svg            → monogram only
dealix-wordmark.svg        → wordmark only
dealix-mark-mono.svg       → monochrome mark
favicon.svg                → favicon (32-px optimized)
dealix-social-card.svg     → 1200×630 social / OG card
```

Never rename these in place — generate exports if you need different
sizes or formats.

## 4. Forbidden treatments

- ❌ Drop shadows that are not in the brand shadow tokens.
- ❌ Outer glow effects.
- ❌ Gradient fills on the wordmark.
- ❌ Removing the navy panel from the mark to "flatten" it.
- ❌ Showing the mark on a busy photo background.
- ❌ Re-arranging mark + wordmark into a horizontal lockup when only
  the stacked lockup is approved.

## 5. Social and avatar exports

- **OG / LinkedIn share:** export `dealix-social-card.svg` at 1200×630.
- **Twitter / X:** crop the OG card to 1200×675 keeping the mark and
  tagline on the left third.
- **Avatar (square):** export `dealix-mark.svg` to PNG at 400×400.
- **App icon (iOS / Android):** export the mark with the navy panel
  unchanged at 1024×1024, no transparency.
