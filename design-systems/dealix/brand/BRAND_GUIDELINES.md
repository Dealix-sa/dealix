# Dealix — Brand & Visual Identity Guidelines — دليل الهوية البصرية

> **Governed AI Operations for Saudi B2B — عمليات ذكاء اصطناعي محوكمة لشركات الأعمال السعودية**
>
> Arabic-primary, English-secondary. Evidence-first. Approval-first. PDPL-native.
> هذا الدليل وثيقة عملية للمصمّم والمطوّر — لا توجد مزاعم تسويقية لا يدعمها سجل الخدمات أو سجل الإثبات.

---

## 0. How to use this document — كيف تستخدم هذا الدليل

- المصمّم: استخدم الألوان والخطوط والمكوّنات كما هي. لا تخترع درجات أو ظلالاً جديدة خارج اللوحة.
- المطوّر: القيم هنا متطابقة مع رموز Tailwind و CSS المتغيّرة في نهاية الملف. ارجع إلى الأسماء، لا إلى الـ hex مباشرةً داخل المكوّنات.
- Designer: use these colors, type, and components verbatim. Do not invent new tints or shadows outside the palette.
- Developer: values map to the Tailwind tokens and CSS variables at the end. Reference token names, not raw hex inside components.

Related: [`design-systems/dealix/DESIGN.md`](../DESIGN.md) (DesignOps tokens & component recipes) · [`design-systems/dealix/docs/IMPLEMENTATION_GUIDE.md`](../docs/IMPLEMENTATION_GUIDE.md).

---

## 1. Brand essence & positioning — جوهر العلامة والتموضع

### عربي

**Dealix** هو نظام تشغيل إيرادات محوكم للشركات السعودية B2B. نحن لا نبيع «أداة ذكاء اصطناعي» ولا قوائم باردة — نبيع **قدرة تشغيل** مصحوبة بـ **دليل قابل للتدقيق**: نرتّب البيانات، نحدّد الفرص، نجهّز مسودات آمنة، ونُخرج قرارات مربوطة بـ Decision Passport و Proof Pack.

ركائز الهوية:

- **الحوكمة قبل الأتمتة (Approval-first):** لا إجراء خارجي بدون موافقة بشرية صريحة.
- **الدليل قبل الادعاء (Evidence-first):** كل رقم مصدره سجل حقيقي، لا تقدير تسويقي.
- **سعودي أولاً (Saudi-first):** عربي أولاً، PDPL-native، ZATCA-aware.
- **الوضوح التنفيذي:** نتيجة أولاً، ثم الدليل، ثم الخطوة التالية.

### English

**Dealix** is a governed revenue operations capability for Saudi B2B companies. We do not sell "an AI tool" or cold lists — we sell **operating capability** backed by **auditable proof**: we organize data, surface opportunities, prepare safe drafts, and issue decisions tied to a Decision Passport and a Proof Pack.

Identity pillars:

- **Approval-first:** no external action without explicit human approval.
- **Evidence-first:** every number comes from a real record, never a marketing estimate.
- **Saudi-first:** Arabic-primary, PDPL-native, ZATCA-aware.
- **Executive clarity:** outcome first, then evidence, then the next step.

### Brand personality — شخصية العلامة

| Is — هي | Is not — ليست |
|---|---|
| Decisive, calm, precise — حازمة، هادئة، دقيقة | Hype, loud, salesy — صاخبة، مبالِغة |
| Evidence-backed — مدعومة بالأدلة | "AI-powered" buzzword — شعار جوفاء |
| Saudi-executive — بلغة تنفيذية سعودية | Generic global SaaS — SaaS عام بلا سياق |
| Trust-led — تقودها الثقة | Automation-at-any-cost — أتمتة بأي ثمن |

---

## 2. Logo usage — استخدام الشعار

### Logo system — منظومة الشعار

- **Primary mark:** geometric diamond form with an embedded "D" — شكل ماسي هندسي يتضمّن حرف "D".
- **Variations:** Full logo (mark + wordmark), mark-only (favicon / avatar / app icon), horizontal, vertical/stacked, monochrome (navy or white), reversed (white on dark).
- **Default usage:** mark + wordmark on a solid Navy `#001F3F` or white surface.

### Clear space & minimum size — المساحة الآمنة والحد الأدنى

- **Clear space — المساحة الآمنة:** keep clear space equal to the height of the "D" mark on all four sides. No other element (text, icon, edge) enters this zone.
- **Minimum size — الحد الأدنى:** 40px tall for digital, 20mm for print. Mark-only: 24px minimum.
- **Backgrounds — الخلفيات:** prefer solid Navy or white. On photography, place the logo on a Navy overlay (opacity ≥ 70%) so contrast stays legible.

### Do — افعل

- Maintain aspect ratio and approved color versions — حافظ على النسبة والألوان المعتمدة.
- Use the reversed (white) logo on Navy or dark imagery — استخدم النسخة البيضاء على الداكن.
- Scale proportionally from the corner — كبّر بنسبة متساوية.

### Don't — لا تفعل

- Rotate, skew, stretch, or compress — لا تدوير أو تشويه أو تمديد.
- Recolor outside Navy / Gold / white — لا ألوان خارج Navy / Gold / الأبيض.
- Add drop shadows, glows, gradients, or outlines to the mark — لا ظلال أو توهّج أو تدرّجات على الشعار.
- Place on low-contrast or busy backgrounds — لا خلفيات منخفضة التباين أو مزدحمة.
- Use an outdated version or recreate the mark by hand — لا نسخ قديمة ولا إعادة رسم يدوي.

---

## 3. Color palette — لوحة الألوان

### Primary — الأساسية

| Name — الاسم | Hex | RGB | Tailwind | When to use — متى تُستخدم |
|---|---|---|---|---|
| **Dealix Navy** | `#001F3F` | 0, 31, 63 | `bg-dealix-navy` | Primary surfaces, headers, nav, hero backgrounds — 60–70% من التصميم |
| **Dealix Gold** | `#D4AF37` | 212, 175, 55 | `bg-dealix-gold` | Accents, primary CTAs, active states, premium markers — 5–10% فقط |
| **Dealix Black** | `#0A0A0A` | 10, 10, 10 | `text-dealix-black` | Dark body text on light surfaces — النصوص الداكنة |
| **White** | `#FFFFFF` | 255, 255, 255 | `text-white` / `bg-white` | Text on dark, light surfaces, negative space — النص على الداكن والمساحات البيضاء |

### Secondary & functional — الثانوية والوظيفية

| Name — الاسم | Hex | RGB | Tailwind | When to use — متى تُستخدم |
|---|---|---|---|---|
| Slate | `#364558` | 54, 69, 88 | `text-dealix-slate` | Secondary text, muted captions — النصوص الثانوية |
| Light Gray | `#F3F4F6` | 243, 244, 246 | `bg-dealix-light` | Card backgrounds on light, dividers — خلفيات البطاقات الفاتحة |
| Info (Ocean) | `#0066FF` | 0, 102, 255 | `text-dealix-ocean` | Links, informational states — الروابط والمعلومات |
| Success (Emerald) | `#10B981` | 16, 185, 129 | `text-dealix-emerald` | Live / approved / proven — مكتمل / معتمد / مُثبت |
| Warning (Amber) | `#F59E0B` | 245, 158, 11 | `text-dealix-amber` | Pilot / pending / needs attention — قيد التجربة / بانتظار |
| Error (Coral) | `#EF4444` | 239, 68, 68 | `text-dealix-coral` | Error / destructive only — خطأ / إجراء خطير فقط |

### Color rules — قواعد اللون

- **Navy carries the brand.** It is the dominant surface; Gold is the spark, never the field — Navy هو السطح المهيمن، و Gold شرارة وليست خلفية.
- **Gold ≤ 10%.** Reserve Gold for the single most important action per view — احصر Gold في أهم إجراء واحد لكل شاشة.
- **One CTA color per email.** Never use Navy and Gold buttons in the same email — لون CTA واحد لكل بريد.
- **Functional colors are semantic, not decorative.** Coral red is for errors only; it is never a brand accent — الأحمر للأخطاء فقط، لا كلمسة جمالية.
- **Status uses color + label, never color alone** (accessibility) — الحالة تُعرَّف باللون والنص معاً.

### Accessibility / contrast — التباين وإمكانية الوصول

| Pairing — التزاوج | Ratio | WCAG |
|---|---|---|
| Navy `#001F3F` + White `#FFFFFF` | 12.6:1 | AAA |
| Gold `#D4AF37` + Navy `#001F3F` | 7.4:1 | AAA |
| White on Gold (body text) | ~1.7:1 | Fail — never put white body text on Gold; use Navy text on Gold |
| Slate `#364558` + White | ~8.6:1 | AAA |

- Minimum target: **4.5:1** for body text, **3:1** for large text and UI borders.
- **Gold + Navy** is the canonical CTA pairing: **Navy text on a Gold fill**, or **Gold text on a Navy fill**.
- Focus ring: `ring-dealix-gold` at 2px, always visible on keyboard navigation.

---

## 4. Typography — الطباعة

### Font stack — حزمة الخطوط

| Role — الدور | English | Arabic | Weight | Tailwind |
|---|---|---|---|---|
| Display / headings — العناوين | Poppins | Cairo | 700–900 | `font-display` |
| Body / UI — النصوص والواجهة | Inter | Tajawal | 400–600 | `font-body` |
| Mono — الكود والمعرّفات | IBM Plex Mono | IBM Plex Mono | 400 | `font-mono` |

- Mono is reserved for evidence IDs, hashes, version stamps, and code — الـ mono للمعرّفات والإصدارات والكود فقط.
- All families ship with local-system fallbacks — لكل عائلة بدائل نظام محلية.

### Scale — السلّم

| Level | Tailwind | Size / line-height | Weight |
|---|---|---|---|
| H1 | `text-5xl font-black font-display` | 48 / 56 | 900 |
| H2 | `text-4xl font-black font-display` | 36 / 44 | 800 |
| H3 | `text-2xl font-bold font-display` | 28 / 36 | 700 |
| H4 | `text-xl font-bold font-display` | 24 / 32 | 600 |
| Body Large | `text-lg` | 18 / 28 | 400 |
| Body | `text-base` | 16 / 24 | 400 |
| Body Small | `text-sm` | 14 / 22 | 400 |
| Caption | `text-xs` | 12 / 18 | 500 |

### Arabic typography — الطباعة العربية

- Use Cairo (600/700/900) for headings, Tajawal (400–700) for body and UI.
- Arabic line-height is **+0.2** over English (target 1.8 for body) for diacritic safety — ارتفاع السطر العربي أعلى بمقدار 0.2 لسلامة التشكيل.
- Always set `dir="rtl"` and `lang="ar"` on Arabic surfaces; switch English sub-blocks locally with `lang="en" dir="ltr"`.
- Arabic prose may use Arabic-Indic numerals (٠–٩); tables and KPIs use ASCII digits for parseability.
- Arabic punctuation: `،` and `؟` in Arabic blocks. Never mix scripts of punctuation.

---

## 5. Iconography & imagery tone — الأيقونات والصور

### Iconography — الأيقونات

- **Style:** minimal geometric line icons — أيقونات خطية هندسية بسيطة.
- **Stroke:** 2px. **Base size:** 24px, scale proportionally.
- **Color:** Navy default, Gold for a single accent per group — Navy افتراضياً و Gold للمسة واحدة.
- Mirror semantically directional icons (forward/back) under RTL using logical properties (`margin-inline-start`, not `margin-left`).

### Imagery — الصور

- **Tone:** calm, professional, evidence-forward — هادئة، احترافية، تنفيذية.
- **People:** diverse Saudi professionals at work; natural, warm lighting — كوادر سعودية متنوعة، إضاءة طبيعية دافئة.
- **Settings:** modern offices, dashboards, collaborative spaces — مكاتب حديثة ولوحات بيانات.
- **Color treatment:** warm neutrals graded toward Navy/Gold — معالجة لونية محايدة دافئة تميل لـ Navy/Gold.
- **Avoid:** stock "robot/AI brain" clichés, glowing neon, fake dashboards with invented numbers — تجنّب صور «الروبوت/دماغ AI»، والنيون، واللوحات بأرقام مخترعة.

### Patterns — الأنماط

- **Primary:** geometric dot grid (Navy + Gold), 16px spacing, 2px dots, 5–10% opacity, background only.
- **Secondary:** subtle Gold divider lines in headers. Optional, premium indicator — لمسة فاخرة اختيارية.

---

## 6. UI component accents — لمسات مكوّنات الواجهة

### Buttons — الأزرار

| Variant | Spec |
|---|---|
| **Primary (Gold)** | Fill `dealix-gold`, text `dealix-navy`, bold, radius 8, `shadow-gold` — أهم إجراء |
| **Primary (Navy)** | Fill `dealix-navy`, text white, radius 8 — على الأسطح الفاتحة |
| **Secondary** | Transparent, 1px `white/20` border, hover border `dealix-gold` — إجراء ثانوي |
| **Destructive** | Outline 1px `dealix-coral`, text coral. Never solid red — لا يُملأ بالأحمر |

- Disabled buttons are **never silent**: always paired with a one-line reason ("approval required", "evidence missing") — الزر المعطّل دائماً بسبب مكتوب.
- Default state for any send/publish action: **Approval Required** — الحالة الافتراضية لأي إرسال: «بانتظار الموافقة».

### Cards, badges, chips — البطاقات والشارات

- **Card:** `bg-white/5`, `border-white/10`, `hover-gold`, no heavy shadow on Navy — بطاقة هادئة على Navy.
- **Badge:** `bg-dealix-gold/20`, text `dealix-gold`, `border-dealix-gold/30` — شارة ذهبية خفيفة.
- **Evidence badge:** mono text `EVT-<id>` / `PROOF-<id>`, always links to the proof ledger, never decorative — شارة الدليل تربط دائماً بسجل الإثبات.
- **Status chips (canonical only):** `Live`, `Pilot`, `Partial`, `Target`, `Blocked`, `Approval Required`, `Draft Only`, `Internal Only` — أسماء الحالات الثمانية المعتمدة فقط (انظر [`DESIGN.md`](../DESIGN.md)).

### Forms, nav, focus — النماذج والتنقّل

- Input height 44px, 1px border, focus = 2px Gold border + ring.
- Primary nav: Navy background, white text, Gold accent on the active item.
- Error = Coral, Success = Emerald — always with an icon and label.

### Available CSS utilities — أدوات CSS الجاهزة

```css
.gradient-text       /* Gold gradient on text — تدرّج ذهبي على النص */
.navy-surface        /* Navy gradient background — خلفية Navy متدرّجة */
.dot-pattern         /* Subtle gold dot background — نقاط ذهبية خفيفة */
.glass               /* Glassmorphism — تأثير زجاجي */
.hover-gold          /* Gold border + glow on hover — حد وتوهّج ذهبي */
.animate-gold-pulse  /* Continuous gold pulse — نبضة ذهبية */
.animate-fade-up     /* Fade + rise on enter — ظهور مع حركة لأعلى */
```

---

## 7. Tone of voice — نبرة الصوت

### Principles — المبادئ

1. **Outcome → evidence → next step.** Open with the result, link the proof, then state the action — النتيجة ثم الدليل ثم الخطوة.
2. **Specific numbers from the ledger.** Never round up to a marketing-friendly figure — أرقام محددة من السجل، لا تقريب تسويقي.
3. **Calm verbs.** Prefer "delivered", "verified", "approved", "in pilot", "blocked pending review" — أفعال هادئة دقيقة.
4. **Bilingual = parallel.** Every external string has Arabic and English of equal weight — كل نص خارجي عربي وإنجليزي متوازيان.
5. **Disclosure always present.** Customer-facing markdown ends with the estimated-vs-verified line — كل ملف للعميل ينتهي بسطر التقدير مقابل التحقّق.

### Example phrases — عبارات نموذجية

| Context | عربي ✅ | English ✅ |
|---|---|---|
| Value line | «نُرتّب بياناتك ونكشف أين تضيع الفرص — بدليل قابل للتدقيق.» | "We organize your data and surface where opportunities leak — with auditable proof." |
| Governance | «لا رسالة خارجية بدون موافقتك. مسودة ثم موافقة ثم سجل.» | "No external message without your approval. Draft, then approve, then log." |
| Error | «لا تملك صلاحية الوصول بعد. تواصل مع المسؤول لطلبها.» | "You don't have access yet. Contact your admin to request it." |
| Next step | «الخطوة التالية: تشخيص مجاني — بدون التزام.» | "Next step: a free diagnostic — no commitment." |

### Forbidden copy — العبارات الممنوعة (verbatim)

Never use these in a **positive (asserted)** context anywhere — page, email, proposal, deck, dashboard:

`نضمن` · `guaranteed` · `revenue guaranteed` · `ranking guaranteed` · `blast` · `scrape` · `cold WhatsApp` · `fully automated external send`

- A negation context ("Dealix never does fully automated external send") is allowed, must be allowlisted, and stays under founder review — السياق النافي مسموح ويبقى تحت مراجعة المؤسس.
- Replace "guaranteed sales / نضمن مبيعات" with "evidenced opportunities / فرص مُثبتة بأدلة".

### Voice do / don't — افعل / لا تفعل

**Do — افعل**

- Lead with a concrete noun and a real outcome — ابدأ باسم ملموس ونتيجة حقيقية.
- Say "estimated" or "case-safe pattern" when a number is not verified — قل «تقديري» أو «نمط آمن» عند عدم التحقّق.
- Keep Arabic primary and first in reading order — العربية أولاً في ترتيب القراءة.

**Don't — لا تفعل**

- Don't promise sales, conversion rates, or ROI as fact — لا وعود بمبيعات أو تحويل أو عائد كحقيقة.
- Don't describe scraping, cold WhatsApp/LinkedIn automation, or bulk outreach as services — لا توصيف للأتمتة الباردة أو الإرسال الجماعي كخدمة.
- Don't use emojis, model names, or hype verbs in shipped artefacts — لا إيموجي ولا اسم نموذج ولا أفعال مبالِغة.

---

## 8. Implementation tokens — رموز التنفيذ

```css
:root {
  /* Brand */
  --color-navy:    #001F3F;
  --color-gold:    #D4AF37;
  --color-black:   #0A0A0A;
  --color-white:   #FFFFFF;
  /* Secondary & functional */
  --color-slate:   #364558;
  --color-light:   #F3F4F6;
  --color-info:    #0066FF; /* Ocean */
  --color-success: #10B981; /* Emerald */
  --color-warning: #F59E0B; /* Amber */
  --color-error:   #EF4444; /* Coral */
  /* Type */
  --font-display: 'Poppins', 'Cairo', system-ui, sans-serif;
  --font-body:    'Inter', 'Tajawal', system-ui, sans-serif;
  --font-mono:    'IBM Plex Mono', ui-monospace, monospace;
  /* Radius */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;
}
```

Tailwind token names (canonical): `dealix-navy`, `dealix-gold`, `dealix-black`, `dealix-slate`, `dealix-light`, `dealix-ocean`, `dealix-emerald`, `dealix-amber`, `dealix-coral`.

---

## 9. RTL / bilingual rules — قواعد RTL والثنائية

- Default direction `dir="rtl"`, `lang="ar"` on customer-facing surfaces; English sub-blocks use `lang="en" dir="ltr"`.
- Arabic first in reading order; English under it. Never side-by-side columns on mobile — العربية أولاً، الإنجليزية تحتها، لا أعمدة متجاورة على الجوال.
- Use logical CSS properties (`margin-inline-start`, `text-align: end`) so layouts mirror correctly.
- Numeric columns: right-aligned in LTR, start-aligned in RTL.

---

**Version:** 2.0 · **Owner:** Dealix Brand · **Status:** Production · **Updated:** 2026-06-07
