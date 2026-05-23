# Dealix Brand Source Assets

This folder is the single source of truth for the **approved Dealix visual identity**.

## Manual step — place the approved logo board

If it does not already exist here, place the approved logo board image at:

```
assets/brand/source/dealix-brand-board.jpeg
```

Expected dimensions: 1500×900 (or any 5:3 ratio export of the approved brand board).

The board image is the visual reference for:

- Logo construction (D monogram + growth arrow + revenue bars + deal/list icon + teal swoosh)
- Wordmark: **DEALIX**
- Tagline: **INTELLIGENT DEALS. REAL GROWTH.**
- Colour calibration (Deep Navy `#0B1220`, Emerald Teal `#00D1A1`, Soft Silver `#B2BBC6`, Slate `#0F1726`, White `#FFFFFF`)

## What does NOT live here

- Production-only credentials, signed agreements, or customer logos — those live outside the repo under the private ops directory.
- Per-customer co-branded assets — those live under `clients/<customer>/brand/` once trust-gated.

## Export pipeline (manual)

When updating the master board, also export the following derivative formats into the sibling folders:

| Folder                          | Format(s)              | Notes                                          |
|---------------------------------|------------------------|------------------------------------------------|
| `assets/brand/logo/`            | SVG, PNG (1024, 512)   | Full lockup (D + wordmark + tagline)           |
| `assets/brand/icon/`            | SVG, PNG (512, 256, 64)| D monogram only — used as favicon, app icon    |
| `assets/brand/wordmark/`        | SVG, PNG (1024)        | "DEALIX" wordmark only                         |
| `assets/brand/monochrome/`      | SVG (black, white)     | Single-colour fallbacks for press / fax / B&W  |
| `assets/brand/social/`          | PNG (1200×630, 1080²)  | OG image, LinkedIn share, X card               |
| `assets/brand/favicons/`        | ICO, PNG (32, 16)      | Browser favicons                               |

## Approval

Every change to assets in this folder must be reviewed and approved by the founder before being referenced in production marketing surfaces. No external send may use a non-approved asset.
