# Dealix Brand Source — Manual Upload

**Owner:** Brand Lead
**Source of truth:** `docs/brand/brand-tokens.json`

## Manual step required

Place the approved Dealix brand board here as:

```
assets/brand/source/dealix-brand-board.jpeg
```

The board carries the master wordmark, the growth arrow, the emerald swoosh, and the approved color chips. It is the single source of visual truth for all subsequent exports.

## Next step (automated brand build)

Once the brand board is in place, the wordmark, growth arrow, and emerald swoosh assets will be exported into the following directories during the next brand build:

```
assets/brand/logo/
assets/brand/icon/
assets/brand/wordmark/
assets/brand/monochrome/
assets/brand/social/
assets/brand/favicons/
```

Expected output naming follows `docs/brand/DEALIX_MARKETING_ASSET_GUIDE.md`.

## Until the upload

Without the brand board in place, downstream brand-build automation will skip export and log a `BRAND_SOURCE_MISSING` warning. UI and document templates fall back to typographic-only wordmark rendering (Inter Semibold, tracking -10, Emerald Teal on Deep Navy).

## What NOT to do

- Do not place draft or unapproved boards in this directory.
- Do not rename the file.
- Do not commit raw vendor exports (PSD, AI) here — those belong in a private design vault.
- Do not modify the board after placement; replace it with a versioned successor.

## Failure mode

- Brand build fails silently because the file is missing or renamed.
- Customer surfaces render with system fonts instead of the wordmark.

## Recovery path

1. Confirm file name matches `dealix-brand-board.jpeg` exactly.
2. Re-run the brand build.
3. Inspect `assets/brand/{logo,icon,wordmark,monochrome,social,favicons}/` for the expected files.

## Disclaimer

This directory carries no claims, no customer data, and no contractual content. It carries brand source files only.
