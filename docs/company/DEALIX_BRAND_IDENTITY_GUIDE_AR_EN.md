# Dealix — Brand Identity Guide (AR + EN)

> **Source of truth for language:** [`BRAND_VOICE.md`](./BRAND_VOICE.md) (doctrine).
> **Source of truth for principles:** [`DEALIX_CONSTITUTION.md`](./DEALIX_CONSTITUTION.md).
>
> This guide adds the *visual* identity (colors, type, spacing) to the existing language doctrine. It does not replace either of the above; if they ever disagree, they win.

## 1. Identity in one line

**AR:** Dealix — مشغّل عمليات الذكاء الاصطناعي المحوكم للمنشآت السعودية.
**EN:** Dealix — the governed AI operations partner for Saudi enterprises.

No "guaranteed sales," no "magic AI," no "set-and-forget." Every claim is backed by SOAEN (Source → Owner → Approval → Evidence → Next Action).

## 2. Color tokens (HSL, dark-first)

| Token | HSL | Use |
|---|---|---|
| `--brand-bg` | `220 30% 6%` | Page background |
| `--brand-surface` | `220 25% 10%` | Cards / panels |
| `--brand-surface-2` | `220 22% 14%` | Elevated surfaces |
| `--brand-border` | `220 20% 22%` | Hairlines |
| `--brand-text` | `210 20% 96%` | Primary text |
| `--brand-text-muted` | `215 15% 70%` | Secondary text |
| `--brand-emerald` | `162 70% 42%` | Primary accent (proof / OK / value) |
| `--brand-emerald-soft` | `162 60% 28%` | Hover / pressed |
| `--brand-gold` | `42 80% 56%` | Trust accent (premium / governance) |
| `--brand-gold-soft` | `42 65% 42%` | Hover / pressed |
| `--brand-amber` | `34 90% 58%` | Caution / pending |
| `--brand-red` | `0 70% 56%` | Block / refusal |

Light mode is allowed; flip background/text and keep the emerald + gold accents.

## 3. Typography

- **Arabic display + body:** Tajawal (300 / 400 / 500 / 700)
- **Latin display + body:** Outfit (400 / 500 / 700)
- **Mono (data, IDs, payment refs):** JetBrains Mono

Scale (Major Third — 1.25):

| Token | Size | Use |
|---|---|---|
| `text-xs` | 12 px | Captions, footnotes |
| `text-sm` | 14 px | Secondary UI |
| `text-base` | 16 px | Body |
| `text-lg` | 20 px | Lead paragraph |
| `text-xl` | 25 px | Section heading |
| `text-2xl` | 31 px | Card heading |
| `text-3xl` | 39 px | Page heading |
| `text-4xl` | 49 px | Hero |

## 4. Spacing — 8 px grid

`4 · 8 · 12 · 16 · 24 · 32 · 48 · 64 · 96 · 128` px. Don't invent half-values; if a layout needs `13px` something else is wrong.

## 5. Logo

- Wordmark: lowercase `dealix` in Outfit 700, optical tracking `-0.02em`.
- The `i` dot becomes a small emerald square — references the SOAEN evidence cell.
- Minimum clear-space = the cap height of the wordmark on every side.
- Minimum size: 96 px wide on screen, 24 mm wide in print.

Assets in this repo:

- `frontend/public/brand/logo.svg` — primary wordmark (dark background)
- `frontend/public/favicon.svg` — square mark
- `frontend/public/og-image.svg` — social share card (1200 × 630)

## 6. Iconography

- Stroke 1.5 px, rounded joins, 24 px grid.
- Lucide icon set is the default. Don't mix outline + filled sets in the same surface.

## 7. Motion

- Default ease: `cubic-bezier(0.4, 0, 0.2, 1)`.
- Default durations: 150 ms (state), 250 ms (entrance), 400 ms (page).
- No looping background animations; doctrine: *calm, not theatrical*.

## 8. Voice — copy patterns

Language rules live in [`BRAND_VOICE.md`](./BRAND_VOICE.md). The shortlist below is for designers/marketers writing surface copy.

### ✅ Use (AR)

- "نرتّب أفضل الفرص"
- "نُنتج Proof Pack"
- "نحوّل العملية إلى نظام"

### ❌ Don't use (AR)

- "نضمن لك المبيعات"
- "أتمتة واتساب باردة"
- "نتائج فورية مضمونة"

### ✅ Use (EN)

- "We surface the best opportunities."
- "We produce a Proof Pack."
- "We turn the process into a governed system."

### ❌ Don't use (EN)

- "Guaranteed pipeline."
- "Cold-outreach automation."
- "Instant results."

## 9. Surface templates

- **Hero:** dark surface, single H1, one supporting paragraph, one primary CTA + one secondary link. No animated particles.
- **Proof card:** number + label (Tajawal 700 / Outfit 700) → evidence link → owner → date. SOAEN order, always.
- **Refusal banner:** when a request violates doctrine (cold WhatsApp, guaranteed claims, fake proof), the system surfaces a `--brand-red` banner that names the violated rule + links to the relevant doctrine line.

## 10. Print

- Page: A4, 24 mm margins (16 mm bottom for footer).
- Footer line: `Dealix · Riyadh, KSA · dealix.me · PDPL-aligned`.
- All bilingual artifacts (one-pager, profile) ship as a single HTML file with `@media print` rules; the founder opens in any browser → Ctrl+P → "Save as PDF."

Last updated: 2026-05-22.
