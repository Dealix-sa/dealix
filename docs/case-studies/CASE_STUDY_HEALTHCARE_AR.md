# دراسة حالة — شركة تقنية رعاية صحية سعودية (توضيحية)
# Case Study — Saudi Healthcare Technology Company (Illustrative)

> **دراسة حالة توضيحية — لا تمثّل عميلاً محدداً**
> **Illustrative case study — does not represent a specific client**
>
> هذه دراسة حالة توضيحية مُركَّبة. لا تُشير إلى عميل حقيقي بعينه. جميع الأرقام والسيناريوهات والشركة الموصوفة افتراضية، مُصمَّمة لتمثيل أنماط منهجية نموذجية يُتوقَّع مواجهتها في قطاع تقنية الرعاية الصحية السعودي. الأسماء والتفاصيل التعريفية محذوفة أو مُخترَعة. تقدير غير مضمون / Estimated, not guaranteed.
>
> This is a composite illustrative case study. It does not refer to any specific real client. All figures, scenarios, and the described company are hypothetical, designed to represent typical methodological patterns expected in Saudi healthcare technology sector engagements. Names and identifying details are removed or invented. Estimated, not guaranteed / تقدير غير مضمون.

روابط: [SPRINT_DELIVERY_PLAYBOOK.md](../03_commercial_mvp/SPRINT_DELIVERY_PLAYBOOK.md) | [PROOF_PACK_STANDARD.md](../07_proof_os/PROOF_PACK_STANDARD.md) | [CASE_STUDY_TECHNOLOGY_COMPANY_AR.md](./CASE_STUDY_TECHNOLOGY_COMPANY_AR.md) | [CASE_STUDY_FINANCIAL_AR.md](./CASE_STUDY_FINANCIAL_AR.md)

---

## ملف الشركة — Company Profile

| الخاصية | التفاصيل |
|---|---|
| القطاع | تقنية الرعاية الصحية B2B / B2B Healthcare Technology |
| الاسم المُجهَّل | شركة ميد-تك السعودية (افتراضية — لا علاقة بكيان حقيقي) |
| الحجم | 25 موظفاً |
| الموقع | الرياض |
| الإيراد السنوي | 8 مليون ريال (افتراضي) |
| نوع العمل | برمجيات إدارة مرافق الرعاية الصحية، مبيعات B2B للمستشفيات والعيادات |
| التصنيف | توضيحي — لا اسم حقيقي، لا أرقام فعلية |

---

## التحدي — The Challenge

**بالعربية:**

واجهت الشركة التوضيحية أربعة تحديات متشابكة في وقت واحد، ما جعل التعامل مع أي منها بمعزل عن البقية غير فعّال:

**التحدي الأول — فجوة PDPL في بيانات المرضى:**
تُعالِج الشركة بيانات تعريف المرضى (أسماء، أرقام هوية، سجلات علاجية مجمَّعة) ضمن منتجها البرمجي. لم تكن هناك وثيقة رسمية تُحدد الأساس القانوني لمعالجة هذه البيانات وفق المادة الثامنة من نظام PDPL. كذلك لم تكن هناك سياسة موثَّقة لموافقة المريض تنعكس في واجهة المنتج، ولا جدول احتفاظ مُعتمَد يُحدد متى تُحذف البيانات.

**التحدي الثاني — ZATCA المرحلة الثانية غير مُطبَّقة:**
الشركة تُصدر فواتير شهرية لمستشفيات وعيادات خاصة. اكتُشف خلال التشخيص أن تنسيق QR Code في الفاتورة الإلكترونية لا يتوافق مع متطلبات حقل TLV المُحدَّد في وثيقة متطلبات ZATCA. هذا يعني أن أي فاتورة مُرسَلة عبر Fatoora معرَّضة للرفض.

**التحدي الثالث — ثلاثة مصادر بيانات منفصلة:**
بيانات العملاء (المستشفيات والعيادات) موزَّعة بين: نظام CRM، جداول Excel في إدارة المشاريع، وتصدير مالي من برنامج المحاسبة. لا يوجد تعريف موحَّد لـ "العميل" عبر المصادر الثلاثة، مما يجعل أي تقرير شهري تجميعاً يدوياً يستغرق 8 ساعات من وقت المؤسس.

**التحدي الرابع — التقارير اليدوية تستنزف وقت المؤسس:**
المؤسس كان يُنفق ما يُقدَّر بـ 8 ساعات أسبوعياً في جمع بيانات من المصادر الثلاثة وإعداد تقرير واحد لمجلس الإدارة. هذا الوقت مأخوذ من اجتماعات العملاء والتطوير الاستراتيجي.

**In English:**

The illustrative company faced four interlinked challenges simultaneously, making addressing any single one in isolation ineffective:

**Challenge 1 — PDPL Gap in Patient Data:**
The company processes patient identification data (names, ID numbers, aggregated treatment records) within its software product. There was no formal document specifying the legal basis for processing under Article 8 of the PDPL regulations. There was also no documented patient consent policy reflected in the product interface, and no approved retention schedule specifying when data must be deleted.

**Challenge 2 — ZATCA Phase 2 Not Implemented:**
The company issues monthly invoices to hospitals and private clinics. The diagnostic revealed that the QR Code format in the e-invoice did not conform to the TLV field requirements specified in the ZATCA requirements document. This means any invoice submitted through Fatoora would be subject to rejection.

**Challenge 3 — Three Disconnected Data Sources:**
Customer data (hospitals and clinics) is distributed across: a CRM system, Excel sheets in project management, and a financial export from the accounting software. There is no unified definition of "customer" across the three sources, making any monthly report a manual 8-hour compilation task for the founder.

**Challenge 4 — Manual Reporting Consuming Founder Time:**
The founder was spending an estimated 8 hours per week collecting data from the three sources and preparing a single board report. This time was taken from client meetings and strategic development.

---

## مسار التعاق — Engagement Path

**بالعربية:**

رحلة التعامل سارت عبر السلم الرباعي خلال 90 يوماً:

| المرحلة | الخدمة | السعر | المدة |
|---|---|---|---|
| 1 | التشخيص المجاني (Free Diagnostic) | مجاني | 3 أيام |
| 2 | Sprint (المسح السريع) | 499 ريال | 7 أيام |
| 3 | Data Pack (حزمة البيانات) | 1,500 ريال | 14 يوماً |
| 4 | Managed Ops Professional | 3,999 ريال/شهر | مستمر |

التشخيص المجاني أنتج نتائج أولية في ثلاثة محاور: مخاطر PDPL محددة، وفجوات ZATCA محددة، وتقدير تسريب الإيرادات الأولي. هذه النتائج هي ما دفعت المؤسس إلى الموافقة على Sprint.

**In English:**

The engagement path followed the four-level ladder over 90 days:

| Stage | Service | Price | Duration |
|---|---|---|---|
| 1 | Free Diagnostic | Free | 3 days |
| 2 | Sprint | SAR 499 | 7 days |
| 3 | Data Pack | SAR 1,500 | 14 days |
| 4 | Managed Ops Professional | SAR 3,999/month | Ongoing |

The Free Diagnostic produced initial findings across three axes: PDPL risks identified, ZATCA gaps identified, and initial revenue leakage estimate. These findings prompted the founder to approve the Sprint.

---

## نتائج السبرنت — Sprint Findings (توضيحية / Illustrative)

**بالعربية:**

### درجة جودة البيانات (DQ Score)

قبل التدخل: **55/100** — بعد 7 أيام: **72/100**

الأبعاد الضعيفة في القياس الأولي:
- **الاكتمال:** 38% من سجلات العملاء تفتقر إلى معرّف قانوني موحَّد (السجل التجاري للمستشفى أو رقم الترخيص الصحي)
- **التفرد:** 12% تكرار في سجلات الفروع (فروع العيادات سُجّلت كعملاء مستقلين بدون ربط بالكيان الأم)
- **المطابقة:** تنسيقات أرقام الهواتف والبريد الإلكتروني غير موحَّدة عبر المصادر الثلاثة

### نتائج PDPL (توضيحية)

تُشير الفجوتان المُحددتان:
1. **فجوة موافقة المريض:** البيانات المُجمَّعة المُعالَجة لا تحمل توثيقاً صريحاً لأساس قانوني المعالجة وفق المادة الثامنة من PDPL. لا تُمثّل هذه المخاطرة استنتاجاً قانونياً نهائياً — وينبغي إحالتها إلى مستشار قانوني مختص.
2. **فجوة سياسة الاحتفاظ:** لا توجد جداول احتفاظ رسمية مُعتمَدة تُحدد متى تُحذف فئات بيانات المرضى. هذه الفجوة مُسجَّلة في تقرير مخاطر PDPL ضمن Proof Pack.

### نتائج ZATCA (توضيحية)

**مشكلة QR Code:** تنسيق QR Code في الفاتورة الإلكترونية يُولِّد قيمة TLV لا تُطابق مخطط التحقق في وثيقة متطلبات ZATCA الإصدار 3.x. النتيجة: أي فاتورة مُرسَلة عبر Fatoora خلال الفترة الحالية معرَّضة للرفض.

### تقدير تسريب الإيرادات (توضيحي)

| المصدر | التقدير الشهري |
|---|---|
| عقود تجديد لم تُتابَع (5 عقود مُحددة) | 11,000 ريال/شهر |
| فواتير مرفوضة من ZATCA (تقدير بناء على حجم الفواتير) | 8,000 ريال/شهر |
| وقت المؤسس في تقارير يدوية (تكلفة فرصة) | ~0 ريال — مُحسوب كوقت، لا نقداً |
| **الإجمالي التقديري** | **19,000 ريال/شهر** |

جميع هذه الأرقام تقديرية. تقدير غير مضمون / Estimated, not guaranteed.

**In English:**

### Data Quality Score (DQ Score)

Before engagement: **55/100** — After 7 days: **72/100**

Weak dimensions in the initial measurement:
- **Completeness:** 38% of customer records lacking a unified legal identifier (hospital commercial registration or health license number)
- **Uniqueness:** 12% duplication in branch records (clinic branches registered as independent customers without linking to the parent entity)
- **Conformance:** Phone number and email formats inconsistent across the three sources

### PDPL Findings (Illustrative)

Two identified gaps:
1. **Patient consent gap:** Aggregated data being processed lacks explicit documentation of legal processing basis under Article 8 of PDPL. This risk does not constitute a final legal conclusion — it should be referred to qualified legal counsel.
2. **Retention policy gap:** No formally approved retention schedules specify when patient data categories must be deleted. This gap is logged in the PDPL risk report within the Proof Pack.

### ZATCA Findings (Illustrative)

**QR Code issue:** The QR Code format in the e-invoice generates a TLV value that does not match the validation schema in the ZATCA requirements document version 3.x. Result: any invoice submitted through Fatoora during the current period is subject to rejection.

### Revenue Leakage Estimate (Illustrative)

| Source | Monthly Estimate |
|---|---|
| Untracked renewal contracts (5 identified contracts) | SAR 11,000/month |
| ZATCA-rejected invoices (estimate based on invoice volume) | SAR 8,000/month |
| Founder time in manual reporting (opportunity cost) | ~SAR 0 — counted as time, not cash |
| **Total Estimate** | **SAR 19,000/month** |

All figures are estimates. Estimated, not guaranteed / تقدير غير مضمون.

---

## نتائج Managed Ops بعد 90 يوماً — Managed Ops Results After 90 Days (توضيحية / Illustrative)

**بالعربية:**

بعد الانتقال إلى Managed Ops Professional وتجاوز 90 يوماً من التشغيل المستمر، القياسات التوضيحية التالية تُمثّل نمط التحسن المتوقع:

| المقياس | قبل التدخل | بعد 90 يوماً | الفئة |
|---|---|---|---|
| درجة جودة البيانات (DQ Score) | 55/100 | 83/100 | تقدير |
| درجة امتثال PDPL | 45/100 | 78/100 | تقدير |
| جاهزية ZATCA | 62/100 | 94/100 | تقدير |
| وقت المؤسس في التقارير | 8 ساعات/أسبوع | 1 ساعة/أسبوع | تقدير |
| عقود غير مُتابَعة مُكتشَفة | 0 | 5 (موثَّقة) | موثَّق |
| قرارات APPROVAL_FIRST مُسجَّلة | — | 34 قرار | موثَّق |

**ملاحظة الفئة:** القياسات المُصنَّفة "تقدير" مُستَخرَجة من منهجية الحساب الداخلية لـ Dealix ولم تُتحقَّق بمصادر خارجية مستقلة. القياسات "موثَّقة" تُشير إلى سجلات عمل مباشرة.

**In English:**

After transitioning to Managed Ops Professional and completing 90 days of continuous operation, the following illustrative measurements represent the expected improvement pattern:

| Metric | Before Engagement | After 90 Days | Category |
|---|---|---|---|
| Data Quality Score (DQ Score) | 55/100 | 83/100 | Estimate |
| PDPL Compliance Score | 45/100 | 78/100 | Estimate |
| ZATCA Readiness | 62/100 | 94/100 | Estimate |
| Founder reporting time | 8 hours/week | 1 hour/week | Estimate |
| Untracked contracts discovered | 0 | 5 (documented) | Documented |
| APPROVAL_FIRST decisions logged | — | 34 decisions | Documented |

**Category note:** Measurements classified as "estimate" are derived from Dealix's internal calculation methodology and have not been verified by independent external sources. "Documented" measurements refer to direct work logs.

---

## مقتطف من حزمة الإثبات — Proof Pack Excerpt (توضيحي / Illustrative)

**بالعربية:**

المقتطف التالي يُمثّل هيكل قسم "القيمة المُلاحَظة" من Proof Pack — هذا نموذج توضيحي، ليس وثيقة فعلية:

```json
{
  "proof_pack_id": "PP-HC-001-ILLUSTRATIVE",
  "client_label": "HealthTech_Anon_001",
  "sprint_period": "2025-Q4 (illustrative)",
  "dq_score_delta": {
    "before": 55,
    "after": 83,
    "classification": "estimate"
  },
  "pdpl_gaps_identified": 2,
  "zatca_gaps_resolved": 1,
  "governance_decisions_logged": 34,
  "revenue_leakage_estimate_sar_monthly": 19000,
  "claim_classification": "estimated_not_verified",
  "disclaimer": "القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value"
}
```

**In English:**

The following excerpt represents the structure of the "Observed Value" section of a Proof Pack — this is an illustrative template, not an actual document:

*(See JSON schema above — identical structure applies in English output.)*

---

## ماذا لم تفعل Dealix — What Dealix Did NOT Do

**بالعربية:**

الوضوح حول ما لم يُنجَز بنفس أهمية ما أُنجز:

- **لم تُجرِ Dealix أي تواصل بارد مع عملاء المستشفيات:** كل إجراء تواصل مع أطراف خارجية كان يستلزم موافقة صريحة مُسبَقة من المؤسس وفق بروتوكول APPROVAL_FIRST.
- **لم تُصدر Dealix أي ادعاء بأرقام مبيعات مضمونة:** جميع التقديرات مُصنَّفة صراحةً كتقديرات في Proof Pack.
- **لم تصل Dealix إلى بيانات المرضى الفردية:** المعالجة اقتصرت على بيانات العملاء المؤسسية (المستشفيات والعيادات كمؤسسات)، لا السجلات الصحية الفردية.
- **لم تُرسِل Dealix رسائل WhatsApp جماعية أو أتمتة LinkedIn:** لا يُقدَّم هذا كخدمة.
- **لا يُغني Managed Ops عن المستشار القانوني:** نتائج PDPL المُسجَّلة مُقدَّمة كمؤشرات منهجية، لا كاستنتاجات قانونية نهائية.

**In English:**

Clarity about what was not done is as important as what was:

- **Dealix did not conduct any cold outreach to hospital clients:** every external communication action required explicit prior approval from the founder under the APPROVAL_FIRST protocol.
- **Dealix did not issue any guaranteed sales number claims:** all estimates are explicitly classified as estimates in the Proof Pack.
- **Dealix did not access individual patient data:** processing was limited to institutional customer data (hospitals and clinics as organizations), not individual health records.
- **Dealix did not send bulk WhatsApp messages or LinkedIn automation:** this is not an offered service.
- **Managed Ops does not substitute for legal counsel:** PDPL findings logged are presented as methodological indicators, not final legal conclusions.

---

## الخطوات التالية — Next Steps

**بالعربية:**

بناءً على Proof Score المُسجَّل بعد 90 يوماً، يدرس المؤسس التوضيحي الانتقال إلى المستوى الخامس: **Custom AI لتحليل مسارات المرضى** داخل منتجه البرمجي. هذا التطوير سيُنفَّذ فقط بعد:

1. تأكيد اكتمال معالجة فجوات PDPL المُحددة (بما في ذلك مراجعة المستشار القانوني).
2. الحصول على موافقة صريحة من مجلس الإدارة على نطاق معالجة بيانات المرضى المُقترح.
3. وضع ضمانات PDPL في معمارية نموذج Custom AI قبل التشغيل.

لا يُطلَق Custom AI ما لم تكتمل هذه الشروط الثلاثة. هذا تطبيق مباشر لمبدأ APPROVAL_FIRST على مستوى المنتج.

**In English:**

Based on the Proof Score logged after 90 days, the illustrative founder is evaluating transition to Level 5: **Custom AI for patient pathway analytics** within the software product. This development would be executed only after:

1. Confirming resolution of the identified PDPL gaps (including legal counsel review).
2. Obtaining explicit board approval on the proposed patient data processing scope.
3. Embedding PDPL safeguards in the Custom AI model architecture before any operation.

Custom AI is not launched unless all three conditions are met. This is a direct application of the APPROVAL_FIRST principle at the product level.

---

## حدود هذه الحالة — Limitations

- دراسة حالة توضيحية مُركَّبة — غير مرتبطة بعميل حقيقي مُحدد.
- أرقام التسريب والتحسين مبنية على أنماط منهجية توضيحية، لا قياسات سوق مستقلة.
- درجات الامتثال (PDPL، ZATCA) تعكس منهجية Dealix الداخلية — لا تُمثّل شهادة امتثال رسمية من الجهات التنظيمية.
- التحويل من مستوى إلى آخر قرار فردي — لا يُمثّل نمطاً مضموناً.
- نتائج PDPL المُدرَجة لأغراض إيضاحية — لا تُغني عن المراجعة القانونية المتخصصة.

- Composite illustrative case study — not tied to a specific real client.
- Leakage and improvement figures are based on illustrative methodological patterns, not independent market measurements.
- Compliance scores (PDPL, ZATCA) reflect Dealix's internal methodology — they do not constitute official compliance certification from regulatory bodies.
- Tier conversion is an individual decision — it does not represent a guaranteed pattern.
- PDPL findings included for illustrative purposes — they do not substitute for specialized legal review.

---

روابط ذات صلة: [CASE_STUDY_TECHNOLOGY_COMPANY_AR.md](./CASE_STUDY_TECHNOLOGY_COMPANY_AR.md) | [CASE_STUDY_LOGISTICS_AR.md](./CASE_STUDY_LOGISTICS_AR.md) | [CASE_STUDY_FINANCIAL_AR.md](./CASE_STUDY_FINANCIAL_AR.md) | [../04_data_os/ALLOWED_USE_POLICY.md](../04_data_os/ALLOWED_USE_POLICY.md)

---

**القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.**
