# Dealix Brand v2 — Logo Assets

> **Status:** Working approximations. Replace with designer master files when available.

## Files

| File | Use | Min size |
|------|-----|----------|
| `primary.svg`     | Stacked lockup — decks, posters, splash screens | 200 px wide |
| `icon.svg`        | Square mark — app icons, avatars, favicons (large) | 24 px |
| `horizontal.svg`  | Horizontal lockup — email signatures, navbars, headers | 120 px wide |
| `monochrome.svg`  | Single-ink white version — print, embroidery, on photos | 120 px wide |
| `favicon-32.svg`  | Simplified mark for browser tab | 16 px |

## Caveat

These SVGs preserve the visual system from the approved brand board (palette, lockup geometry, tagline placement, icon composition) but are **not pixel-parity** with the designer master. They are safe for internal docs, repo READMEs, and engineering surfaces. For external customer-facing artefacts (investor deck, signed proposals, paid ads, business cards) — wait for the master `.ai` / `.svg` from the designer.

## Replacement procedure

1. Drop the master `.svg` files in this directory using the same filenames.
2. Open each in a browser and verify the `viewBox` is preserved (so existing references don't break).
3. Update the `__meta.released` and a `__meta.logo_revision` field in `../../tokens.json`.
4. Note the swap in the project changelog.

## Palette reference

- Deep Navy `#0B1220`
- Emerald Teal `#00D1A1` (light hover `#34E3B5`, dark active `#00A37D`)
- Soft Silver `#B2BBC6`
- Slate `#0F1726`
- White `#FFFFFF`

See `../../tokens.json` for the full token set.
