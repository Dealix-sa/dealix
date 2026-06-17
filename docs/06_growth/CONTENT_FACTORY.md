# Content Factory — Dealix Self-Growth OS

مصنع التسويق الذاتي: مدخلات تشغيلية يومية → مخرجات محتوى يومية → إعادة
استخدام كل فكرة إلى ~10 أصول. كل أصل يحمل **CTA واحد**، والمحتوى الذي
يلمس عميلًا حقيقيًا (proof / case-safe) **يحتاج موافقة المؤسس قبل النشر.**

> المصدر الحي للأفكار: [`data/growth/content_ideas.jsonl`](../../data/growth/content_ideas.jsonl).
> التقويم: `python3 scripts/growth/generate_content_calendar.py`
> → [`reports/growth/CONTENT_CALENDAR_30D.md`](../../reports/growth/CONTENT_CALENDAR_30D.md).

---

## المدخلات (كل يوم)

market intelligence · diagnostic notes · customer proof packs · objections ·
delivery lessons · sector signals · founder thoughts.

## المخرجات (كل يوم)

5 LinkedIn posts · 2 short video scripts · 1 newsletter · 1 blog post ·
1 sector page update · 1 case-safe insight · 1 partner note · 1 founder build log.

---

## أنواع المحتوى

| النوع | الهدف |
|---|---|
| Founder insight | بناء ثقة |
| Pain education | رفع وعي |
| Framework | جعل Dealix مرجعًا |
| Proof story (case-safe) | إثبات |
| Operational teardown | جذب شركات |
| Tool launch | جذب inbound |
| Partner note | فتح قنوات |
| Objection answer | بيع بدون إفشاء |

---

## آلة إعادة الاستخدام (Repurposing)

كل فكرة → 10 أصول. مثال على موضوع «CRM لا يكفي بدون operating rhythm»:

```
LinkedIn post · short video · blog · newsletter · carousel
· landing page section · email nurture · sales objection answer
· academy lesson · partner talking point
```

---

## Proof-to-Content Flywheel

```
Delivery → Proof Pack → Anonymized Insight → LinkedIn → Blog
→ Sector Page → Diagnostic CTA → More Demand
```

مثال case-safe (بدون ذكر اسم العميل):

> «في إحدى شركات الخدمات، المشكلة لم تكن نقص leads؛ كانت غياب next action
> واضح بعد كل محادثة.»

قوالب جاهزة: `python3 scripts/growth/generate_case_safe_content.py`
→ [`reports/growth/CASE_SAFE_CONTENT.md`](../../reports/growth/CASE_SAFE_CONTENT.md).

---

## بوابة الحوكمة

- أي محتوى خارجي = **يحتاج review** من المؤسس.
- العناصر بحالة `needs-approval` في `content_ideas.jsonl` تظهر مفلَّمة (⚠)
  في التقويم ولا تُنشر تلقائيًا.
- لا fake proof، لا fake testimonials، لا أرقام غير مُتحقَّقة.
- كل أصل: **CTA واحد** فقط — لا تكدّس CTAs.
- لا محتوى عام عن «AI» — اربطه دائمًا بألم تشغيلي محدد.

---

## القنوات

- **Organic Search** — SEO طويل المدى (انظر `AI_SEARCH_GEO_STRATEGY.md`).
- **AI Search / GEO** — صيغة سؤال/جواب.
- **LinkedIn Founder-Led** — أفضل قناة B2B الآن (1 pain + 1 framework +
  1 proof + 1 build log + 1 CTA).
- **YouTube Shorts / TikTok** — مقاطع قصيرة حول ألم واحد.
- **Newsletter** — *Dealix Weekly Command Brief*.
- **Partner Referrals** — بعد أول 3 Proof Packs.
- **Paid Ads** — لاحقًا فقط، بعد معرفة ICP/angle/landing/offer.

---

## كيف نضيف فكرة

1. أضف سطرًا في `data/growth/content_ideas.jsonl`
   (id, type, topic_ar, pillar, cta, channel, status).
2. اضبط `status=needs-approval` لأي محتوى proof/case-safe.
3. شغّل `generate_content_calendar.py` لرؤيتها مجدولة.
