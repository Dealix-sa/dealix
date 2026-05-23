# DEALIX Marketing Asset Guide

> Wordmark: **DEALIX**
> Tagline: **INTELLIGENT DEALS. REAL GROWTH.**

This guide describes how to produce, name, store, and export Dealix
marketing assets so they stay on-brand from first draft to public
publication. It complements `DEALIX_BRAND_SYSTEM.md`,
`DEALIX_VISUAL_IDENTITY.md`, and `DEALIX_BRAND_VOICE.md`.

The goal is simple: a Dealix asset should look like Dealix even when a
prospect screenshots it, crops it, or pastes it into a foreign deck.

---

## 1. Asset taxonomy

| Asset type | Purpose | Typical surface |
| --- | --- | --- |
| Hero image | Landing page banner | Marketing site |
| OG card | Social share preview | LinkedIn, X, OG meta |
| Product screenshot | Show the UI | Marketing site, deck, proposal |
| Diagram | Explain a concept | Deck, report, blog |
| Quote card | Customer or operator quote | Social, deck (with approval) |
| Stat card | Single metric with denominator | Social, deck |
| Sector brief | Short report PDF | Sales follow-up |
| Long-form report | Full sector report | Sales follow-up, content |
| Webinar slide deck | Live event deck | Webinar, partner event |
| Event backdrop | Booth or stage backdrop | Trade event |
| Email banner | Header image for email | Marketing email |

Each asset type has a master template. Designers do not start from a blank
canvas — they open the master and edit.

---

## 2. Naming convention

Files follow a single naming pattern:

```
dealix_{asset_type}_{topic}_{locale}_{version}.{ext}
```

Examples:
- `dealix_og_homepage_en_v3.png`
- `dealix_quote_almutawa_ar_v1.png`
- `dealix_diagram_revenue_flow_en_v2.svg`
- `dealix_report_logistics_saudi_q2_2026_ar_v1.pdf`

Rules:
- Lowercase, snake_case.
- Locale is `en`, `ar`, or `bil` (bilingual).
- Version starts at `v1` and increments on substantive change.
- No spaces, no parentheses, no emoji.

---

## 3. Storage layout

```
assets/brand/
  source/        # canonical SVG, AI, Figma exports
  marketing/
    og/
    hero/
    diagrams/
    quotes/
    stats/
    reports/
    decks/
    email/
```

Working files live in design tools (Figma). Exported assets land in this
tree. Anything outside the tree is not authoritative.

---

## 4. Export specifications

| Asset | Format | Dimensions | DPI | Notes |
| --- | --- | --- | --- | --- |
| OG card | PNG | 1200×630 | 72 | sRGB |
| LinkedIn share | PNG | 1200×627 | 72 | |
| LinkedIn carousel slide | PNG | 1080×1350 | 72 | |
| X share card | PNG | 1200×675 | 72 | |
| Email banner | PNG | 600×200 | 72 | Compress < 100 KB |
| Hero image (desktop) | WebP + PNG fallback | 2560×1440 | 72 | |
| Hero image (mobile) | WebP + PNG fallback | 750×1334 | 72 | |
| Product screenshot | PNG | Native | 2× retina | |
| Diagram | SVG | Vector | n/a | Inline in HTML where possible |
| Sector report | PDF/A-1b | A4 portrait | Print-grade | Embed fonts |
| Deck | PDF + native (`.key`, `.pptx`) | 1920×1080 | 72 | 16:9 |
| Event backdrop | PDF | Vector | Print-grade | Bleeds + crop marks |

All exports are sRGB on screen, CMYK on print. Do not mix.

---

## 5. On-brand checklist for any asset

Before exporting an asset, run this checklist:

- [ ] Uses Deep Navy, Slate, Emerald Teal, Soft Silver, or White only
      (state colors allowed when carrying state).
- [ ] Wordmark or monogram placed per `DEALIX_LOGO_USAGE.md`.
- [ ] Tagline present if the surface requires it.
- [ ] Type uses Inter (Latin) and IBM Plex Sans Arabic (Arabic).
- [ ] No banned vocabulary (guaranteed revenue/sales/meetings, hype words).
- [ ] All customer references have approval recorded in the proof ledger.
- [ ] All metrics carry a denominator or an "early signal, n=X" disclosure.
- [ ] RTL layouts use logical CSS / Figma auto-layout direction.
- [ ] WCAG AA contrast preserved.
- [ ] Filename follows the naming convention.

A reviewer signs off by ticking the boxes. The asset does not ship until
the checklist is clean.

---

## 6. Hero images

- Background: Deep Navy. If a photograph is used, overlay it with Deep
  Navy at 80%+ opacity.
- Headline: Inter Bold, white, `4xl`–`5xl`.
- Sub-headline: Inter Medium, Soft Silver, `xl`.
- CTA button: Emerald Teal background, Deep Navy text. (On a white
  section CTA, the button background is Deep Navy with white text — see
  the color rule in `DEALIX_COLOR_SYSTEM.md`.)
- Decorative element: at most one — typically the teal swoosh arc.

Hero images do not contain stock photography of "businesspeople pointing
at screens". They contain product UI screenshots, abstract diagrams, or a
typographic field.

---

## 7. OG cards

OG cards are the single most-shared Dealix asset. They follow a strict
template.

- Background: Deep Navy.
- Monogram: top-left (LTR) or top-right (RTL), 64 px tall.
- Title: Inter Semibold, white, `3xl`, 2 lines max.
- Optional subtitle: Inter Medium, Soft Silver, `lg`, 1 line.
- Bottom-left: small wordmark + tagline at `xs`.
- Bottom-right: a faint teal swoosh, no text.

The OG card does not contain a CTA. The shared link is the CTA.

---

## 8. Product screenshots

- Capture at 2× device pixel ratio.
- Crop tightly to the relevant feature. Do not show empty chrome.
- Mask any real customer data: use the staging "Demo Co." dataset, or
  blur identifying fields. Never publish a screenshot containing a real
  customer's data without that customer's written approval.
- Annotate sparingly. Where annotation is needed, use Emerald Teal
  callouts on a Slate overlay.
- Do not auto-add browser chrome unless the surface requires it (e.g.
  an iOS Safari screenshot). When you do, use a clean macOS Safari /
  Chrome chrome — never a third-party "screenshot beautifier" frame.

---

## 9. Diagrams

Dealix diagrams favor flow over ornament. The visual grammar:

- Nodes are Slate cards with 1 px Soft Silver borders.
- Edges are 1.5 px lines: Soft Silver for inert, Emerald Teal for
  active.
- Arrowheads are filled triangles, not chevrons.
- Labels use Inter Medium, white on dark / Deep Navy on light.
- Layout is left-to-right in LTR, right-to-left in RTL.
- Diagrams export as SVG. Inline in HTML where possible so they scale
  and search.

---

## 10. Quote cards (customer / operator quotes)

Quote cards are the **most-regulated** asset type because they involve
proof publication.

Rules:
1. The customer name, logo, and the quote text must each be approved in
   writing and logged in the proof ledger before the asset is produced.
2. The card displays: the quote in Inter Medium `xl`, the attribution
   (name, role, company) in Inter Regular `sm`, the customer logo at
   reduced opacity, and the Dealix monogram in the bottom corner.
3. The card does not include a stat unless that stat is also approved.
4. Quote cards in Arabic require an Arabic-native review pass.

If any approval is missing, the asset stays in draft.

---

## 11. Stat cards

Stat cards highlight a single number. The number must carry a denominator
or a disclosure.

- Headline number: Inter Bold, `5xl`, Emerald Teal (on dark) or Deep
  Navy (on light).
- Denominator or disclosure: Inter Regular, `xs`, directly under the
  number. Example: "across 14 Saudi B2B pilots, Q1 2026".
- Topic label: Inter Medium, `sm`, Soft Silver.
- Dealix monogram in the corner.

A stat card without a denominator or disclosure is off-brand.

---

## 12. Report PDFs

- A4 portrait, single column.
- Cover: Deep Navy background, large Inter Bold title, monogram,
  publication date, version number.
- Body: White background, Inter for headings, Inter for body, Soft
  Silver hairline rules.
- Tables: alternating rows in `#F3F5F8`. Headers in Inter Semibold.
- Disclosures: methodology, sample size, date range, "results vary"
  notice — always at the end, never absent.
- Last page: contact, version, change log.

Reports are exported as PDF/A-1b with embedded fonts and pass the basic
PDF accessibility checklist.

---

## 13. Email banners

- 600×200 px max.
- Solid Deep Navy background — no images of people, no stock backgrounds.
- Wordmark + tagline centered. Or a small headline (Inter Semibold `xl`,
  white) for campaign banners.
- File size under 100 KB.
- ALT text in plain language, Arabic if the email is Arabic.

---

## 14. Decks

Native deck files (`.key`, `.pptx`) live alongside the PDF export. Native
files allow editing; PDFs are the canonical share.

- Slide master uses Deep Navy or White surfaces. Pick one per deck.
- Mixing dark and light slides in the same deck is allowed but should
  follow a section rhythm (e.g. cover and section dividers dark, body
  light).
- Slide numbers, footer with date, and "DEALIX" wordmark in the footer.
- No more than 30% of the slide is image; the rest is type and white
  space.

---

## 15. Publication workflow

1. Designer opens the relevant master in Figma.
2. Designer edits, runs the on-brand checklist (section 5).
3. Brand director reviews.
4. If the asset references a customer or a metric, founder + legal
   review.
5. Exports written to `assets/brand/marketing/{type}/...` per naming
   convention.
6. Asset linked from the publication surface (site, email campaign,
   social post).
7. Asset recorded in the proof ledger if it includes any external
   claim.

A draft asset never escapes step 4 unless someone broke the rule.

---

## 16. Bilingual note — العربية

كل أصل تسويقي يجب أن يحمل بصمة دِيليكس البصرية واللغوية. الألوان الخمسة
الأساسية، خطّا Inter و IBM Plex Sans Arabic، الشعار في موضعه الصحيح،
الشعار النصّي والشعار الفرعي حيث يلزم. لا نَنشر اسم عميل أو رقماً أو شعار
شركة دون موافقة مكتوبة موثّقة. الأصول العربية ليست ترجمة حرفية للأصول
الإنجليزية، بل صياغة أصلية بنفس النّبرة والمضمون. أسماء الملفات
بالإنجليزية فقط، باستخدام لاحقة `_ar` للإصدارات العربية، و`_bil`
لثنائية اللغة.
