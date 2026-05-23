# DEALIX Marketing Asset Guide

**Owner:** Brand Lead
**Source of truth:** `docs/brand/brand-tokens.json` + `assets/brand/`

## Asset classes

| Class | Examples |
|---|---|
| Web banner | Landing hero, sector landing, blog header |
| Social card | LinkedIn post image, X card, IG carousel |
| Proposal | Cover, scope, pricing, appendix |
| Deck | Internal pitch, customer pitch, partner deck |
| Report | Diagnostic, sprint outcome, sector scorecard |
| Email header | Outbound draft template, nurture broadcast |

## Web banner specs

| Surface | Dimensions | Safe zone |
|---|---|---|
| Landing hero | 2880 x 1620 (16:9) | Center 1920 x 1080 |
| Sector landing | 2400 x 1200 (2:1) | Center 1600 x 800 |
| Blog header | 2400 x 1200 (2:1) | Center 1600 x 800 |

Default backdrop: Pipeline gradient (Deep Navy to Slate). Wordmark or lockup placed within safe zone. CTA in Emerald Teal.

## Social card specs

| Platform | Dimensions | Notes |
|---|---|---|
| LinkedIn post | 1200 x 627 | Wordmark top-left, single headline, single number |
| LinkedIn carousel | 1080 x 1080 (per slide) | 5-7 slides, one idea per slide |
| X card | 1200 x 675 | Same composition rules as LinkedIn |
| IG square | 1080 x 1080 | Wordmark optional, mark required |
| IG story | 1080 x 1920 | Safe zone center 1080 x 1500 |

See `DEALIX_SOCIAL_MEDIA_KIT.md` for content templates.

## Proposal specs

- Page size: A4 portrait (210 x 297 mm) or US Letter (8.5 x 11 in).
- Margins: 25 mm.
- Cover: full-bleed Pipeline gradient, lockup top-left, customer name top-right, document title centered vertically.
- Body: White background, Deep Navy text, Inter at body 16px equivalent (11pt print).
- Footer on every page: wordmark left, page number center, disclosure right.

See `DEALIX_PROPOSAL_TEMPLATE_GUIDE.md` for full structure.

## Deck specs

- Aspect ratio: 16:9, slide size 1920 x 1080.
- Default backdrop: Deep Navy.
- Title slide: lockup centered, Emerald swoosh behind.
- Section divider: full-bleed Pipeline gradient with section number top-left, section title centered.
- Content slide: max one H2, max three H3, max one chart, max one table. No slide carries all four.
- Speaker notes: founder-voice, conversational, not duplicating the slide.

See `DEALIX_SALES_DECK_GUIDE.md` for the 12-slide structure.

## Report specs

- Page size: A4 portrait.
- Cover: same as proposal cover, with report type tag (Diagnostic / Sprint / Scorecard) in Emerald Teal Micro caps.
- Methodology section is mandatory.
- Aggregated data only. No PII.
- Closing page: disclosure block, version stamp, owner name.

See `DEALIX_REPORT_TEMPLATE_GUIDE.md` for templates.

## Email header specs

- Width: 600 px (standard email client safe width).
- Height: 120 px.
- Background: Deep Navy.
- Wordmark left, tagline right (Micro caps, Soft Silver).
- No images in the body of cold or first-touch emails. Plain text wins deliverability.

## File naming convention

```
dealix-{class}-{surface}-{name}-{lang}-{version}.{ext}
```

Examples:

- `dealix-banner-landing-hero-en-v3.png`
- `dealix-deck-customer-pitch-ar-v2.pdf`
- `dealix-proposal-cover-acme-en-v1.indd`

## Versioning

- v1 — first release
- v2, v3 — content updates
- vX-draft — pre-approval
- vX-final — approved and published

Only `final` versions go to customers.

## Approval (trust gates)

| Asset | Trust gate |
|---|---|
| Internal deck | A0 — self |
| Template deck | A1 — Brand Lead |
| Customer proposal | A2 — Founder + Brand Lead |
| Press, partner co-brand | A3 — Founder only |

## Failure mode

- Customer proposal published as `vX-draft`.
- Social card with off-aspect-ratio crop, cutting the wordmark.
- Email header with an image-only logo (renders broken in many clients).

## Recovery path

1. Replace asset with the correct `final` version.
2. Re-export from `assets/brand/`.
3. Log the incident in the Brand Lead's quarterly review note.

## Disclaimer

Marketing assets are vehicles for evidence, not for promise. Any number, claim, or outcome on a marketing surface must be sourceable to a dated, founder-approved record. Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
