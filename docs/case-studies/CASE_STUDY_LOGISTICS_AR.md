# دراسة حالة — شركة لوجستيات سعودية (مُجهَّلة الهوية)
# Case Study — Saudi Logistics Company (Anonymized)

> **دراسة حالة توضيحية — بناءً على نتائج Sprint نموذجية في قطاع اللوجستيات**
> **Illustrative case study — based on typical Sprint findings in the logistics sector**
>
> هذه دراسة حالة توضيحية مُركَّبة. لا تُشير إلى عميل حقيقي محدد. جميع الأرقام والسيناريوهات مبنية على أنماط منهجية نموذجية متوقعة في قطاع اللوجستيات السعودي. الأسماء والتفاصيل التعريفية محذوفة امتثالاً لنظام حماية البيانات الشخصية (PDPL).
>
> This is a composite illustrative case study. It does not refer to any specific real client. All figures and scenarios are based on typical methodological patterns expected in Saudi logistics sector engagements. Names and identifying details are removed in compliance with PDPL.

روابط: [SPRINT_DELIVERY_PLAYBOOK.md](../03_commercial_mvp/SPRINT_DELIVERY_PLAYBOOK.md) | [PROOF_PACK_STANDARD.md](../07_proof_os/PROOF_PACK_STANDARD.md) | [CASE_STUDY_TECHNOLOGY_COMPANY_AR.md](./CASE_STUDY_TECHNOLOGY_COMPANY_AR.md)

---

## ملف الشركة — Company Profile

| الخاصية | التفاصيل |
|---|---|
| القطاع | لوجستيات وتوزيع B2B / B2B Logistics and Distribution |
| الحجم | 120 موظفاً (تقدير) |
| الموقع | الدمام — المنطقة الشرقية |
| نوع العمل | عقود لوجستيات B2B متكررة، فوترة إلكترونية مرتفعة الحجم |
| التحديات الرئيسية | عدم امتثال ZATCA المرحلة الثانية + تسريب إيرادات من عقود منتهية غير مُجدَّدة |
| التصنيف | مُجهَّل — لا اسم حقيقي، لا أرقام إيراد فعلية |

---

## المشكلة — The Problem

**بالعربية:**
الشركة واجهت ضغطاً من جبهتين في آنٍ واحد:

**الجبهة الأولى — عدم الامتثال لـ ZATCA:**
كانت الشركة تُصدر فواتير B2B بحجم يومي مرتفع، لكن مدير العمليات اكتشف في مراجعة داخلية أن ثلاثة تنسيقات فواتير لا تستوفي متطلبات المرحلة الثانية من ZATCA. المشكلة لم تُكتشَف إلا عندما بدأ أحد عملاء المؤسسات يرفض فواتير معينة من نظام Fatoora. هذا الرفض كان يعني تأخير التحصيل وخطر الغرامات.

**الجبهة الثانية — تسريب الإيرادات من العقود المنتهية:**
مع تطور عمليات الشركة عبر السنوات، تراكمت عقود خدمات لوجستية مع عملاء مؤسسات لم تُجدَّد في مواعيدها. لم يكن هناك نظام يتابع تواريخ الانتهاء ويُنبّه المبيعات مسبقاً. النتيجة: عقود بقيمة مُقدَّرة 47,000 ريال كانت قابلة للتجديد لكنها تركت في حالة ركود.

المؤسس أدرك أن المشكلتين مترابطتان: شركة غير متوافقة مع ZATCA تُعرّض نفسها لانقطاع في التدفق النقدي يُزيد من حدة خسائر العقود المتروكة.

**In English:**
The company faced pressure from two directions simultaneously:

**Front 1 — ZATCA Non-compliance:**
The company issued high-volume daily B2B invoices, but an internal review revealed that three invoice formats did not meet ZATCA Phase 2 requirements. The problem was discovered only when a major enterprise client began having invoices rejected by Fatoora. This rejection meant collection delays and penalty risk.

**Front 2 — Revenue Leakage from Lapsed Contracts:**
As the company grew over the years, logistics service contracts with enterprise clients accumulated without systematic renewal tracking. No system tracked expiry dates and alerted the sales team in advance. Result: contracts with an estimated value of SAR 47,000 were renewable but left dormant.

The founder recognized the problems were interconnected: a ZATCA non-compliant company faces cash flow interruptions that compound contract revenue losses.

---

## رحلة الـ 7 أيام — The 7-Day Journey

**بالعربية:**

### اليوم الأول — تحديد النطاق وتوقيع جواز المصدر

قبل أي عمل، وقّع مدير العمليات بصفته مالك سير العمل على جوازَي مصدر منفصلَين:

**جواز المصدر 1 — بيانات الفواتير:**
- المالك: الشركة
- نوع المصدر: تصدير نظام ERP للفواتير
- الاستخدام المسموح به: مراجعة امتثال ZATCA فقط
- علامة PII: نعم (تفاصيل الطرف المقابل)
- مدة الاحتفاظ: 90 يوماً

**جواز المصدر 2 — بيانات العقود:**
- المالك: الشركة
- نوع المصدر: تصدير قاعدة بيانات العقود
- الاستخدام المسموح به: تحليل تسريب الإيرادات فقط
- علامة PII: نعم (أسماء جهات الاتصال في المؤسسات)
- مدة الاحتفاظ: 90 يوماً

لا يبدأ العمل دون توقيعَي الجواز — هذا تطبيق مبدأ APPROVAL_FIRST من اليوم الأول.

### اليوم الثاني — مراجعة امتثال ZATCA

حُلِّلت عينة من 200 فاتورة B2B من الثلاثة أشهر الأخيرة.

**النتائج:**
- **تنسيق الفاتورة A:** مستوفٍ لمتطلبات المرحلة الثانية (XML صحيح، QR Code موجود، حقول إلزامية مكتملة).
- **تنسيق الفاتورة B:** قيمة VAT محسوبة بطريقة خاطئة في حالات الخصم — 23 فاتورة متأثرة في العينة.
- **تنسيق الفاتورة C:** رقم التسجيل الضريبي للمشتري مفقود في حقل إلزامي — 31 فاتورة متأثرة في العينة.
- **تنسيق الفاتورة D (فواتير الائتمان):** تنسيق XML لا يحتوي على الإشارة المطلوبة إلى رقم الفاتورة الأصلية — 11 فاتورة متأثرة.

**إجمالي الفواتير ذات مشاكل امتثال في العينة:** 65 من 200 (32.5% من العينة).

### اليوم الثالث — تحليل العقود وتحديد التسريب

حُلِّلت 156 عقداً نشطاً وسابقاً من قاعدة البيانات.

**النتائج:**
- **عقود منتهية غير مُجدَّدة ولا تزال قابلة للتجديد:** 8 عقود
- **القيمة التقديرية السنوية الإجمالية لهذه العقود:** 47,000 ريال (بناءً على قيمة آخر عقد + متوسط الزيادة السنوية للقطاع — تقدير، لا ضمان)
- **متوسط عمر كل عقد متروك:** 4.2 شهراً منذ الانتهاء
- **8 عقود إضافية:** تنتهي خلال 60 يوماً القادمة — تتطلب متابعة استباقية

### اليوم الرابع — قياس جودة البيانات

حُسبت درجة DQ على بيانات العقود:
- **النتيجة الأولية: 69/100**
- الأبعاد الضعيفة: الحداثة (تواريخ الانتهاء لم تُحدَّث في 40% من السجلات)، الاكتمال (جهات تواصل التجديد مفقودة في 28% من العقود)

### اليوم الخامس — مراجعة الحوكمة

أُجريت مراجعة حوكمة شاملة بمبدأ APPROVAL_FIRST:

- **قرارات مُسجَّلة:** 11
- **إجراءات موصى بها للتواصل الخارجي:** 6 — جميعها مُصنَّفة DRAFT_ONLY، لا إرسال دون موافقة مُسجَّلة من مدير المبيعات
- **مسودات مُوقَّفة (BLOCK):** 1 — تضمنت ادعاءً بأن Dealix سيحل مشكلة ZATCA تلقائياً (ادعاء مضلل)
- **مسودات تحتاج إزالة PII (REDACT):** 2 — تضمنت اسم جهة التواصل في نص المعاينة

**تحذير ZATCA الحرج:** تم رفع تنبيه رسمي لمدير العمليات بضرورة تصحيح التنسيقات B وC وD قبل إرسال أي فاتورة B2B جديدة. هذا إجراء داخلي — لا يتضمن Dealix إرسال أي بلاغ لـ ZATCA نيابةً عن العميل دون موافقة صريحة.

### اليوم السادس — إعداد خارطة الإجراءات

أُعِدَّت قائمة إجراءات مُرتَّبة بالأولوية:

1. تصحيح التنسيقات B وC وD في نظام الفوترة (إجراء تقني داخلي للعميل).
2. متابعة 8 عقود منتهية غير مُجدَّدة (مسودات جاهزة، تتطلب موافقة للإرسال).
3. إعداد نظام تنبيه للعقود المنتهية خلال 60 يوماً.
4. توثيق الأساس القانوني لبيانات جهات التواصل في العقود.

### اليوم السابع — تسليم حزمة الإثبات

تسليم Proof Pack كامل + خارطة إجراءات مُفصَّلة.

**In English:**

### Day 1 — Scope Definition and Source Passport Signing

Before any work, the Operations Manager as workflow owner signed two separate Source Passports:

**Source Passport 1 — Invoice Data:**
- Owner: company
- Source type: ERP invoice export
- Allowed use: ZATCA compliance review only
- PII flag: yes (counterparty details)
- Retention: 90 days

**Source Passport 2 — Contract Data:**
- Owner: company
- Source type: contract database export
- Allowed use: revenue leakage analysis only
- PII flag: yes (enterprise contact names)
- Retention: 90 days

Work begins only after both passports are signed — APPROVAL_FIRST from day one.

### Day 2 — ZATCA Compliance Review

A sample of 200 B2B invoices from the last three months was analyzed.

**Findings:**
- **Invoice Format A:** compliant with Phase 2 (correct XML, QR Code present, mandatory fields complete).
- **Invoice Format B:** VAT value calculated incorrectly in discount scenarios — 23 invoices affected in sample.
- **Invoice Format C:** buyer tax registration number missing from a mandatory field — 31 invoices affected in sample.
- **Invoice Format D (credit notes):** XML format missing the required reference to the original invoice number — 11 invoices affected.

**Total invoices with compliance issues in sample:** 65 of 200 (32.5% of sample).

### Day 3 — Contract Analysis and Leakage Identification

156 active and historical contracts analyzed from the database.

**Findings:**
- **Lapsed contracts not renewed, still renewable:** 8 contracts
- **Total estimated annual value of these contracts:** SAR 47,000 (based on last contract value plus estimated sector-average annual increase — estimate, not guarantee)
- **Average age of each dormant contract:** 4.2 months since expiry
- **Additional 8 contracts:** expiring within the next 60 days — require proactive follow-up

### Day 4 — Data Quality Measurement

DQ score computed on contract data:
- **Initial score: 69/100**
- Weak dimensions: currency (expiry dates not updated in 40% of records), completeness (renewal contact missing in 28% of contracts)

### Day 5 — Governance Review

Full governance review under APPROVAL_FIRST:

- **Decisions logged:** 11
- **Recommended external communications:** 6 — all classified DRAFT_ONLY, no sending without logged Sales Manager approval
- **Blocked drafts (BLOCK):** 1 — contained a claim that Dealix would resolve ZATCA issues automatically (misleading claim)
- **PII redaction required (REDACT):** 2 — contained contact name in preview text

**Critical ZATCA alert:** A formal alert was raised to the Operations Manager to correct Formats B, C, and D before sending any new B2B invoices. This is an internal action — Dealix does not file any communication with ZATCA on the client's behalf without explicit approval.

### Day 6 — Action Map Preparation

Priority-ranked action list prepared.

### Day 7 — Proof Pack Delivery

Full Proof Pack delivered with detailed action map.

---

## مخرجات السبرنت — Sprint Outputs

**بالعربية:**

| المخرج | التفاصيل |
|---|---|
| درجة جودة البيانات (بيانات العقود) | 69/100 |
| تنسيقات فواتير لا تستوفي ZATCA الثانية | 3 من أصل 4 تنسيقات |
| فواتير متأثرة في العينة | 65 من 200 |
| عقود منتهية قابلة للتجديد | 8 عقود |
| القيمة التقديرية للعقود المتروكة | 47,000 ريال/سنة (تقدير) |
| عقود تنتهي خلال 60 يوماً | 8 عقود |
| مسودات تواصل جاهزة للمراجعة | 6 (DRAFT_ONLY) |
| درجة حزمة الإثبات | 77/100 |

**In English:**

| Output | Detail |
|---|---|
| Data quality score (contract data) | 69/100 |
| Invoice formats failing ZATCA Phase 2 | 3 of 4 formats |
| Invoices affected in sample | 65 of 200 |
| Lapsed renewable contracts | 8 contracts |
| Estimated value of dormant contracts | SAR 47,000/year (estimate) |
| Contracts expiring within 60 days | 8 contracts |
| Communication drafts ready for review | 6 (DRAFT_ONLY) |
| Proof Pack score | 77/100 |

---

## ردود الفعل التوضيحية للمؤسس — Illustrative Founder Reaction

> **ملاحظة:** هذه الاقتباسات افتراضية توضيحية. لا تُمثّل قولاً حرفياً لعميل حقيقي.
> **Note:** These quotes are illustrative hypotheticals. They do not represent the literal words of a real client.

**بالعربية:**
"كنا نظن أن مشكلة ZATCA هي تقنية بحتة تُحل مع مزوّد نظام ERP. لكن السبرنت أوضح أن المشكلة في 3 تنسيقات فواتير مختلفة، وأن عندنا 47,000 ريال من العقود المتروكة لم نكن نعرف عنها. هذا يُغيّر الصورة الكاملة."

**In English:**
"We thought the ZATCA problem was purely technical, to be resolved with our ERP provider. The sprint showed that the issue spans 3 different invoice formats, and that we had SAR 47,000 in dormant contracts we were not aware of. That changes the complete picture."

---

## نتائج الشهر الثاني — Month 2 Outcomes (Estimated Pattern)

> **تذكير:** هذه نتائج توضيحية مُستهدفة لا قياسات متحقق منها.
> **Reminder:** These are illustrative target outcomes, not verified measurements.

**بالعربية:**

في الشهر الثاني بعد السبرنت (بعد تصحيح التنسيقات وتفعيل مسودات التواصل بموافقة مُسجَّلة):

- امتثال ZATCA محقَّق: تنسيقات B وC وD صُحِّحت.
- 6 من أصل 8 عقود متروكة جُدِّدت (نمط متوقع — لا ضمان).
- العقود الـ 8 المُنتهية خلال 60 يوماً دخلت في مسار متابعة استباقية.
- وقّعت الشركة على **Managed Ops Essential بسعر 2,999 ريال/شهر** لمواصلة المراقبة الشهرية.

**In English:**

In month 2 post-sprint (after format correction and draft activations with logged approvals):

- ZATCA compliance achieved: Formats B, C, and D corrected.
- 6 of 8 dormant contracts renewed (expected pattern — not a guarantee).
- 8 contracts expiring within 60 days entered a proactive follow-up track.
- Company signed **Managed Ops Essential at SAR 2,999/month** for ongoing monthly monitoring.

---

## ما يتضمنه Managed Ops Essential لهذا العميل — What Managed Ops Essential Includes for This Client

**بالعربية:**

| الخدمة | التكرار |
|---|---|
| مراقبة امتثال ZATCA: فحص تنسيقات الفواتير والربط مع Fatoora | شهري |
| تقرير جودة البيانات: 6 أبعاد مع مقارنة شهرية | شهري |
| تنبيهات العقود: قائمة بالعقود المنتهية خلال 60 يوماً القادمة | شهري |
| مراجعة مخاطر PDPL: جوازات المصادر ومدد الاحتفاظ | شهري |
| مسودات تواصل لتجديد العقود (DRAFT_ONLY) | حسب الحاجة، بموافقة مُسجَّلة |
| جلسة مراجعة شهرية (45 دقيقة) | شهري |
| تحديث حزمة الإثبات | ربع سنوي |

**In English:**

| Service | Frequency |
|---|---|
| ZATCA compliance monitoring: invoice format checks and Fatoora integration | Monthly |
| Data quality report: 6 dimensions with monthly comparison | Monthly |
| Contract alerts: list of contracts expiring within next 60 days | Monthly |
| PDPL risk review: Source Passports and retention periods | Monthly |
| Contract renewal communication drafts (DRAFT_ONLY) | As needed, with logged approval |
| Monthly review session (45 minutes) | Monthly |
| Proof Pack update | Quarterly |

---

## القيمة المُلاحَظة — Observed Value (Estimated, not verified)

| المقياس | الوضع قبل السبرنت | الوضع بعد السبرنت (تقديري) | التصنيف |
|---|---|---|---|
| تنسيقات فواتير لا تستوفي ZATCA | 3 | 0 (بعد التصحيح) | موثَّق (التحديد) / تقديري (التصحيح) |
| عقود منتهية غير متابَعة | غير معروفة | 8 مُحدَّدة | موثَّق |
| القيمة التقديرية للعقود المتروكة | غير معروفة | 47,000 ريال/سنة | مُقدَّر |
| مخاطرة ZATCA على التحصيل | قائمة | مُعالَجة (مؤشر) | موثَّق (التحديد) |

**هذه الأرقام تصف ما وجده السبرنت ووثّقه. لا تُمثّل ضمانات بنتائج تحصيل أو تجديد عقود.**

---

## حدود هذه الحالة — Limitations

- دراسة حالة توضيحية مُركَّبة — غير مرتبطة بعميل حقيقي مُحدد.
- تصحيح تنسيقات ZATCA مسؤولية تقنية تقع على عاتق الشركة ومزوّد ERP — لا يُنفّذ Dealix تعديلات على الأنظمة مباشرةً.
- تجديد العقود الـ 6 نمط مُستهدف لا نتيجة مضمونة — يعتمد على استجابة العملاء.
- قيمة 47,000 ريال تقدير داخلي لا قياس سوق مستقل.

- Composite illustrative case study — not tied to a specific real client.
- ZATCA format correction is a technical responsibility of the company and ERP provider — Dealix does not directly modify client systems.
- 6 contract renewals is a target pattern, not a guaranteed outcome — depends on client response.
- SAR 47,000 value is an internal estimate, not an independent market measurement.

---

روابط ذات صلة: [CASE_STUDY_TECHNOLOGY_COMPANY_AR.md](./CASE_STUDY_TECHNOLOGY_COMPANY_AR.md) | [case_001_anonymized.md](./case_001_anonymized.md) | [PRODUCT_SPEC_MANAGED_OPS.md](../product/PRODUCT_SPEC_MANAGED_OPS.md)

---

**القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.**
