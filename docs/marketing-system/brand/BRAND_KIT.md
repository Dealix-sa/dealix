# Dealix Brand Kit — عروض ومواد دعائية

**المرجع التفصيلي:** [`../../sales-kit/dealix_brand_guidelines.md`](../../sales-kit/dealix_brand_guidelines.md)  
**Tokens الآلية:** [`brand-tokens.yaml`](brand-tokens.yaml) · **CSS مشترك:** [`marketing-shared.css`](marketing-shared.css)

---

## الألوان (60-30-10)

| Token | Hex | الاستخدام |
|-------|-----|-----------|
| `deep_green` | `#0A4D3F` | عناوين، خلفيات هيدر، أزرار أساسية |
| `gold` | `#C9A961` | CTA ثانوي، تمييز، أرقام رئيسية |
| `sand` | `#F4F0E8` | خلفيات شرائح فاتحة |
| `charcoal` | `#1A1A1A` | نص أساسي |
| `warm_gray` | `#6B6B6B` | نص ثانوي |

لا تضع Gold و Green بنفس الوزن البصري — الذهب accent فقط.

---

## الخطوط

| اللغة | العائلة | العناوين | النص |
|-------|---------|----------|------|
| عربي | IBM Plex Sans Arabic (+ Noto fallback) | Bold 700 | Regular 400 |
| إنجليزي | Inter | SemiBold 600 | Regular 400 |
| أكواد | JetBrains Mono | — | 400 |

**RTL:** `direction: rtl` + مرآة كاملة للتخطيط (انظر [`../presentations/RTL_QA_CHECKLIST.md`](../presentations/RTL_QA_CHECKLIST.md)).

---

## شبكة الشرائح (16:9)

```
┌────────────────────────────────────────────────────────┐
│ 48px margin                                            │
│  ┌──────────────────────────────────────────────────┐  │
│  │ ACTION TITLE (max ~15 words, conclusion-first)   │  │
│  ├──────────────────────────────────────────────────┤  │
│  │                                                  │  │
│  │     ONE visual anchor (chart / diagram / quote)    │  │
│  │                                                  │  │
│  │  supporting bullets (max 3–5, secondary weight)    │  │
│  └──────────────────────────────────────────────────┘  │
│ 48px margin                          footer: logo + #   │
└────────────────────────────────────────────────────────┘
```

- **عمود واحد للرسالة الرئيسية**؛ لا عمودين متساويين يتنافسان.
- **حد أقصى ~30 كلمة** في جسم الشريحة (استثناء: جدول مقارنة واحد).
- **عنوان الشريحة = الاستنتاج** (أسلوب McKinsey action title).

### أنماط العناوين

| النمط | مثال |
|-------|------|
| استنتاج | «تأخر الرد يهدر ٤٠٪ من الفرص في أول ٣٠ يوماً» |
| رقم | «سبرنت ٧ أيام يُنتج ١٠ حسابات مُرتّبة + Proof Pack» |
| سؤال (افتتاح فقط) | «ماذا يكلفكم عدم توحيد بيانات الإيرادات؟» |

إذا احتوى العنوان «و» — افصل لشريحتين.

### الجداول

- رأس الجدول: خلفية `#0A4D3F`، نص أبيض.
- صفوف متناوبة: `#FFFFFF` / `#F4F0E8`.
- أرقام الجداول: Western (123)؛ السرد: Arabic-Indic اختياري.

---

## مكوّنات قابلة لإعادة الاستخدام

| المكوّن | الاستخدام |
|---------|-----------|
| بطاقة حالة | قبل/بعد، نتائج Sprint |
| قمع/مسار | pipeline، conversion |
| MAP مصغّر | خطوة تالية بعد الاجتماع |
| شارة امتثال | «مسودة فقط — لا إرسال بارد» |

أيقونات: Lucide، stroke 2px، 20–24px.

---

## ربط PowerPoint / Google Slides / Figma

1. استورد `brand-tokens.yaml` يدوياً أو عبر Figma variables (الألوان أعلاه).
2. Master slide: خلفية `sand` أو `white`؛ شريحة غلاف `deep_green` + شعار أبيض.
3. قالب جاهز للنص: انسخ من [`../presentations/live-deck-b2b-ar.md`](../presentations/live-deck-b2b-ar.md).

---

## موافقة النشر

قبل إرسال أي asset خارجي: مراجعة ضد NON_NEGOTIABLES (لا وعود صفقات، لا إرسال بارد).
