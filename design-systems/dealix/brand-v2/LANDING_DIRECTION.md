# Dealix — Landing Page Direction (Brand v2)

> Direction spec, not implementation. Captures the visual and behavioral rules for `dealix.sa` and any v2 marketing surface. Implementation is a separate task — see [`BRAND.md` § Roadmap](./BRAND.md).

---

## 1. النبرة البصرية · Visual Tone

**Dark premium · fintech-meets-AI.**

- خلفية أساسية: navy `#0B1220` — لا أبيض، لا رمادي فاتح، لا gradients ملوّنة.
- اللون الوحيد المضيء: teal `#00D1A1` (للـ CTAs والـ growth signals).
- النصوص: أبيض للـ headlines، silver `#B2BBC6` للـ body الثانوي.
- مساحة بيضاء سخية — عمودي 96px+ بين الـ sections.
- الإحساس: "Bloomberg Terminal" + "Stripe" + "Linear" — هادئ، دقيق، واثق.

**ممنوع · Forbidden:**
- ❌ Gradients vivid (purple/pink/orange).
- ❌ stock illustrations (cartoon people، abstract blobs).
- ❌ parallax scrolling.
- ❌ autoplay video أو Lottie loops.
- ❌ testimonial sliders.
- ❌ "as seen on" logo strips غير مُثبتة.
- ❌ countdown timers أو fake scarcity badges.

---

## 2. هيكل الصفحة · Section Blueprint

```
┌─────────────────────────────────────────────────────┐
│  1. Hero                                            │
│     - Tagline (AR + EN)                             │
│     - Sub-headline (one line, value)                │
│     - Primary CTA (teal) + Ghost CTA (silver)       │
│     - Icon-only logo above wordmark                 │
├─────────────────────────────────────────────────────┤
│  2. Trust strip                                     │
│     - Real customer logos OR named pilots only      │
│     - "12 Saudi accounts · 4 verticals" — receipts  │
├─────────────────────────────────────────────────────┤
│  3. Five Pillars                                    │
│     - 5 cards (one per brand pillar)                │
│     - Icon + AR name + EN name + 1-line desc        │
├─────────────────────────────────────────────────────┤
│  4. Product surface preview                         │
│     - Real dashboard screenshot (navy UI)           │
│     - 3 callouts pointing to KPIs / proof packs     │
├─────────────────────────────────────────────────────┤
│  5. Outcomes row                                    │
│     - 3 case-study cards                            │
│     - Real numbers, source-linked, no claims w/o    │
│       receipts                                      │
├─────────────────────────────────────────────────────┤
│  6. Pricing teaser                                  │
│     - 5-rung ladder (Free → Sprint → Pack → Ops →   │
│       Custom)                                       │
│     - One CTA: "ابدأ بـ Free Diagnostic"            │
├─────────────────────────────────────────────────────┤
│  7. Footer                                          │
│     - Trust marks (PDPL, ZATCA, NCA aligned)        │
│     - Bilingual links                               │
│     - Horizontal monochrome logo                    │
└─────────────────────────────────────────────────────┘
```

---

## 3. الـ Hero — Treatment

- **Background:** navy `#0B1220` fill، مع radial gradient teal خفيف جدًا (opacity 0.08) في الزاوية السفلية اليمنى (RTL) للإضاءة.
- **Logo:** `icon.svg` 96×96px أعلى المنتصف.
- **Wordmark:** "DEALIX" أبيض، Sora 700، 96px، letter-spacing 14.
- **Tagline:** teal `#00D1A1`، Space Grotesk 500، 22px، letter-spacing 5، uppercase.
  - AR: "صفقات ذكية. نمو حقيقي."
  - EN: "INTELLIGENT DEALS. REAL GROWTH."
- **Subhead:** silver، 20px، سطر واحد فقط، يصف القيمة لا الميزة.
- **CTAs:**
  - Primary: teal fill، navy text، radius `md` (14px)، padding `24×48`.
  - Ghost: silver outline 1px، silver text، نفس الـ radius والـ padding.
- **Height:** 100vh على الـ desktop، 85vh على الـ mobile.

---

## 4. المكونات · Components

### Cards
- Background: `slate` `#0F1726`.
- Border: 1px `border` (`#1F2A44`).
- Radius: `lg` (20px).
- Padding: 32px.
- Hover: border يتحوّل لـ teal 50% opacity، transform translateY(-2px).

### Buttons
- **Primary (teal fill):** background teal، text navy، weight 600. Hover → `teal_light` `#34E3B5`. Active → `teal_dark` `#00A37D`.
- **Ghost (silver outline):** background transparent، border 1px silver، text silver. Hover → border white، text white.
- Radius: `md` (14px). لا تستخدم pill إلا في الـ chips.

### KPI Tile
- Background: `slate`.
- KPI number: Sora 700، 48px، teal.
- Label: Space Grotesk 500، 14px، silver، uppercase، letter-spacing 4.
- Source link: 12px تحت الـ tile، silver underline.

### Chips / Badges
- pill radius (9999px).
- Success → teal على navy 12% opacity fill.
- Warn → `#E0A744` على نفس fill.
- Danger → `#D45656` على نفس fill.

---

## 5. الحركة · Motion

- **Ease:** `cubic-bezier(0.2, 0.8, 0.2, 1)` — مُعاد من
  [`landing/styles.css` `--ease`](../../../landing/styles.css).
- **Duration:** أقصى 400ms للـ scroll reveal. CTAs 180ms.
- **النمط الوحيد المسموح:** fade + translateY(8px → 0).
- ممنوع: parallax، scale-in dramatic، rotate، typewriter، particle effects.
- `prefers-reduced-motion: reduce` → عطّل كل الحركة الاختيارية فورًا.

---

## 6. Typography on Landing

| Use | Token | Family | Size |
|---|---|---|---|
| Hero AR    | `display` | IBM Plex Sans Arabic 700 | 64px |
| Hero EN    | `display` | Sora 700                 | 64px |
| Section H2 | `3xl`     | Sora 600                 | 30px |
| Card title | `xl`      | Sora 600                 | 20px |
| Body       | `base`    | Space Grotesk / Plex AR  | 16px |
| Caption    | `xs`      | Space Grotesk / Plex AR  | 12px |

- Arabic content يحصل على `lang="ar" dir="rtl"`.
- لا تخلط arabic + english في نفس السطر — استخدم sub-blocks.

---

## 7. RTL / Bilingual

- الـ default direction: RTL (Arabic-primary). راجع
  [`../DESIGN.md` §1](../DESIGN.md).
- Toggle EN ↔ AR في الـ navbar أعلى يسار (LTR) / أعلى يمين (RTL).
- لا تترجم الـ tagline داخل الـ hero — اعرضها AR و EN معًا على سطرين.

---

## 8. الأداء · Performance Budget

- LCP < 2.0s على 4G سعودي.
- Total page weight < 600 KB (excluding hero screenshot).
- Fonts: subset Sora + Plex AR Latin/Arabic فقط، preload الـ display weight.
- لا third-party scripts thicker than analytics (Plausible/Umami مُفضّل، لا Google Tag Manager بـ 20 سكربت).
- صور: AVIF/WebP، lazy-load كل شيء خارج الـ first viewport.

---

## 9. التبعيات على الـ Code القائم · Code Dependencies

> هذا الـ direction يفترض الترحيل التالي في الـ codebase. لا تنفّذ الـ landing v2 بدون هذه التحديثات أولًا:

1. `landing/styles.css` — أعد ربط `--accent` و `--accent-2` إلى
   `#00D1A1` / `#34E3B5`. `--ink-900` (`#0b1220`) ✅ مطابق بالفعل.
2. `frontend/tailwind.config.ts` — أضف `navy`, `teal`, `silver`, `slate` palettes من
   [`tokens.json`](./tokens.json). احتفظ بـ `gold` / `emerald` كـ deprecated.
3. Fonts — أضف Sora و Space Grotesk إلى الـ font loader.

كل هذا مدوّن كـ follow-up في [`BRAND.md` § Roadmap](./BRAND.md).

---

## 10. القياس · How we know it's working

- زائر يفتح الصفحة → خلال 5 ثوانٍ يعرف:
  1. ما هي Dealix.
  2. لمن.
  3. الخطوة التالية.
- Bounce rate < 50% على الـ desktop SA traffic.
- CTA primary CTR > 8%.
- لا شكوى من "يبدو مثل أي landing AI" — التميّز البصري هدف صريح.

---

## مراجع · References

- [`BRAND.md`](./BRAND.md) — الهوية الكاملة.
- [`tokens.json`](./tokens.json) — القِيَم.
- [`assets/logos/`](./assets/logos/) — الأصول.
- [`../DESIGN.md`](../DESIGN.md) — قواعد RTL / forbidden copy.
- [`../../../landing/styles.css`](../../../landing/styles.css) — الـ tokens القائمة (للـ migration reference).
