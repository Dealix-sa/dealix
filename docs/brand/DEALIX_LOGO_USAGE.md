# Dealix Logo Usage

> Logo policy. Any deviation must be approved by the Brand Guardian and recorded in the audit log.

## 1. Concept

The Dealix logo combines four conceptual marks into one identity system:

1. **`D` monogram** — the company name, the stability anchor.
2. **Growth arrow** — a single line that climbs through the `D`, exiting up-right.
3. **Revenue bars** — three ascending bars suggesting consecutive months of growth.
4. **Deal / list icon** — implied by the rhythm of the bars; visible explicitly on the long-form mark.

A **teal swoosh** ties the arrow tip to the brand accent.

## 2. Approved files

Stored under `assets/brand/`:

```
assets/brand/source/    # Editable source files (SVG, native)
assets/brand/logo/      # Primary horizontal lockups (full, compact)
assets/brand/wordmark/  # Wordmark-only files
assets/brand/icon/      # `D` mark only
assets/brand/monochrome/# White-only and Navy-only variants
assets/brand/social/    # OG images, LinkedIn header crops
assets/brand/favicons/  # 16, 32, 48, 192, 512 px PNGs and ICO
```

`apps/web/components/brand/dealix-logo.tsx` is the canonical **inline SVG** used inside the Founder Console and product UI.

## 3. Lockup specifications

| Lockup | Components | Use |
|---|---|---|
| **Full horizontal** | mark + wordmark + tagline (silver) | Decks, hero, proposals |
| **Compact horizontal** | mark + wordmark | Console nav, footers |
| **Stacked vertical** | mark centred above wordmark | Square avatars, social |
| **Mark only** | `D` mark with swoosh | Favicons, app icons |
| **Wordmark only** | `DEALIX` in display weight 800 | Document headers, invoices |

## 4. Clearspace

Minimum clearspace on every side equals the cap height of the `D` mark. Inside this zone: **no text, no icons, no UI chrome**.

## 5. Minimum sizes

| Lockup | Digital | Print |
|---|---|---|
| Full | 220 px wide | 64 mm wide |
| Compact | 96 px wide | 32 mm wide |
| Mark only | 24 px | 8 mm |
| Wordmark only | 120 px | 40 mm |

## 6. Background rules

| Background | Approved lockup |
|---|---|
| Navy `#0B1220` | full-colour or monochrome white |
| Surface `#0F1726` | full-colour |
| White `#FFFFFF` | monochrome navy |
| Photographic | full-colour, only over navy plate (≥ 40 % opacity) |

## 7. Prohibited treatments

- Recolouring outside the approved palette.
- Adding gradients, shadows, outlines, glows, bevels.
- Rotating, skewing, stretching, mirroring.
- Combining with other logos in a lock-up.
- Animating the mark beyond the approved 200 ms ease.
- Reconstructing in third-party generative AI tools without Brand Guardian approval.

## 8. Co-branding

When co-branding with a customer or partner, place the partner mark to the right of the Dealix lockup with **two clearspace units** between them and a vertical 1 px divider in `border.subtle`.

## 9. Misuse review

Every brand misuse incident — internal or external — is recorded in `assets/brand/misuse-log.md` and reviewed monthly by the Brand Guardian.
