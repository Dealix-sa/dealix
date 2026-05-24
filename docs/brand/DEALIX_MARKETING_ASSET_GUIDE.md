# Dealix Marketing Asset Guide | دليل الأصول التسويقية

> Templates, sizing, and shipping rules for every marketing asset Dealix puts into the world.

---

## 1. Asset Inventory | جرد الأصول

| Surface | Asset | Owner |
|---|---|---|
| Landing | Hero, section illustration, OG image | Marketing |
| LinkedIn | Post image (1080×1080, 1200×627), carousel (1080×1350) | Marketing |
| X | Post image (1600×900), header (1500×500) | Marketing |
| Instagram | Post (1080×1080), story (1080×1920), reel cover (1080×1920) | Marketing |
| YouTube | Thumbnail (1280×720), channel art (2560×1440) | Marketing |
| Email | Header (600×200), CTA banner (600×120) | Marketing |
| Decks | Investor, sales, partner | Sales / Founder |
| Print | One-pager (A4), case study (A4 4-page) | Marketing |
| Event | Banner (stand-up, pull-up), table card | Marketing |

---

## 2. Open Graph (OG) Images | صور المشاركة

- **Size:** 1200×630px (Twitter card auto-derives 800×418).
- **Background:** Deep Navy `#0B1220`.
- **Wordmark:** White, top-left, 64px height, 64px from edges.
- **Headline:** Inter Semibold 56–72px, white, max 8 words.
- **Subhead (optional):** Inter Regular 24px, Soft Silver, max 12 words.
- **Accent:** Single Emerald Teal rule or chip — never a decorative blob.
- **Arabic OG:** IBM Plex Sans Arabic Semibold, RTL layout, wordmark top-right.

Naming: `og-<slug>-<lang>.jpg` (e.g., `og-revenue-sprint-en.jpg`).

---

## 3. Social Posts | منشورات التواصل

**Square (1080×1080)**
- 80px safe-area on all sides.
- Wordmark monogram top-left.
- One headline (≤ 10 words), one supporting line (≤ 14 words).
- Emerald Teal accent reserved for a single CTA or chip.

**Carousel (1080×1350, 5–10 slides)**
- Slide 1: hook (question or sharp claim).
- Slides 2–N: one idea per slide, one chart per slide.
- Final slide: CTA + wordmark + handle.

**Story / Reel cover (1080×1920)**
- Safe zone: 250px top, 350px bottom (avoid platform UI overlays).
- Center the headline; keep wordmark inside the safe zone.

---

## 4. LinkedIn | لينكدإن

- **Post images:** 1200×627 for link previews; 1080×1080 for native posts.
- **Document posts ("PDF carousels"):** 1080×1350 per page, 8–12 pages, exported as PDF.
- **Founder profile banner:** 1584×396, Deep Navy with white wordmark + one-line positioning.
- **Company banner:** 1128×191, Deep Navy with tagline lockup.

---

## 5. Sales & Investor Decks | عروض المبيعات والمستثمرين

| Deck | Slides | Aspect | Owner |
|---|---|---|---|
| Founder/Investor | 12–16 | 16:9 | Founder |
| Sales (long) | 10–14 | 16:9 | Sales |
| Sales (short) | 5–7 | 16:9 | Sales |
| Partner | 8–10 | 16:9 | Partnerships |

**Master template rules:**
- Cover slide: Deep Navy, wordmark top-left, tagline lockup centered, date in caption.
- Section dividers: full-bleed Deep Navy with Emerald Teal eyebrow label.
- Content slides: max 1 chart + 1 headline + ≤ 5 bullets.
- Closing slide: clear next step, owner name, contact, and the line "Approval-gated. Evidence-led."

---

## 6. Case Studies & Proof Packs | الحالات الدراسية

- Never publish without **written customer approval** (non-negotiable).
- Template includes: context → constraint → what shipped → what changed → next step.
- Numbers always in ranges with conditions and pilot N.
- Logo placement only after partner co-brand approval.
- Reference: `docs/PROOF_AND_CASE_STUDY_SYSTEM.md`.

---

## 7. Email Assets | أصول البريد

- **Header banner:** 600×200, Deep Navy, white wordmark, no decorative imagery.
- **CTA banner:** 600×120, Emerald Teal background, Deep Navy headline, button-style.
- **Footer:** 600×80, Soft Silver text on Deep Navy, includes physical address, unsubscribe link, and the line "Dealix — approval-gated revenue OS for Saudi B2B."
- All emails render dark-mode safe (test in Gmail dark + Outlook).

---

## 8. Event & Print | الفعاليات والمطبوعات

- **Roll-up banner (85×200 cm):** Deep Navy, wordmark top, single headline mid-height, QR to landing at bottom.
- **One-pager (A4):** white background, Deep Navy headline, one chart, one CTA. Bilingual variants in two separate files.
- **Business card:** Deep Navy face with monogram; back lists name, role, email, mobile, and Dealix.sa.

---

## 9. Approval Workflow | سير الموافقة

```
Brief  →  Draft  →  Brand Lead review  →  Function lead review  →  Approve to ship  →  Log in asset registry
```

- **Required gates** for any customer-facing asset:
  1. Brand consistency check (colors, type, logo).
  2. Voice check (no hype, no guaranteed claims).
  3. Bilingual parity check.
  4. Accessibility check (contrast, alt text).
  5. Non-negotiables check (no auto-send, no unpublished proof, no pricing without escalation).
- **Customer logos & quotes** require written customer approval before publish.

---

## 10. File Hygiene | تنظيم الملفات

- Source files in Figma "Dealix Marketing" project.
- Exports in `assets/marketing/<surface>/<yyyy>/<slug>/`.
- Naming: `dealix-<surface>-<slug>-<lang>-<size>.<ext>`.
- Retain editable source + final exports. Never delete a shipped asset.

---

## 11. Do / Don't | افعل / لا تفعل

**Do**
- Use the master templates.
- Test on dark mode + RTL.
- Keep one idea per asset.
- Cite numbers with ranges, conditions, and pilot N.

**Don't**
- Don't add new accent colors.
- Don't auto-publish anything that names a customer.
- Don't put white text on Emerald Teal.
- Don't ship an English asset without an Arabic counterpart on bilingual surfaces.

---

## 12. KPI | مؤشرات الأداء

- Brand consistency score per shipped asset (target ≥ 90%).
- Bilingual asset coverage on KSA-facing surfaces (target 100%).
- Time-to-publish from approved brief (target ≤ 5 working days).
- Approval-gate violations (target 0).

---

## 13. Related Documents | مراجع

- `DEALIX_BRAND_SYSTEM.md`
- `DEALIX_VISUAL_IDENTITY.md`
- `DEALIX_LOGO_USAGE.md`
- `DEALIX_ACCESSIBILITY_GUIDE.md`
- `docs/marketing/DEALIX_MARKETING_OS.md`
