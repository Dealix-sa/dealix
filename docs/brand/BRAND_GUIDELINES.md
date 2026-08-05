# Dealix — Brand Guidelines

> **Version:** 1.0 · **Locked:** 2026-05-22 · **Owner:** Founder (Sami)
> **Companion docs:** [`DESIGN_TOKENS.md`](./DESIGN_TOKENS.md) ·
> [`GITHUB_ORG_BRANDING.md`](./GITHUB_ORG_BRANDING.md) ·
> [`LANDING_DIRECTION.md`](./LANDING_DIRECTION.md)

---

## 1. Brand essence

| | |
|---|---|
| **Name** | Dealix (always capitalised in running text as **Dealix**; never DEALIX in body copy — only inside the logo lockup) |
| **Tagline (EN)** | Intelligent Deals. Real Growth. |
| **Tagline (AR)** | صفقات ذكية. نموّ حقيقي. |
| **One-liner (EN)** | The AI Operating Team that turns Saudi B2B pipelines into evidence-backed revenue. |
| **One-liner (AR)** | فريق التشغيل بالذكاء الاصطناعي اللي يحوّل خطّ مبيعات الشركات السعودية إلى إيرادات مدعومة بالدليل. |
| **Personality** | Precise · Calm · Premium · Saudi-built · Globally legible |
| **Anti-personality** | Hypey · Generic-startup-purple · "Disruptor" · Cute · Emoji-driven |

---

## 2. Logo system

The Dealix mark is a stylised letter **D** wrapping a **growth chart** with an
upward arrow. The D is the *deal*; the chart is *real growth*. The two are
inseparable — never extract just one half.

### 2.1 Approved lockups (the only four)

1. **Primary logo** — icon + DEALIX wordmark + tagline, stacked vertically.
   Use on: covers, hero sections, full-page artwork, the website's first fold.
2. **Horizontal wordmark** — icon to the left of DEALIX wordmark, divider, then tagline below.
   Use on: email headers, navigation bars, slide masters, press kit lockups.
3. **Icon only** — just the D-with-chart mark.
   Use on: favicons, app icons, social profile pictures, watermarks ≥ 32 px.
4. **Monochrome** — the horizontal lockup in single-colour silver/white only.
   Use on: dark partner contexts, print where colour is constrained,
   single-colour embossing/etching, fax-grade PDFs.

> Anything else — vertical wordmark only, slogan-only, icon-with-modified-arrow,
> initials "DX", etc. — is **not** an approved lockup and must not be used.

### 2.2 Clear space

The minimum clear space around any lockup is **the height of the letter "D"**
in the wordmark (call this `1×`). Nothing — text, photo edge, button, card border — may enter the `1×` halo on any side.

For the **icon only**, clear space = **25% of the icon's width** on every side.

### 2.3 Minimum size

| Lockup | Print min | Screen min |
|---|---|---|
| Primary (vertical) | 32 mm wide | 160 px wide |
| Horizontal wordmark | 40 mm wide | 200 px wide |
| Icon only | 8 mm | 24 px (favicons may use a tighter 16 px ICO variant) |
| Monochrome | same as base lockup | same as base lockup |

Below these sizes, switch to the next smaller lockup (e.g. horizontal → icon).

### 2.4 Logo do / don't

**Do**
- Place the primary logo on `Deep Navy #0B1220` or `Slate #0F1726` — these are the canonical backgrounds.
- On photography, place the logo on the darkest 25% of the image, and only after a contrast check.
- Export at 2× / 3× density for retina screens. Always use SVG where the renderer supports it.

**Don't**
- Don't recolour the gradient. The chart-arrow is the *only* element that carries Emerald Teal; the D outline stays Soft Silver / White.
- Don't add drop shadows, outer glows, bevels, or 3D extrusion. The logo is flat-with-gradient by design.
- Don't place the full-colour logo on white. White backgrounds use the **navy version** of the wordmark (see §3.3 safe combinations) or the monochrome lockup.
- Don't compress the lockup horizontally or stretch vertically. Scale uniformly.
- Don't crop the arrow or chart bars to "fit" a tight space — switch lockups instead.
- Don't combine the logo with another brand mark closer than the clear-space rule.

### 2.5 File deliverables (canonical exports)

All master files live at `landing/assets/logos/`:

```
landing/assets/logos/
├── dealix-primary.svg              # vertical primary, on-dark
├── dealix-primary-on-light.svg     # vertical primary, on-light (navy wordmark)
├── dealix-horizontal.svg           # horizontal lockup, on-dark
├── dealix-horizontal-on-light.svg  # horizontal lockup, on-light
├── dealix-icon.svg                 # icon only
├── dealix-monochrome.svg           # mono silver/white horizontal
├── dealix-monochrome-dark.svg      # mono navy/slate horizontal (light bg)
├── favicon.ico                     # 16/32/48 multi-size
├── favicon-512.png                 # PWA / OG fallback
└── og-image.png                    # 1200×630 social preview, primary on navy
```

Source designer file (Figma / Illustrator) is managed off-repo. PRs that touch
these files require founder review.

---

## 3. Colour palette

### 3.1 Brand anchors (locked — do not edit without founder sign-off)

| Token | Hex | Role | Where it appears |
|---|---|---|---|
| `--deep-navy` | `#0B1220` | Primary dark surface, hero backgrounds | Website body, deck masters, app shell |
| `--emerald-teal` | `#00D1A1` | Brand accent — only on dark | Chart arrow, primary CTA on navy, link underlines, glow accents |
| `--soft-silver` | `#B2BBC6` | Muted text on dark, dividers | Section captions, table secondary text |
| `--slate` | `#0F1726` | Alt dark surface | Cards inside hero, panel separators |
| `--white` | `#FFFFFF` | Text on dark, light surfaces | Headings on dark, light-mode backgrounds |

### 3.2 Functional extensions (added for product UI, AA-compliant)

The five anchors above cover brand surfaces but **cannot** carry the full
weight of a product UI alone — there are no state colours, no light-mode
accent, no muted text for light backgrounds. The additions below fill those
gaps without diluting the brand:

| Token | Hex | Role |
|---|---|---|
| `--teal-ink` | `#007A5C` | The teal accent for use on **light backgrounds**. Passes WCAG AA on white (5.3:1). Use anywhere `--emerald-teal` would fail contrast. |
| `--silver-2` | `#6B7480` | Muted body text on light backgrounds. Passes AA on white (4.6:1). |
| `--navy-50` | `#E8EBF1` | Light-mode background tint (1.5% navy). Use for table-row stripes and card alt-fills in light mode. |
| `--success` | `#10B981` | Positive state (passed test, deal closed, evidence verified). |
| `--warn` | `#F59E0B` | Caution state (pending review, approval required, expiring soon). |
| `--danger` | `#EF4444` | Negative state (blocked, hard-gate violation, failed evidence check). |
| `--info` | `#60A5FA` | Informational state (neutral notice, system message). |

### 3.3 Safe colour combinations (contrast matrix)

Body text (≥ 14 px) needs ≥ 4.5:1 (WCAG AA). Large text / icons (≥ 18 px or
14 px bold) need ≥ 3.0:1.

| Foreground | Background | Ratio | Verdict |
|---|---|---|---|
| `--white` `#FFFFFF` | `--deep-navy` `#0B1220` | ~18.6:1 | ✅ AAA |
| `--emerald-teal` `#00D1A1` | `--deep-navy` `#0B1220` | ~9.6:1 | ✅ AAA |
| `--soft-silver` `#B2BBC6` | `--deep-navy` `#0B1220` | ~9.7:1 | ✅ AAA |
| `--white` `#FFFFFF` | `--slate` `#0F1726` | ~17.3:1 | ✅ AAA |
| `--emerald-teal` `#00D1A1` | `--white` `#FFFFFF` | ~2.0:1 | ❌ FAIL — use `--teal-ink` |
| `--teal-ink` `#007A5C` | `--white` `#FFFFFF` | ~5.3:1 | ✅ AA |
| `--deep-navy` `#0B1220` | `--white` `#FFFFFF` | ~18.6:1 | ✅ AAA |
| `--silver-2` `#6B7480` | `--white` `#FFFFFF` | ~4.6:1 | ✅ AA |
| `--soft-silver` `#B2BBC6` | `--white` `#FFFFFF` | ~1.9:1 | ❌ FAIL — never use silver on white |

**Implication:** Emerald Teal is an **on-dark only** colour. If a designer
needs a teal accent on a light background (light-mode docs, white-background
slides, printed brochures), they switch to `--teal-ink`. This is the single
most important contrast rule in the brand.

### 3.4 Gradients

The brand uses **one** sanctioned gradient:

```
linear-gradient(135deg, #00D1A1 0%, #00A37C 100%)
```

It appears on the logo chart-arrow and may be reused for:

- Primary CTA buttons on dark backgrounds (subtle, ≤ 5% lighter at top).
- Hero accent strokes (1–2 px hairlines under section headings).
- Investor-deck cover artwork backgrounds at very low opacity (≤ 8%).

Never invent rainbow gradients, purple-to-pink, or animated colour shifts.

---

## 4. Typography

The brand uses **three families** (display + UI + Arabic) plus **one
monospace** for evidence IDs and code. This is a deliberate reduction from
the four candidates originally floated (Sora, Space Grotesk, Manrope, Plus
Jakarta) — too many similar geometric sans-serifs creates visual noise.

| Role | Family | Weights used | Use it for |
|---|---|---|---|
| Display | **Space Grotesk** | 600, 700 | Headlines, hero text, deck section titles |
| UI / body Latin | **Inter** | 400, 500, 600 | All body copy, UI labels, captions, tables |
| Arabic | **IBM Plex Sans Arabic** | 400, 500, 600 | All Arabic copy in any role |
| Monospace | **JetBrains Mono** | 400, 500 | Evidence IDs (`EVT-…`), code blocks, hashes, version stamps |

**Why these:**
- Space Grotesk has a slightly engineered, technical character — fits "AI
  Operating Team" without falling into generic SaaS sans.
- Inter is the most readable UI font available in 2025, with extensive
  weights and ligatures. It's the workhorse.
- IBM Plex Sans Arabic is the strongest Arabic companion to Inter (both are
  open, both have a wide weight range, both pair cleanly). Already in use in
  the operational design system, so reusing it keeps Arabic typography
  consistent across both brand layers.
- JetBrains Mono is the monospace standard in the operational layer.

### 4.1 Type scale (display: Space Grotesk; body: Inter)

| Token | Size | Line-height | Weight | Use |
|---|---|---|---|---|
| `display-xl` | 64 px | 1.05 | 700 | Investor cover, single hero word |
| `display-l` | 48 px | 1.10 | 700 | Hero headline (web), deck section opener |
| `display-m` | 36 px | 1.15 | 600 | Sub-hero, page H1 |
| `heading-l` | 28 px | 1.25 | 600 | Section H2 (Space Grotesk) |
| `heading-m` | 22 px | 1.30 | 600 | Subsection H3 (Inter) |
| `heading-s` | 18 px | 1.35 | 600 | Card title (Inter) |
| `body-l` | 18 px | 1.55 | 400 | Lede / opening paragraph |
| `body-m` | 16 px | 1.55 | 400 | Standard body (Inter / IBM Plex Sans Arabic) |
| `body-s` | 14 px | 1.50 | 400 | Caption / helper |
| `mono-m` | 14 px | 1.50 | 500 | Evidence IDs, code, hashes (JetBrains Mono) |

Arabic always renders at **+10% line-height** vs the Latin equivalent (e.g.
body-m Arabic = 1.70) for diacritic clarity. The CSS variable system in
`tokens.css` handles this automatically via the `[lang="ar"]` selector.

### 4.2 Wordmark

The DEALIX wordmark in the logo is a **custom geometric uppercase** with a
distinguishing triangular cut inside the "A" (visible in the primary logo).
Do not attempt to recreate this in CSS — always use the SVG lockup. Body
copy never spells the brand as "DEALIX"; it's "Dealix".

---

## 5. Iconography

Use **Lucide** (`lucide.dev`) as the system icon library — it's open, has
~1,400 icons, and matches the geometric weight of Space Grotesk.

### 5.1 Brand pillar icons (the five at the bottom of the lockup)

These are *brand* icons (custom-styled), not system icons. They are part of
the press lockup and the website footer. Treat them as logo elements:

| Pillar | Glyph cue | Colour |
|---|---|---|
| Built on Trust | Shield | `--emerald-teal` outline |
| Driven by Growth | Ascending bar chart | `--emerald-teal` outline |
| Closing Deals | Handshake | `--emerald-teal` outline |
| Focused on Results | Crosshair / target | `--emerald-teal` outline |
| Global Mindset, Local Impact | Globe with meridians | `--emerald-teal` outline |

Source: `landing/assets/logos/pillars/*.svg` (one file per pillar, on-dark
variant only — on-light uses `--teal-ink`).

### 5.2 System icons (everything else)

- Stroke width: **1.5 px** at 24×24 base size.
- Corner radius: rounded (Lucide default).
- Colour: inherit `currentColor`. Never hard-code hex inside an icon.
- Size scale: 16 / 20 / 24 / 32 / 48 px.

---

## 6. Voice & tone

Dealix talks like a **competent Saudi operator briefing an executive** —
not like a SaaS marketer.

### 6.1 Voice rules (apply to every customer-facing string)

1. **Specific over abstract.** "Closed 18 deals in 7 days" not "boost your sales".
2. **Evidence-first.** Every claim has a proof link, an SLA, or a measurable
   number. If it doesn't, rewrite it until it does or cut it.
3. **No hype verbs.** Banned: *revolutionise · disrupt · unleash · supercharge ·
   crush · 10x · skyrocket · game-changer · cutting-edge · best-in-class*.
4. **Approval is a feature, not an apology.** Frame the founder-approval gate
   as a benefit ("nothing ships without your green light"), not a limitation.
5. **Bilingual parity.** Every external string ships in both Arabic and
   English with the same meaning — never a hyped English version paired with
   a sober Arabic translation, or vice versa.
6. **Saudi context, global legibility.** Use Saudi market specifics when
   they're real ("PDPL-compliant", "SAR 499"); don't perform localness.
   International readers should still understand without a glossary.
7. **Numbers in ASCII for tables, Arabic-Indic in prose.** Tables and KPIs
   stay parseable; prose can use ٠١٢٣٤٥٦٧٨٩ where natural in Arabic.

### 6.2 Headline patterns that work

- **The verb-first promise**
  EN: *Close deals you can prove.*
  AR: *سكّر صفقات تقدر تثبتها.*
- **The Saudi-specific anchor**
  EN: *Built in Riyadh. PDPL-compliant by design.*
  AR: *مبنيّ من الرياض. متوافق مع PDPL من اللحظة الأولى.*
- **The contrast frame**
  EN: *Not another CRM. An AI Operating Team.*
  AR: *مش CRM ثاني. فريق تشغيل بالذكاء الاصطناعي.*

### 6.3 Banned strings (verbatim, from the forbidden-claims test)

These mirror the operational design system's forbidden list:

`نضمن` · `guaranteed` · `blast` · `scrape` · `cold WhatsApp` ·
`revenue guaranteed` · `ranking guaranteed` · `fully automated external send`

Banned in **positive** context. Allowed inside an explicit negation
("Dealix never does *fully automated external send*"), with the negation
allowlisted in `tests/test_landing_forbidden_claims.py`.

---

## 7. Bilingual & RTL

- Arabic is **not** a translation of English — it's a parallel voice. Some
  English phrases are dropped in Arabic; some Arabic phrases ("نموّ حقيقي")
  carry weight that the English doesn't.
- Arabic blocks render `dir="rtl" lang="ar"`. English sub-blocks switch
  locally with `<section lang="en" dir="ltr">…</section>`.
- Status chips, evidence badges, and table arrows mirror under RTL. Icons
  that have semantic direction (forward/back arrows) use logical CSS
  properties (`margin-inline-start`, not `margin-left`).
- The Arabic tagline *صفقات ذكية. نموّ حقيقي.* uses a full stop, not an
  Arabic comma — it's a pair of short statements, not a clause.

---

## 8. Usage examples (quick reference)

| Surface | Background | Logo lockup | Type combo |
|---|---|---|---|
| Website hero (`landing/index.html`) | `--deep-navy` | Primary (vertical) | `display-l` Space Grotesk |
| Email signature | white | Horizontal on-light (navy wordmark) | `body-m` Inter |
| Investor deck cover | `--deep-navy` | Primary (vertical) | `display-xl` Space Grotesk |
| Investor deck body slides | `--slate` | Horizontal top-left, 32 px | `heading-l` + `body-m` |
| Twitter/X profile | `--deep-navy` | Icon only (400×400) | n/a |
| LinkedIn company banner | `--deep-navy` + gradient hairline | Horizontal centred | tagline in `--emerald-teal`, `heading-m` |
| GitHub repo README | white | Horizontal on-light | `body-m` Inter |
| App favicon | n/a | Icon only (16/32/48 ICO) | n/a |
| Press release PDF | white | Monochrome-dark (navy) | Inter only |

---

## 9. Decision log

| Date | Decision | Rationale |
|---|---|---|
| 2026-05-22 | Adopted Deep Navy + Emerald Teal as brand anchors | Replaces uncommitted earlier teal/purple exploration; matches the locked logo lockup the founder approved. |
| 2026-05-22 | Reduced fonts from 4 candidates → 3 + mono | Sora, Space Grotesk, Manrope, Plus Jakarta are too similar — visual noise without distinction. Space Grotesk wins on geometric character. |
| 2026-05-22 | Added `--teal-ink #007A5C` for light-mode use | Emerald Teal fails WCAG AA on white (~2:1). Without an ink variant, designers would either silently break contrast or invent their own off-brand teal. |
| 2026-05-22 | Added state tokens (success/warn/danger/info) | Brand anchors don't carry product UI states. Added in a single coherent family, not pulled from random sources. |
| 2026-05-22 | Kept IBM Plex Sans Arabic as the Arabic family | Already used by the operational design system. Single Arabic typeface across both layers avoids customer confusion when they see both surfaces. |
| 2026-05-22 | Logo full-colour version is on-dark only | The gradient chart-arrow loses contrast on white backgrounds. On-light surfaces use the monochrome navy lockup. |

---

## 10. Where to ask questions

- **"Can I use this colour here?"** → Check the contrast matrix in §3.3 first. If it's not in the matrix, default to no.
- **"Can I add a new font?"** → No. Reuse the existing four.
- **"Can I tweak the logo for [event/season/campaign]?"** → No. Use one of the four approved lockups.
- **"Can I use the icon by itself on a dark photo?"** → Yes, if the photo's darkest region under the icon is ≥ `--deep-navy` in luminance and the clear space rule holds.
- **"Something not covered here?"** → Open a PR in this folder with the proposed addition. Founder reviews brand-layer PRs.
