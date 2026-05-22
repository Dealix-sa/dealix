# Landing Visual Direction — Dealix

> How the Dealix brand renders in `landing/` (the marketing website).
> Companion to [`BRAND_GUIDELINES.md`](./BRAND_GUIDELINES.md) and
> [`DESIGN_TOKENS.md`](./DESIGN_TOKENS.md).
>
> **Scope:** Visual direction only — colours, layout patterns, animation
> rules, section archetypes. **Not** in scope: copy (lives in
> `docs/sales-kit/`), or technical implementation choices like Astro vs.
> raw HTML (the existing pages are vanilla HTML + `styles.css`).

---

## 1. The feel in one sentence

A **calm, dark, instrument-panel** aesthetic — like a financial trading
terminal that learned to write Arabic. Not a SaaS marketing page with
purple gradients and oversized illustrations.

If you find yourself reaching for **purple, pink, glassmorphism, animated
3D blobs, isometric illustrations, or hand-drawn squiggles** — stop. None
of those belong in Dealix.

---

## 2. Page anatomy (standard sections, in order)

Most landing pages under `landing/*.html` should follow this archetype:

1. **Nav** — slim, sticky on scroll, max-height 64 px.
2. **Hero** — single dark surface, one headline, one sub-line, one CTA.
3. **Proof strip** — a single horizontal row of evidence (logos, KPI, status badges).
4. **Three pillars** — what the product/page does, three columns desktop, stacked mobile.
5. **The deep section** — the one piece of detail this page exists to convey (a comparison table, a workflow diagram, a calculator).
6. **Social proof** — quote(s) or case-study card(s). Always evidence-linked.
7. **Pricing or CTA repeat** — depending on page type.
8. **Footer** — five-pillar icon row, links, legal, language toggle.

A page may **skip** sections, but it must not **reorder** them or invent
new positions for the existing ones.

---

## 3. Section-by-section visual rules

### 3.1 Nav

- Background: `--bg` with `backdrop-filter: blur(12px)` and 86% alpha when sticky.
- Logo: horizontal lockup, 32 px tall, top-left.
- Links: Inter 500, 14 px, `--text-muted`. Hover → `--text`.
- Primary CTA on the far right: filled with `--accent` background and `--on-accent` text. Radius `--radius-md`.
- Language toggle (AR / EN) lives between the last nav link and the CTA — never inside a hamburger menu, even on mobile.

### 3.2 Hero

- Background: `--bg` (Deep Navy).
- Optional accent: a single 1-px Emerald-Teal hairline at the bottom of the hero, full-width, with a subtle `--shadow-glow-teal` to the line.
- Headline: `--type-display-l` Space Grotesk, `--text`.
- Sub-line: `--type-body-l` Inter, `--text-muted`, max 56 ch wide.
- CTA: primary button (filled `--accent`) + secondary outline button. Never three buttons. Never a "Learn More" arrow link.
- Optional product mock: lives **right** of the text on desktop (LTR), **left** on RTL. Float on `--bg-alt` card with `--radius-xl`.

**Forbidden in hero:**
- Animated word cyclers ("AI / Sales / Growth / Future").
- Large hero illustrations with characters or people.
- Auto-playing video.
- Marquee scrolls of "trusted by" logos (those belong in §3.3).

### 3.3 Proof strip

A single horizontal row, 64–96 px tall, `--bg-alt` background.

Two patterns are allowed:

- **Logos** — grayscale partner/customer logos, evenly spaced. Max 6 items.
  Always include a "+12 more" trailing label when you have more than 6 — do not invent a marquee.
- **KPIs** — three to five KPI tiles (number + label), each evidence-linked.
  Format: `1,247` (Space Grotesk 600, `--accent`) above `pilot deals closed` (Inter 400, `--text-muted`).

Never both patterns on the same page.

### 3.4 Three pillars

- Three cards, equal width, gap `--space-6`.
- Card background: `--bg-alt`, padding `--space-5`, radius `--radius-lg`.
- Icon at top (24 px, `--accent`), then heading (`--type-heading-m`), then 1–3 lines of body (`--type-body-m`, `--text-muted`).
- On mobile (`< var(--bp-md)`): stack vertically with `--space-4` gap.

### 3.5 Deep section

This is where the page **earns its existence**. Typical patterns:

- **Comparison table** — 4-column max, header `--bg-alt`, numeric columns right-aligned (LTR) / start-aligned (RTL). Forbidden cells use the `--danger` colour with an X icon, not red text.
- **Workflow diagram** — left-to-right (LTR) or right-to-left (RTL) flow, max 5 steps. Steps as numbered cards connected by hairlines. Animate on scroll only if `prefers-reduced-motion: no-preference`.
- **Calculator** — input form on one side, output panel on the other. Output panel always shows the proof source ("Based on 247 Saudi pilot deals, May 2024 → May 2026").

### 3.6 Social proof

- Quote: Inter italic 400, 22 px, `--text`. Open and close with proper typographic quotes (`"` `"` in EN, `«` `»` in AR).
- Attribution: Inter 500, 14 px, `--text-muted`. Format: `— First Name, Role at Company`.
- Evidence chip below the attribution: `--mono`, format `PROOF-<id>`, links to the proof ledger.
- Never use stock-photo headshots. Real photo or no photo.

### 3.7 Pricing / CTA repeat

- For a pricing page: 3-tier card layout, middle tier raised with `--shadow-md` and a `--accent`-coloured "Most popular" pill at the top.
- For a non-pricing page: a single CTA card on `--bg-alt`, padding `--space-7`, radius `--radius-xl`. One headline, one sub-line, one button.

### 3.8 Footer

- Background: same as page (`--bg` on dark pages, `--bg-alt` on light interludes).
- Top of footer: the **five-pillar icon row** from the brand lockup. Each icon `--accent`, 32 px, with its label (Built on Trust / Driven by Growth / etc.) in `--type-body-s`.
- Below: four columns of links (Product / Company / Resources / Legal), then a bottom row with copyright, language toggle, and a 16 px logo on the right.

---

## 4. Animation rules

Less is more. Dealix animates **on intent**, not on idle.

| Trigger | Effect | Duration | Easing |
|---|---|---|---|
| Hover on CTA | Background lightens 4%, glow appears (`--shadow-glow-teal`) | `--duration-fast` | `--easing-standard` |
| Hover on card | Lift 2 px, `--shadow-md` | `--duration-fast` | `--easing-standard` |
| Section enters viewport | Opacity 0 → 1, translateY 12 px → 0 | `--duration-slow` | `--easing-entrance` |
| Tab switch | Cross-fade old → new | `--duration-base` | `--easing-standard` |
| Modal open | Backdrop fades in, modal scales 0.97 → 1 | `--duration-slow` | `--easing-entrance` |

**Forbidden:**
- Continuous "breathing" animations on idle elements.
- Parallax on scroll.
- Cursor-following effects.
- "Spotlight" mouse-tracking gradients.
- Bouncy springs (`overshoot > 0`).
- Auto-rotating carousels (manual user control only).

All animation respects `prefers-reduced-motion: reduce` — when on, every
animation duration drops to 0 ms (handled in `tokens.css`).

---

## 5. Imagery

### 5.1 What's allowed

- **Product screenshots** — at 2× density, with a 1 px `--divider` border and `--radius-lg` corners. Real UI, not Figma mockups.
- **Diagrams** — geometric, single-stroke (1.5 px), `--accent` on `--bg`. Match the icon weight.
- **Founder portrait** — a single real photo, monochrome treatment (sepia-toned to brand palette), used only on `landing/founder.html` and investor materials.

### 5.2 What's banned

- Stock photography of people in suits shaking hands.
- 3D-rendered abstract objects (cubes, spheres, fluid shapes).
- Illustrations of generic "AI brains", "data nodes", or "networks".
- Emoji as decoration in any UI surface.
- Gradient meshes / "aurora" backgrounds — the only sanctioned gradient is the teal 135° one in `tokens.css`.

---

## 6. Bilingual / RTL behaviour on the landing site

- Every page must render correctly in both `lang="en" dir="ltr"` and `lang="ar" dir="rtl"`.
- The language toggle sets `<html lang>` and `<html dir>` — never just one or the other.
- Use **logical CSS** (`margin-inline-start`, `padding-inline-end`, `text-align: start/end`) everywhere. Avoid `left` / `right` properties except where direction-explicit is required (e.g. a flag icon).
- Numerals: ASCII digits in pricing tables (parseable for screen readers and copy-paste), Arabic-Indic in prose.
- Test every page by toggling `dir` mid-session — interactive elements (modals, dropdowns, drawers) must mirror correctly without a full reload.

---

## 7. Existing `landing/` files — migration notes

The current `landing/styles.css` predates this brand layer and uses raw
hex values (likely from the Saudi-green operational palette mixed with
ad-hoc additions). When migrating an existing page to the new brand:

1. Add `<link rel="stylesheet" href="/design-systems/dealix-brand/tokens.css">` **before** `styles.css`.
2. Search for hard-coded colours in the page's inline styles and replace with `var(--…)` tokens.
3. Replace any custom font declarations with the four `--font-*` variables.
4. Run the page through Lighthouse — contrast scores must remain ≥ 95 after migration. If they drop, you're missing a `--teal-ink` swap.
5. Re-test with the language toggle in both directions before merging.

Don't migrate all pages in one PR. Migrate **one page at a time**, starting
with the highest-traffic pages (`index.html`, `pricing.html`,
`diagnostic.html`, `services.html`).

---

## 8. Page checklist (use this for any landing PR)

Before merging any new landing page or significant redesign:

- [ ] Tokens stylesheet loaded **before** any page-specific CSS.
- [ ] No raw hex values anywhere in the file (`grep -E "#[0-9A-Fa-f]{3,8}" path/to/page.html` returns nothing).
- [ ] Hero uses one headline + one sub-line + ≤ 2 CTAs.
- [ ] At least one **evidence-linked** number or quote on the page.
- [ ] Both `dir="ltr"` and `dir="rtl"` render correctly.
- [ ] No banned imagery / animation patterns (§4, §5.2).
- [ ] Page passes the forbidden-claims test (`tests/test_landing_forbidden_claims.py`).
- [ ] Lighthouse mobile score ≥ 90 for Performance, Accessibility, Best Practices.
- [ ] Five-pillar icon row present in the footer.
- [ ] Logo is one of the four approved lockups; no recoloured / cropped variants.
