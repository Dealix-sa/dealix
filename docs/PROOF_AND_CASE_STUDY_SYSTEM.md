# Dealix — Proof & Case Study System
<!-- PHASE 6 | Owner: Founder | Updated: 2026-05-18 -->
<!-- NO_FAKE_PROOF | NO_PUBLIC_WITHOUT_CONSENT -->

> **القاعدة الأساسية:** لا دليل = لا ادعاء. لا موافقة = لا نشر.
> كل case study يمر بـ 4 مراحل: إثبات → توثيق → موافقة → نشر.

> **حالة الشركة:** صفر عملاء دافعين. لا يوجد Proof Pack حقيقي بعد. القالب
> في §8 أدناه **قالب فارغ بحقول نائبة** — يُملأ فقط بأدلة موثّقة من Sprint
> فعلي. لا يُملأ مسبقاً بنتائج وهمية تحت أي ظرف.
>
> **Company status:** zero paying customers. No real Proof Pack exists yet.
> The template in §8 is an **empty, placeholder-only** template — filled
> only with documented evidence from an actual Sprint. Never pre-filled with
> fabricated results.

---

## 1. أنواع أحداث الإثبات (Proof Events)

| نوع الحدث | التعريف | مستوى الدليل | يُعدّ إثباتاً لـ |
|-----------|---------|-------------|-----------------|
| `diagnostic_delivered` | تم تسليم تقرير تشخيصي للعميل | L1 — أساسي | الكفاءة التشخيصية |
| `draft_approved` | وافق العميل على مسودة رسالة | L2 — متوسط | جودة المخرجات |
| `message_sent_by_client` | أرسل العميل رسالة مبنية على مسودتنا | L3 — قوي | قيمة عملية |
| `meeting_booked` | حُجز اجتماع نتيجة رسالة Dealix | L4 — قوي جداً | أثر مباشر |
| `deal_progressed` | صفقة انتقلت مرحلة نتيجة المتابعة | L4 — قوي جداً | أثر مباشر |
| `payment_received` | تم تحصيل دفع من عميل Dealix | L5 — أقوى | الإيراد الحقيقي |
| `client_testimonial` | شهادة مكتوبة من العميل | L5 — أقوى | ثقة اجتماعية |

---

## 2. مستويات الدليل

### L1 — Delivered (تم التسليم)
```
المطلوب: مخرج تم إرساله للعميل
مقبول في: عروض داخلية فقط
غير مقبول في: تسويق خارجي أو ادعاءات ROI
```

### L2 — Approved (تم الموافقة)
```
المطلوب: موافقة مكتوبة أو رسالة موافقة من العميل
مقبول في: عروض Pilot لعملاء مشابهين
غير مقبول في: ادعاءات ROI أو نتائج مالية
```

### L3 — Acted (تم التطبيق)
```
المطلوب: دليل أن العميل استخدم المخرج فعلياً
مقبول في: "ساعدنا [نوع شركة] على [إجراء محدد]"
غير مقبول في: ادعاءات عائد مالي محدد
```

### L4 — Impacted (أثر موثق)
```
المطلوب: ربط مباشر بين مخرج Dealix ونتيجة تجارية
مقبول في: "أدى إلى [نتيجة] في [إطار زمني]"
غير مقبول في: ادعاءات ROI% بدون حسابات مدققة
```

### L5 — Validated (نتيجة مُثبتة)
```
المطلوب: نتيجة مالية أو شهادة رسمية + موافقة النشر
مقبول في: Case study كامل + تسويق خارجي
شرط: موافقة مكتوبة وموقعة
```

---

## 3. متطلبات الموافقة (Consent Requirements)

### قبل البدء في Pilot
- [ ] DPA موقّع (نموذج: `docs/DPA_PILOT_TEMPLATE.md`)
- [ ] موافقة على معالجة البيانات (PDPL)
- [ ] فهم واضح أن المخرجات للاستخدام الداخلي

### قبل بناء Case Study
- [ ] موافقة مكتوبة لاستخدام الحالة في التسويق
- [ ] تحديد مستوى الإفصاح (اسم الشركة / قطاع فقط / مجهول)
- [ ] مراجعة العميل للنص قبل النشر

### قبل النشر العام
- [ ] موافقة نشر موقّعة (أو رسالة موافقة واضحة)
- [ ] مراجعة المؤسس النهائية
- [ ] تطبيق التحريرات المطلوبة

---

## 4. مراحل بناء Case Study

### المرحلة 1: التقاط حدث الإثبات
```
المصدر: Proof Pack اليوم 7 من كل Sprint
التوثيق: sprint_id + client_id + proof_event_type + date + evidence
التخزين: /proof_ledger (داخلي فقط)
```

### المرحلة 2: تحرير القصة
```
الهيكل الأساسي:
  - الخلفية: [نوع الشركة، القطاع — بدون اسم حتى الموافقة]
  - التحدي: ما الألم الذي واجهته؟
  - الحل: ما الذي قدمه Dealix؟ (مخرجات حقيقية فقط)
  - النتيجة: ماذا حدث؟ (L4 أو L5 فقط)
  - الشهادة: [اقتباس مباشر — بموافقة فقط]

محظورات:
  ✗ لا "وفّرنا X%" بدون قياس حقيقي
  ✗ لا "أغلقنا X صفقة" بدون دليل
  ✗ لا "ضمنّا ROI" في أي صياغة
```

### المرحلة 3: طلب الموافقة
```
نص طلب الموافقة (العربية):

"[الاسم]، شكراً على ثقتك في Dealix.
كتبت ملخصاً لما حققناه معاً في Sprint الأخير.
هل تسمح لي باستخدامه [في عروض / على موقعنا / في LinkedIn]؟
طبعاً، أي تعديل تطلبه — يصير.
يمكنني إرسال النص للمراجعة أولاً لو تريد."
```

### المرحلة 4: الإصدار والنشر
```
أنواع النشر (بترتيب الأمان):
  [داخلي]   → proof_ledger فقط (لا موافقة مطلوبة)
  [مجهول]   → "شركة خدمات سعودية B2B..." (يحتاج موافقة قطاع)
  [جزئي]    → قطاع + حجم (يحتاج موافقة مكتوبة)
  [كامل]    → اسم الشركة + شهادة (يحتاج موافقة موقّعة)
```

---

## 5. سياسة التحرير والإخفاء (Redaction Policy)

### ما يُحرّر دائماً (بدون موافقة محددة)
- أسماء موظفين غير المؤسس
- أرقام مالية محددة (إلا بموافقة صريحة)
- بيانات عملاء الشركة العميلة
- معلومات pipeline أو استراتيجية تنافسية

### ما يمكن إظهاره بموافقة L2+
- قطاع الشركة
- حجم الشركة (تقريبي)
- نوع التحدي

### ما يتطلب موافقة L5
- اسم الشركة
- اسم المؤسس
- أرقام مالية محددة
- شهادات مكتوبة

---

## 6. نموذج طلب الشهادة (Testimonial Request Flow)

### الوقت المناسب: اليوم 7 من Sprint أو بعد نتيجة L4+

```
[رسالة واتساب]

"[الاسم]، ممتنن جداً على ثقتك.
سؤال صغير: لو تكتب 2-3 جمل عن تجربتك مع Dealix،
تكون من أهم الأشياء تساعدنا في مساعدة شركات مشابهة.

لا يلزمك شيء — بس لو كانت التجربة إيجابية ومريح معها،
أي كلام بسيط يكفي."

[إذا وافق]
"شكراً! هل تسمح أستخدمه [وصف الاستخدام]؟"

[إذا رفض]
"تمام تماماً، أقدّر تجاوبك.
شكراً على وقتك في Sprint — هيكون مرجع لنا للتحسين."
```

---

## 7. سجل الإثباتات (Proof Ledger Template)

```yaml
proof_id: PLX-001
sprint_id: SPR-001
date: 2026-MM-DD
client_sector: [B2B Services / Agency / Consulting]
client_size: [5-15 / 15-50]
proof_events:
  - type: diagnostic_delivered
    level: L1
    date: Day 1
  - type: drafts_approved
    count: 5
    level: L2
    date: Day 4
  - type: client_testimonial
    level: L5
    consent: written
    date: Day 7
kpis_baseline:
  pipeline_size: [insufficient_data]
  deals_count: X
kpis_end:
  drafts_delivered: 5
  drafts_approved: 5
  meetings_booked: [insufficient_data]
public_permission: none | sector_only | full
notes: ""
```

---

---

## 8. قالب Proof Pack القابل لإعادة الاستخدام (Reusable Proof Pack TEMPLATE)

> ⚠️ **هذا قالب فارغ.** كل `[ ]` حقل نائب يُملأ بدليل موثّق فقط — من Proof
> Pack اليوم 7 لـ Sprint فعلي. لا يُملأ بأرقام مفترضة. لا يُنشر خارجياً
> إلا بعد موافقة نشر موقّعة (راجع §3 و§4).
>
> ⚠️ **This is an empty template.** Every `[ ]` is a placeholder filled only
> with documented evidence from a real Sprint's Day-7 Proof Pack. Never
> filled with assumed numbers. Not published externally without signed
> publication consent.

```markdown
# Proof Pack — [client_id] — [التاريخ / Date]
<!-- INTERNAL until signed publication consent. Status: TEMPLATE — empty -->

## 0. الميتاداتا / Metadata
- proof_id: [PLX-NNN]
- sprint_id: [SPR-NNN]
- client_sector: [قطاع — بدون اسم حتى الموافقة / sector — no name until consent]
- client_size: [نطاق تقريبي / approximate range]
- delivery_mode: [verified product (Rung 0–1) / founder-assisted (Rung 3–5)]
- prepared_by: [Founder]
- public_permission: [none | sector_only | partial | full]

## 1. ملخص الإثبات / Proof Summary
- أعلى مستوى دليل تحقّق / Highest evidence level reached: [L1 | L2 | L3 | L4 | L5]
- عدد أحداث الإثبات الموثّقة / Documented proof events: [N]
- ملاحظة: لا يُذكر أي ادّعاء لا يسنده حدث موثّق أدناه.

## 2. أحداث الإثبات / Proof Events (evidence-backed only)
| الحدث / Event | المستوى / Level | التاريخ / Date | الدليل / Evidence ref |
|---|---|---|---|
| [diagnostic_delivered] | [L1] | [Day 1] | [ملف/لقطة موثّقة / file ref] |
| [draft_approved ×N] | [L2] | [Day N] | [رسالة موافقة العميل / approval msg ref] |
| [meeting_booked] | [L4] | [Day N] | [دليل الحجز / booking proof ref] |
| [ ... ] | [ ] | [ ] | [ ] |

## 3. المؤشّرات / KPIs (entered by client or measured — never assumed)
| المؤشّر / Metric | قبل / Baseline | نهاية Sprint / End | المصدر / Source |
|---|---|---|---|
| [حجم pipeline / pipeline size] | [insufficient_data أو رقم العميل] | [ ] | [client-entered] |
| [مسودات مُسلّمة / drafts delivered] | [—] | [ ] | [Dealix log] |
| [مسودات موافَق عليها / drafts approved] | [—] | [ ] | [client approval] |
| [اجتماعات محجوزة / meetings booked] | [insufficient_data] | [ ] | [documented] |

> أي خانة بلا دليل = `insufficient_data`. لا تُملأ بتقدير.
> Any cell without evidence = `insufficient_data`. Never estimated.

## 4. القيمة / Value framing
- القيمة التقديرية / Estimated value: [محسوبة من مدخلات العميل فقط / from
  client inputs only — clearly labelled estimate]
- القيمة المُتحقَّقة / Verified value: [فقط إن وُجد دليل L5 + موافقة /
  only with L5 evidence + consent — otherwise: not available]

## 5. حدود وإفصاحات / Limitations & disclosures
- [ما الذي لم يُقَس؟ / what was not measured]
- [ما الذي يتطلّب فترة أطول لإثباته؟ / what needs longer to prove]
- نمط التسليم لهذه الدرجة / delivery mode disclosure: [ ]

## 6. الموافقة / Consent status
- DPA موقّع / signed: [نعم/لا — راجع docs/DPA_PILOT_TEMPLATE.md]
- موافقة نشر / publication consent: [none — انظر
  docs/wave8/PROOF_PUBLICATION_CONSENT_TEMPLATE.md]
- مستوى الإفصاح المسموح / disclosure level allowed: [ ]

---
Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
```

**أين يُحفظ:** القالب المملوء يُحفظ داخلياً في `/proof_ledger` فقط. لا
يتحوّل إلى case study عام إلا عبر مراحل §3–§4 وبموافقة نشر موقّعة.

---

*Version 1.1 | NO_FAKE_PROOF gate enforced | All public content requires explicit consent | Reusable Proof Pack template added 2026-05-18 — empty placeholders only*

---

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.*
