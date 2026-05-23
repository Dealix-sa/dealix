# Dealix Brand Operating System

> **Purpose.** A single source of truth for how Dealix looks, sounds, and feels across every internal and external surface.
> Treat this file as policy, not inspiration. Anything that violates it is a defect, not a creative choice.

---

## 1. Brand Essence

| Field | Value |
|---|---|
| Name | **DEALIX** |
| Tagline | **INTELLIGENT DEALS. REAL GROWTH.** |
| Category | Saudi B2B **Revenue Operating System** |
| Promise | Intelligent deal flow, founder-approved growth, trust-gated AI execution |
| Audience | Saudi B2B founders, RevOps, Heads of Sales, Heads of Growth, agencies operating into KSA |
| Voice | Calm authority, evidence-led, never hype, bilingual AR + EN |

### 1.1 Five Brand Pillars
1. **Built on Trust** — approval gates, audit logs, no external action without consent.
2. **Driven by Growth** — every machine ladders up to revenue.
3. **Closing Deals** — bias to cash collected, not pipeline theatrics.
4. **Focused on Results** — measured by founder outcomes, not vanity metrics.
5. **Global Mindset, Local Impact** — Arabic-first execution, world-class engineering.

### 1.2 What we never say
- "Guaranteed revenue / sales / leads"
- "Auto-pilot growth" (we are **semi-autonomous, founder-gated**)
- "Replace your sales team"
- "AI that sells for you with no human in the loop"
- Anything that violates the 11 non-negotiables in `AGENTS.md`.

---

## 2. Surfaces Governed by this System

| Surface | Owner module |
|---|---|
| Founder Console | `apps/web/` |
| Public landing | `landing/`, `frontend/` |
| Sales proposals | `dealix/marketing_factory/`, `templates/` |
| Customer portal | `frontend/src/app/customer-portal` |
| Trust Center | `landing/trust.html`, `apps/web/app/safety` |
| Internal dashboards | `dashboard/`, `apps/web/app/control-plane` |
| Social / LinkedIn | `assets/brand/social`, `docs/marketing/LINKEDIN_OUTREACH_GUIDE.md` |
| Proof artifacts | `docs/proof/`, `docs/case-studies/` |
| Invoices / contracts | `dealix/payments/`, `templates/` |

Every surface must:
1. Use the official tokens (`docs/brand/brand-tokens.json`, `apps/web/lib/brand-tokens.ts`).
2. Use the Dealix wordmark or `D` mark in the approved lockups.
3. Pass the accessibility contrast minimums (§5).
4. Render correctly in **dark navy default** with teal as accent, silver for secondary text.

---

## 3. Logo System

### 3.1 Concept
- **`D` monogram** — anchor; suggests stability and identity.
- **Growth arrow** — emergent line cutting upward through the `D`.
- **Revenue bars** — three ascending bars beneath, encoding deal-flow velocity.
- **Deal / list icon** — micro-mark; represents structured deal records.
- **Teal swoosh** — accent ribbon connecting brand to motion.

### 3.2 Lockups
- **Primary horizontal** — `D-mark` + `DEALIX` wordmark + tagline beneath in silver.
- **Compact horizontal** — `D-mark` + `DEALIX` (no tagline).
- **Stacked vertical** — `D-mark` centered above wordmark; for square crops.
- **Mark only** — `D-mark` alone; favicons, app icons, watermark.
- **Wordmark only** — `DEALIX` alone; document headers, footers, single-line CTAs.

### 3.3 Clearspace
Minimum clearspace = the height of the `D-mark` cap on all sides. Do not place text, photography, or UI chrome inside this zone.

### 3.4 Minimum size
- Digital: 24 px tall (mark), 96 px wide (horizontal lockup).
- Print: 8 mm tall (mark), 32 mm wide (horizontal lockup).

### 3.5 Prohibited
- Recolouring outside the approved palette.
- Adding drop shadows, gradients, outlines, or bevels.
- Rotating, skewing, or stretching.
- Placing on low-contrast photographic backgrounds without a navy plate.
- Reconstructing in third-party AI image tools without brand-guardian approval.

---

## 4. Colour System

Source of truth: `docs/brand/brand-tokens.json`.

| Role | Token | Hex |
|---|---|---|
| Background — primary | `color.bg.primary` | `#0B1220` |
| Background — surface | `color.bg.surface` | `#0F1726` |
| Brand — accent | `color.accent.primary` | `#00D1A1` |
| Brand — accent (hover) | `color.accent.hover` | `#00B388` |
| Text — primary | `color.text.primary` | `#FFFFFF` |
| Text — secondary | `color.text.secondary` | `#B2BBC6` |
| Text — muted | `color.text.muted` | `#7C8895` |
| Border — subtle | `color.border.subtle` | `#1B2536` |
| Status — success | `color.status.success` | `#00D1A1` |
| Status — warning | `color.status.warning` | `#F2B33D` |
| Status — danger | `color.status.danger` | `#FF6B6B` |
| Status — info | `color.status.info` | `#5AC8FA` |

**Default mode is dark.** Light mode is reserved for printed invoices and PDF exports.

---

## 5. Accessibility

| Pair | Target ratio | Use |
|---|---|---|
| `text.primary` on `bg.primary` | ≥ 12 : 1 | body, headings |
| `text.secondary` on `bg.primary` | ≥ 4.5 : 1 | labels, captions |
| `accent.primary` on `bg.primary` | ≥ 4.5 : 1 | links, primary actions |
| `text.primary` on `accent.primary` | ≥ 4.5 : 1 | buttons |
| `text.muted` on `bg.primary` | ≥ 3 : 1 | disabled UI only |

Verifier: `scripts/verify_brand_system.py` checks these pairs against the token file.

WCAG references: 4.5 : 1 for normal text, 3 : 1 for large text and non-text elements.

---

## 6. Typography

| Role | Family | Weight | Notes |
|---|---|---|---|
| Display | Inter Tight, IBM Plex Sans Arabic | 700 | Hero, page heroes |
| Heading | Inter, IBM Plex Sans Arabic | 600 | h1-h3 |
| Body | Inter, IBM Plex Sans Arabic | 400-500 | running text |
| Mono | JetBrains Mono | 400-500 | code, IDs, tokens |

Arabic and English must always share weight and size. Never set Arabic at a smaller optical size than English.

Type scale (rem): 0.75, 0.875, 1, 1.125, 1.25, 1.5, 1.875, 2.25, 3, 3.75.

---

## 7. Iconography

- Stroke 1.5, rounded joins.
- Use accent teal only for state ("active", "approved", "live"), never as default fill.
- Source set: `lucide-react` (already in ecosystem). Custom marks live in `assets/brand/icon/`.

---

## 8. Motion

- Default ease: `cubic-bezier(.2,.8,.2,1)` over 180-220 ms.
- Hover/focus: opacity or background only; never bounce.
- Loading: silver shimmer on `bg.surface`; never spin a logo.

---

## 9. Voice & Tone

| Mode | Use |
|---|---|
| Calm authority | Founder-facing dashboards, proposals |
| Evidence-led | Trust Center, audit, eval reports |
| Operator-tight | CLIs, error messages, console copy |
| Bilingual symmetry | Every founder-facing surface ships AR + EN |

Detailed examples: `docs/brand/DEALIX_BRAND_VOICE.md`.

---

## 10. Governance

- **Owner.** Brand Guardian agent (`docs/ai/BRAND_GUARDIAN_AGENT.md`).
- **Change control.** Brand changes ship as PRs; verifier `scripts/verify_brand_system.py` must pass.
- **Audit.** Every export of the wordmark goes to `assets/brand/`. Do not store brand exports outside this folder.
- **Trust.** No autonomous external use of the brand. Brand Guardian flags violations but never sends or publishes.

---

## 11. Related documents

- `docs/brand/DEALIX_VISUAL_IDENTITY.md`
- `docs/brand/DEALIX_LOGO_USAGE.md`
- `docs/brand/DEALIX_COLOR_SYSTEM.md`
- `docs/brand/DEALIX_TYPOGRAPHY.md`
- `docs/brand/DEALIX_BRAND_VOICE.md`
- `docs/brand/DEALIX_MARKETING_ASSET_GUIDE.md`
- `docs/brand/DEALIX_ACCESSIBILITY_GUIDE.md`
- `docs/brand/brand-tokens.json`
