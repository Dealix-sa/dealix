# Dealix Marketing Asset Guide

## 1. Asset inventory

| Asset | File path | Owner |
|---|---|---|
| Wordmark — full | `assets/brand/logo/dealix-full.svg` | Brand Guardian |
| Wordmark — compact | `assets/brand/logo/dealix-compact.svg` | Brand Guardian |
| Mark only | `assets/brand/icon/dealix-mark.svg` | Brand Guardian |
| Wordmark only | `assets/brand/wordmark/dealix-wordmark.svg` | Brand Guardian |
| Monochrome white | `assets/brand/monochrome/dealix-white.svg` | Brand Guardian |
| Monochrome navy | `assets/brand/monochrome/dealix-navy.svg` | Brand Guardian |
| LinkedIn header | `assets/brand/social/linkedin-header.png` | Marketing OS |
| OG image — generic | `assets/brand/social/og-default.png` | Marketing OS |
| OG image — proof | `assets/brand/social/og-proof.png` | Marketing OS |
| Favicon set | `assets/brand/favicons/` | Brand Guardian |

`apps/web/components/brand/dealix-logo.tsx` is the **inline SVG** used inside the Founder Console — it is the source of truth at runtime.

## 2. Asset creation checklist

Before any new brand asset is shipped:

- [ ] Tokens used match `docs/brand/brand-tokens.json`.
- [ ] Clearspace respected.
- [ ] Minimum size respected.
- [ ] Lock-up matches an approved variant.
- [ ] AR + EN versions produced if text is present.
- [ ] Accessibility contrast verified.
- [ ] Brand Guardian sign-off recorded.
- [ ] Asset stored under `assets/brand/`.

## 3. Template specs

| Template | Format | Notes |
|---|---|---|
| Sales deck | 16:9 PPTX / PDF | Cover uses full lockup with tagline |
| One-pager | A4 / Letter PDF | Compact lockup, brand grid |
| Proposal | A4 / Letter PDF | Compact lockup + customer name |
| Case study | A4 PDF + HTML | Bilingual, proof-bound |
| LinkedIn post | 1200 × 1200 | Mark + sentence |
| LinkedIn header | 1584 × 396 | Wordmark + positioning |
| OG image | 1200 × 630 | Wordmark + headline |

## 4. Approval flow

1. Asset drafted by Marketing OS or Brand Guardian.
2. Asset checked against this guide.
3. Asset committed to `assets/brand/` with a `CHANGELOG.md` entry.
4. Audit log records the brand change.

## 5. Versioning

Brand assets are versioned with the Dealix brand tokens. Bumps follow semver:

- **Major** — change to lockup, accent colour, or wordmark.
- **Minor** — change to monochrome variant, new lockup added.
- **Patch** — file format updates, minor optical fixes.

Current version: **1.0.0**.

## 6. Distribution

External distribution of brand assets to partners or customers must come from `assets/brand/` only — never from generative AI tools. Partners receive a sealed brand pack via the partner portal.
