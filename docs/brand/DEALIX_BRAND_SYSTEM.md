# Dealix Brand System

> **Tagline:** Intelligent Deals. Real Growth.
> **Mission:** Build a brand-led, founder-controlled, trust-gated, AI-native Saudi B2B Revenue Operating Company.

This document is the **master entry point** for the Dealix brand. Every other brand document, design token file, component, and marketing surface must derive from this one.

---

## 1. What is the Dealix brand?

Dealix is a **revenue operating system** for Saudi B2B companies. The brand expresses:

- **Trust** — every automation is human-approved and auditable; no uncontrolled outbound.
- **Growth** — measurable revenue lift through intelligent deal flow.
- **Precision** — AI that is trust-gated, evaluated, and reviewable.
- **Founder control** — the founder always sees, approves, and can kill any flow.
- **Local impact, global mindset** — Saudi-first, KSA-tax-aware, Arabic-and-English fluent.

The brand is **dark, enterprise, premium**. Not playful. Not loud. Not silicon-valley pastel. It is a serious operating system worn like a tailored thobe — precise, navy, with a single sharp accent of teal energy.

## 2. Brand pillars (canonical)

| Pillar                          | What it means in product/marketing                                          |
|---------------------------------|------------------------------------------------------------------------------|
| Built on Trust                  | Approval queues, audit logs, kill switches, no "fully autonomous" promises   |
| Driven by Growth                | Concrete revenue KPIs, before/after metrics, sector benchmarks              |
| Closing Deals                   | Sample → proposal → payment artefacts, not "AI productivity" vapor          |
| Focused on Results              | Every machine has KPI, input/output, owner, recovery path                   |
| Global Mindset, Local Impact    | Bilingual, KSA-tax-aware, sector reports in AR + EN                         |

These pillars are the **only allowed top-level marketing themes** for content, sales decks, and landing copy. Do not invent new pillars without founder approval.

## 3. Identity components

The full visual identity is documented in:

- [`DEALIX_VISUAL_IDENTITY.md`](./DEALIX_VISUAL_IDENTITY.md) — logo construction & application
- [`DEALIX_LOGO_USAGE.md`](./DEALIX_LOGO_USAGE.md) — do/don't rules, clear space, sizing
- [`DEALIX_COLOR_SYSTEM.md`](./DEALIX_COLOR_SYSTEM.md) — palette + semantic tokens
- [`DEALIX_TYPOGRAPHY.md`](./DEALIX_TYPOGRAPHY.md) — type system (AR + EN)
- [`DEALIX_BRAND_VOICE.md`](./DEALIX_BRAND_VOICE.md) — tone, words to use, words to avoid
- [`DEALIX_MARKETING_ASSET_GUIDE.md`](./DEALIX_MARKETING_ASSET_GUIDE.md) — proposal/deck/social templates
- [`DEALIX_ACCESSIBILITY_GUIDE.md`](./DEALIX_ACCESSIBILITY_GUIDE.md) — WCAG-aligned rules

## 4. Where the brand lives

| Surface                     | Source of truth                                            |
|----------------------------|------------------------------------------------------------|
| Logo / icon files           | `assets/brand/` (source) + `apps/web/public/brand/` (web)  |
| Design tokens (TS)          | `apps/web/lib/brand-tokens.ts`                              |
| Design tokens (JSON)        | `docs/brand/brand-tokens.json`                              |
| Web styles                  | `apps/web/styles/brand.css`                                 |
| Founder Console shell       | `apps/web/components/founder-shell.tsx`                     |
| Reusable brand components   | `apps/web/components/brand/*`                               |
| Public landing CSS          | `landing/dealix-brand.css`                                  |
| Proposal / deck templates   | `docs/brand/DEALIX_MARKETING_ASSET_GUIDE.md`                |

## 5. Non-negotiable rules

These are hard rules. The brand verifier (`scripts/verify_brand_system.py`) enforces them and CI will fail if any are violated.

1. **No "guaranteed revenue / guaranteed sales / guaranteed results" claims.** Anywhere. Ever.
2. **No "fully autonomous selling" or "AI that sells for you" copy.** We say *AI-assisted*, *trust-gated*, *founder-approved*, *revenue intelligence*.
3. **All colour applications must meet WCAG contrast** — body text ≥ 4.5:1, large text (≥ 18.66px bold or 24px regular) ≥ 3:1, UI components & graphical objects ≥ 3:1.
4. **The logo never sits on a low-contrast background.** Always use it on Deep Navy, Slate, White, or a monochrome fallback.
5. **The tagline always appears in the canonical form** — `Intelligent Deals. Real Growth.` — with that exact capitalisation and punctuation.
6. **No emojis in brand surfaces.** Internal Slack is fine; brand-touched surfaces (proposals, decks, landing, console, emails) stay clean.
7. **Arabic and English are first-class.** Never ship an English-only proposal or deck. Provide AR + EN.

## 6. Approval

The brand system is owned by the founder. Material changes (palette, logo, tagline, pillars) require explicit founder approval. The brand verifier protects the doctrine; the founder protects the verifier.
