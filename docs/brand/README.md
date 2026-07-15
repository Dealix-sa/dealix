# Dealix Brand Layer — `docs/brand/`

> **Scope:** Public-facing brand identity (logo, palette, typography, voice, visual
> direction) for `dealix.com`, investor materials, GitHub organisation, social,
> and the marketing landing site (`landing/`).
>
> **Not in scope:** The operational design system that governs customer-facing
> artefacts (Arabic-first proof packs, evidence ledger UI, executive dashboards)
> lives at `design-systems/dealix/DESIGN.md` and uses a separate Saudi-green
> palette. The two systems coexist intentionally — see §"Two-layer model" below.

---

## Two-layer brand model

| Layer | Purpose | Location | Palette anchor |
|-------|---------|----------|----------------|
| **Brand layer** (this folder) | Marketing, investor, web, GitHub, social, decks | `docs/brand/` + `design-systems/dealix-brand/` | Deep Navy `#0B1220` + Emerald Teal `#00D1A1` |
| **Operational layer** | Saudi customer artefacts, proof packs, dashboards, executive emails | `design-systems/dealix/` | Saudi Green `#0A5C36` + Sand Gold `#C8A86A` |

The brand layer is what an outsider sees first — the website, the pitch deck,
the GitHub org. The operational layer is what a paying Saudi customer sees
inside their workspace. Both ship simultaneously. Neither overrides the other.

---

## Files in this folder

| File | Use it when… |
|------|--------------|
| [`BRAND_GUIDELINES.md`](./BRAND_GUIDELINES.md) | You need to know what the logo, colours, type, or voice should look like. Single source of truth. |
| [`DESIGN_TOKENS.md`](./DESIGN_TOKENS.md) | You're implementing the brand in code (CSS, Figma, Tailwind, slides). Pairs with `design-systems/dealix-brand/tokens.{json,css}`. |
| [`GITHUB_ORG_BRANDING.md`](./GITHUB_ORG_BRANDING.md) | You're setting up a new repo, the org profile, README badges, or social previews. |
| [`LANDING_DIRECTION.md`](./LANDING_DIRECTION.md) | You're touching anything under `landing/` — hero, sections, animations, gradients. |

Implementation tokens live at:

- `design-systems/dealix-brand/tokens.json` — machine-readable (designers/build tools)
- `design-systems/dealix-brand/tokens.css` — CSS custom properties (drop into any page)

---

## Tagline (locked)

**EN:** *Intelligent Deals. Real Growth.*
**AR:** *صفقات ذكية. نموّ حقيقي.*

Use the exact wording. Do not paraphrase ("smart deals", "true growth", etc.).
The English form is the primary lockup pairing under the wordmark; the Arabic
form is for Arabic-locale pages, Arabic decks, and the Arabic README.

---

## Five brand pillars (icon row at the bottom of the press lockup)

1. **Built on Trust** — كل ادّعاء مربوط بدليل في الـ proof ledger.
2. **Driven by Growth** — مقاييس النموّ هي المنتج، مش feature ثانوي.
3. **Closing Deals** — التركيز على conversion، مش vanity metrics.
4. **Focused on Results** — outcome-priced offers (499 SAR sprint → 25K SAR custom AI).
5. **Global Mindset, Local Impact** — بنيت في السعودية، صُمّمت للسوق العالمي.

These are not interchangeable with marketing taglines. They are the
five-pillar value system used in investor decks and the footer icon row.

---

## Change control

The brand layer is a contract. Changes that require founder sign-off:

- Any change to the **logo**, **wordmark**, or **tagline** wording.
- Any change to the five **palette anchors** (Deep Navy, Emerald Teal,
  Soft Silver, Slate, White).
- Any new **primary typeface**.
- Any change to the **five pillars** above.

Small additions (a new tint, a new icon, a new section pattern in
`LANDING_DIRECTION.md`) can be added by PR without founder sign-off, but must
reference the existing tokens and not introduce raw hex values.

---

## See also

- `docs/sales-kit/dealix_brand_guidelines.md` — earlier draft, retained for
  historical voice notes (English copy patterns). Superseded by this folder
  for anything visual.
- `docs/BRAND_PRESS_KIT.md` — founder bios, company descriptions, boilerplate
  in 3 lengths. Still authoritative for **copy**; uses tokens from here for
  **visual treatment**.
- `docs/company/BRAND_VOICE.md` — short voice rules for internal writers.
