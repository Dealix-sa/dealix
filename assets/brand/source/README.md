# Dealix Brand Source Assets

Place the approved **Dealix brand board** master file here as:

```
assets/brand/source/dealix-brand-board.jpeg
```

Approved colors (source of truth: [`docs/brand/brand-tokens.json`](../../../docs/brand/brand-tokens.json)):

| Role            | Hex       |
|-----------------|-----------|
| Deep Navy       | `#0B1220` |
| Slate (surface) | `#0F1726` |
| Emerald Teal    | `#00D1A1` |
| Soft Silver     | `#B2BBC6` |
| White           | `#FFFFFF` |

Approved wordmark: **DEALIX**
Approved tagline: **INTELLIGENT DEALS. REAL GROWTH.**

Subfolders:

- `../logo/` — full-color logo lockups (SVG primary)
- `../icon/` — square app icons & favicons
- `../wordmark/` — wordmark-only variants
- `../monochrome/` — mono lockups for low-color/print
- `../social/` — exported assets sized for social (do not link to external CDNs)
- `../favicons/` — favicon set for the Founder Console & landing

When you add new exports, register them in the brand assets registry:

```
private-ops/brand/brand_assets_registry.csv
```

Until the approved logo image is committed, the Founder Console uses the
SVG monogram in `apps/web/components/brand/dealix-logo.tsx` (also the
brand fallback for any UI that needs a logo).
