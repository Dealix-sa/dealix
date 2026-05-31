# دراسة حالة — شركة خدمات مالية سعودية (توضيحية)
# Case Study — Saudi Financial Services Company (Illustrative)

> **دراسة حالة توضيحية — لا تمثّل عميلاً محدداً**
> **Illustrative case study — does not represent a specific client**
>
> هذه دراسة حالة توضيحية مُركَّبة. لا تُشير إلى عميل حقيقي بعينه. جميع الأرقام والسيناريوهات والشركة الموصوفة افتراضية، مُصمَّمة لتمثيل أنماط منهجية نموذجية يُتوقَّع مواجهتها في قطاع الخدمات المالية والتقنية المالية السعودي. الأسماء والتفاصيل التعريفية محذوفة أو مُخترَعة. تقدير غير مضمون / Estimated, not guaranteed.
>
> This is a composite illustrative case study. It does not refer to any specific real client. All figures, scenarios, and the described company are hypothetical, designed to represent typical methodological patterns expected in Saudi financial services and fintech sector engagements. Names and identifying details are removed or invented. Estimated, not guaranteed / تقدير غير مضمون.

روابط: [SPRINT_DELIVERY_PLAYBOOK.md](../03_commercial_mvp/SPRINT_DELIVERY_PLAYBOOK.md) | [PROOF_PACK_STANDARD.md](../07_proof_os/PROOF_PACK_STANDARD.md) | [CASE_STUDY_HEALTHCARE_AR.md](./CASE_STUDY_HEALTHCARE_AR.md) | [CASE_STUDY_TECHNOLOGY_COMPANY_AR.md](./CASE_STUDY_TECHNOLOGY_COMPANY_AR.md)

---

## ملف الشركة — Company Profile

| الخاصية | التفاصيل |
|---|---|
| القطاع | خدمات مالية / تقنية مالية B2B / B2B Financial Services / Fintech |
| الاسم المُجهَّل | شركة فين-أوبس السعودية (افتراضية — لا علاقة بكيان حقيقي) |
| الحجم | 45 موظفاً |
| الموقع | الرياض |
| الإيراد السنوي | 22 مليون ريال (افتراضي) |
| نوع العمل | حلول إدارة المدفوعات والفوترة للمؤسسات، عقود B2B سنوية |
| التصنيف | توضيحي — لا اسم حقيقي، لا أرقام فعلية |

---

## التحدي — The Challenge

**بالعربية:**

تُواجه الشركة التوضيحية أربعة تحديات مترابطة، كل منها قائم بذاته لكن مُتضخِّم بالبقية:

**التحدي الأول — رفض ZATCA للفواتير الإلكترونية:**
بدأت المشكلة عندما أبلغ قسم المالية عن رفض متكرر لفواتير من منظومة Fatoora. التحقيق الداخلي كشف ثلاثة أسباب متداخلة: الختم الرقمي غائب أو بتنسيق غير صحيح، تنسيق رقم التسجيل الضريبي (TRN) يحتوي على أخطاء نمطية في حالات معينة، وملف XML للفاتورة لا يُجتاز فحص التحقق (XML Validation) من الإصدار الأحدث لوثيقة متطلبات ZATCA. كل فاتورة مرفوضة تعني تأخيراً في التحصيل وخطر غرامة.

**التحدي الثاني — سؤال المادة السادسة من PDPL:**
الشركة تُعالِج بيانات مالية لعملاء مؤسسات، بعضها يتضمن سجلات معاملات تندرج ضمن تعريف "البيانات المالية الحساسة" وفق اللوائح التنفيذية لـ PDPL. الإدارة لم تكن متيقنة إن كانت ضوابط معالجة هذه البيانات تُوثِّق صراحةً ما تُبيحه المادة السادسة كأساس قانوني للمعالجة. هذه ليست نتيجة قانونية — هي مؤشر يحتاج إلى مراجعة مستشار قانوني.

**التحدي الثالث — جودة بيانات CRM بنسبة 48% فقط:**
أربعة مصادر بيانات عملاء منفصلة تُغذّي قرارات المبيعات: نظام CRM الرئيسي، جداول Excel لإدارة الحسابات، تصدير من منصة الفوترة، وسجل بريد إلكتروني من نظام المتابعة. التداخل بين هذه المصادر أنتج معدل تكرار مُقدَّر بـ 23% في سجلات العملاء، وجودة بيانات إجمالية بـ 48/100 — مما يجعل أولوية قائمة المبيعات تقديراً شخصياً لا قراراً مُستنداً إلى بيانات.

**التحدي الرابع — ثلاثة تقارير يدوية أسبوعية:**
فريق القيادة يتلقى ثلاثة تقارير Excel أسبوعية (مبيعات، تدفق نقدي، مؤشرات عمليات) يُعدَّها ثلاثة أشخاص مختلفون من مصادر غير مُوحَّدة. التقارير الثلاثة كثيراً ما تحتوي على أرقام متعارضة لنفس المقياس بسبب تعريفات حساب مختلفة.

**In English:**

The illustrative company faces four interlinked challenges, each standalone but amplified by the others:

**Challenge 1 — ZATCA Invoice Rejections:**
The problem began when the finance department reported repeated rejections from the Fatoora platform. Internal investigation revealed three overlapping causes: the digital stamp is absent or in an incorrect format, the Tax Registration Number (TRN) format contains pattern errors in certain cases, and the invoice XML file fails the validation check against the latest version of the ZATCA requirements document. Every rejected invoice means a collection delay and penalty risk.

**Challenge 2 — PDPL Article 6 Data Processing Question:**
The company processes financial data for institutional clients, some of which includes transaction records that fall under the definition of "sensitive financial data" under PDPL executive regulations. Management was uncertain whether the controls for processing this data explicitly documented what Article 6 permits as a legal basis for processing. This is not a legal conclusion — it is an indicator requiring legal counsel review.

**Challenge 3 — CRM Data Quality at 48% Only:**
Four separate customer data sources feed sales decisions: the main CRM system, Excel sheets for account management, an export from the invoicing platform, and an email log from the follow-up system. Overlap between these sources produced an estimated 23% duplication rate in customer records, and overall data quality of 48/100 — making sales list prioritization a personal judgment rather than a data-grounded decision.

**Challenge 4 — Three Weekly Manual Reports:**
The leadership team receives three weekly Excel reports (sales, cash flow, operations metrics) prepared by three different people from non-unified sources. All three reports frequently contain conflicting numbers for the same metric due to different calculation definitions.

---

## مسار التعاقد — Engagement Path

**بالعربية:**

الشركة دخلت مباشرة عبر Sprint دون مرحلة تشخيص مجاني، بناءً على إحالة من شريك أعمال:

| المرحلة | الخدمة | السعر | المدة |
|---|---|---|---|
| 1 | Sprint (المسح السريع) | 499 ريال | 7 أيام |
| 2 | Data Pack (حزمة البيانات) | 1,500 ريال | 14 يوماً |
| 3 | Managed Ops Enterprise | 4,999 ريال/شهر | مستمر (6 أشهر موثَّقة) |

**In English:**

The company entered directly via Sprint without a Free Diagnostic stage, based on a business partner referral:

| Stage | Service | Price | Duration |
|---|---|---|---|
| 1 | Sprint | SAR 499 | 7 days |
| 2 | Data Pack | SAR 1,500 | 14 days |
| 3 | Managed Ops Enterprise | SAR 4,999/month | Ongoing (6 months documented) |

---

## نتائج السبرنت — Sprint Findings (الأسبوع الأول / توضيحية)

**بالعربية:**

### درجة جودة البيانات

قبل التدخل: **48/100** — نهاية الأسبوع الأول: **71/100**

مصادر الضعف المُحددة:
- **التفرد:** 23% تكرار في سجلات العملاء عبر المصادر الأربعة (643 سجلاً فريداً مُستخرَجاً من 837 سجلاً إجمالياً)
- **الاكتمال:** 41% من سجلات CRM تفتقر إلى تاريخ آخر تواصل موثَّق
- **الصلاحية:** 17% من أرقام TRN في قاعدة عملاء CRM لا تُجتاز فحص التنسيق القياسي

### فجوات ZATCA المُحددة (5 فجوات)

| رقم | الفجوة | التصنيف |
|---|---|---|
| 1 | الختم الرقمي (Digital Stamp) غائب من 34% من الفواتير المُختبَرة | حرجة |
| 2 | تنسيق TRN يحتوي على أخطاء نمطية في حالات معينة | حرجة |
| 3 | ملف XML لا يُجتاز فحص التحقق للإصدار 3.x | حرجة |
| 4 | حقل تاريخ الفاتورة لا يُتابع منطقة التوقيت السعودية (UTC+3) | متوسطة |
| 5 | حقل وصف السلعة/الخدمة يتجاوز الحد الأقصى للأحرف في حالات معينة | منخفضة |

### تقدير التعرض لغرامات ZATCA (توضيحي)

بناءً على حجم الفواتير اليومي وفترة عدم الامتثال المُقدَّرة، وبتطبيق جدول غرامات ZATCA المعلن:

**التقدير الإجمالي للتعرض: 37,500 ريال** (تقدير توضيحي، غير مضمون)

هذا الرقم مبني على نمط عينة من الفواتير المُختبَرة، لا على مراجعة قانونية شاملة لجميع الفواتير المُصدَرة.

**In English:**

### Data Quality Score

Before engagement: **48/100** — End of week 1: **71/100**

Identified weakness sources:
- **Uniqueness:** 23% duplication in customer records across four sources (643 unique records extracted from 837 total records)
- **Completeness:** 41% of CRM records lack a documented last-contact date
- **Validity:** 17% of TRN numbers in the CRM customer base fail the standard format check

### ZATCA Gaps Identified (5 Gaps)

| No. | Gap | Classification |
|---|---|---|
| 1 | Digital Stamp absent from 34% of invoices tested | Critical |
| 2 | TRN format contains pattern errors in certain cases | Critical |
| 3 | XML file fails validation check for version 3.x | Critical |
| 4 | Invoice date field does not follow Saudi time zone (UTC+3) | Medium |
| 5 | Item/service description field exceeds maximum character limit in certain cases | Low |

### ZATCA Penalty Exposure Estimate (Illustrative)

Based on daily invoice volume and estimated non-compliance period, applying the published ZATCA penalty schedule:

**Total exposure estimate: SAR 37,500** (illustrative estimate, not guaranteed)

This figure is based on a sample pattern from tested invoices, not a comprehensive legal review of all issued invoices.

---

## نتائج Managed Ops بعد 6 أشهر — Managed Ops Results After 6 Months (توضيحية / Illustrative)

**بالعربية:**

| المقياس | قبل التدخل | بعد 6 أشهر | الفئة |
|---|---|---|---|
| درجة جودة البيانات (DQ Score) | 48/100 | 89/100 | تقدير |
| جاهزية ZATCA | 52/100 | 98/100 | تقدير |
| توافق PDPL | 41/100 | 76/100 | تقدير |
| تكرار سجلات العملاء | 23% | أقل من 3% | تقدير |
| التقارير اليدوية الأسبوعية | 3 تقارير يدوية | صفر — مُؤتمتة عبر Proof Pack | موثَّق |
| إيرادات محمية من غرامات ZATCA | — | 37,500 ريال (تقدير) | تقدير |
| قرارات APPROVAL_FIRST مُسجَّلة | — | 67 قراراً في 6 أشهر | موثَّق |

**ملاحظة الفئة:** درجات الامتثال تعكس منهجية Dealix الداخلية ولم تُتحقَّق من جهة تنظيمية مستقلة. "موثَّق" يُشير إلى سجلات عمل مباشرة في سجل القرارات.

**In English:**

| Metric | Before Engagement | After 6 Months | Category |
|---|---|---|---|
| Data Quality Score (DQ Score) | 48/100 | 89/100 | Estimate |
| ZATCA Readiness | 52/100 | 98/100 | Estimate |
| PDPL Alignment | 41/100 | 76/100 | Estimate |
| Customer record duplication | 23% | Below 3% | Estimate |
| Weekly manual reports | 3 manual reports | Zero — automated via Proof Pack | Documented |
| Revenue protected from ZATCA penalties | — | SAR 37,500 (estimate) | Estimate |
| APPROVAL_FIRST decisions logged | — | 67 decisions in 6 months | Documented |

**Category note:** Compliance scores reflect Dealix's internal methodology and have not been verified by an independent regulatory body. "Documented" refers to direct work logs in the decision registry.

---

## أبرز الحوكمة — Governance Highlights

**بالعربية:**

الإبراز المُميَّز لهذه الحالة التوضيحية هو كثافة تطبيق APPROVAL_FIRST في قطاع الخدمات المالية، حيث كل إجراء خارجي له ثقل قانوني أعلى:

**67 قرار APPROVAL_FIRST خلال 6 أشهر — تصنيف القرارات:**

| نوع القرار | العدد | الوصف |
|---|---|---|
| DRAFT_ONLY | 38 | مسودات تواصل مُنتَجة بدون إرسال تلقائي — في انتظار موافقة مالك سير العمل |
| REQUIRE_APPROVAL | 18 | إجراءات خارجية موقوفة حتى تأكيد صريح — شملت مراسلات مع عملاء وتحديثات فواتير |
| BLOCK | 7 | رفض كامل — 4 حالات تضمنت ادعاءات غير مصدرية، 3 حالات اقترحت بيانات قد تُعرِّض الشركة لمخاطر PDPL |
| REDACT | 4 | إزالة بيانات شخصية من مخرجات قبل عرضها على مالك سير العمل |

كل قرار مُسجَّل في سجل القرارات (Governance Decision Log) مع: نوع القرار، المُبرر، الطابع الزمني، معرّف مالك سير العمل.

**In English:**

The distinguishing highlight of this illustrative case is the density of APPROVAL_FIRST application in the financial services sector, where every external action carries higher legal weight:

**67 APPROVAL_FIRST decisions over 6 months — decision classification:**

| Decision Type | Count | Description |
|---|---|---|
| DRAFT_ONLY | 38 | Communication drafts produced without automatic sending — awaiting workflow owner approval |
| REQUIRE_APPROVAL | 18 | External actions held pending explicit confirmation — included client correspondence and invoice updates |
| BLOCK | 7 | Full rejection — 4 cases contained unsourced claims, 3 cases proposed data that could expose the company to PDPL risks |
| REDACT | 4 | Personal data removed from outputs before presenting to workflow owner |

Every decision is logged in the Governance Decision Log with: decision type, rationale, timestamp, workflow owner identifier.

---

## ماذا لم تفعل Dealix — What Dealix Did NOT Do

**بالعربية:**

- **لم تصل Dealix إلى أي بيانات مصرفية أو بيانات حسابات عملاء:** النطاق اقتصر على بيانات CRM وبيانات الفوترة وسجلات العمليات التي وافق عليها مالك سير العمل صراحةً في جواز المصدر (Source Passport).
- **لم تُجرِ Dealix أي تنقيب على LinkedIn أو جمع بيانات من مصادر خارجية:** لا يُقدَّم هذا كخدمة.
- **لم تُصدر Dealix أي ادعاء بأرقام إيرادات مضمونة:** تقدير حماية 37,500 ريال من غرامات ZATCA هو تقدير توضيحي مبني على عينة — ليس ضماناً.
- **لم تُقدِّم Dealix استشارة قانونية بشأن PDPL أو ZATCA:** نتائج الامتثال مُقدَّمة كمؤشرات منهجية تحتاج إلى مراجعة مستشار قانوني ومحاسب ضريبي مرخَّص.
- **لم تُرسِل Dealix أي رسائل خارجية باسم الشركة دون موافقة:** كل قرار REQUIRE_APPROVAL يُوثِّق هذا صراحةً.

**In English:**

- **Dealix did not access any banking data or client account data:** scope was limited to CRM data, billing data, and operations records explicitly approved by the workflow owner in the Source Passport.
- **Dealix did not conduct any LinkedIn scraping or external data collection:** this is not an offered service.
- **Dealix did not issue any guaranteed revenue number claims:** the estimate of SAR 37,500 in ZATCA penalty protection is an illustrative sample-based estimate — not a guarantee.
- **Dealix did not provide legal advice on PDPL or ZATCA:** compliance findings are presented as methodological indicators requiring review by qualified legal counsel and a licensed tax advisor.
- **Dealix did not send any external messages on the company's behalf without approval:** every REQUIRE_APPROVAL decision documents this explicitly.

---

## الخطوات التالية — Next Steps

**بالعربية:**

بعد 6 أشهر من Managed Ops Enterprise مع Proof Score مُسجَّل أعلى من 85/100، تدرس الشركة التوضيحية الانتقال إلى المستوى الخامس: **Custom AI لإثراء بيانات مخاطر الائتمان** (Credit Risk Data Enrichment).

هذا المشروع في مرحلة التقييم فحسب، ويستلزم قبل أي قرار:
1. تحديد نطاق دقيق لبيانات المُستخدَمة وما يتضمنه من تعريفات PDPL.
2. مراجعة متطلبات هيئة سوق المال (CMA) على استخدامات نماذج AI في قرارات الائتمان.
3. موافقة مجلس الإدارة على النطاق المُحدَّد قبل بدء التطوير.

لا يُطلَق Custom AI في القطاع المالي دون مرور ثلاثة بوابات: PDPL، CMA، APPROVAL_FIRST على مستوى المنتج.

**In English:**

After 6 months of Managed Ops Enterprise with a Proof Score logged above 85/100, the illustrative company is evaluating transition to Level 5: **Custom AI for credit risk data enrichment**.

This project is in evaluation stage only, and requires before any decision:
1. Precise scoping of data to be used and its PDPL classification implications.
2. Review of Capital Market Authority (CMA) requirements on AI model use in credit decisions.
3. Board approval of the defined scope before development commences.

Custom AI is not launched in the financial sector without passing three gates: PDPL, CMA review, APPROVAL_FIRST at the product level.

---

## حدود هذه الحالة — Limitations

- دراسة حالة توضيحية مُركَّبة — غير مرتبطة بعميل حقيقي مُحدد.
- أرقام الغرامات والتحسين مبنية على أنماط منهجية توضيحية وعينة اختبار محدودة، لا مراجعة قانونية شاملة.
- درجات الامتثال (PDPL، ZATCA) تعكس منهجية Dealix الداخلية — لا تُمثّل شهادة امتثال رسمية من هيئة الزكاء والضريبة والجمارك أو الهيئة السعودية للبيانات والذكاء الاصطناعي.
- تقدير "حماية 37,500 ريال" مبني على عينة فواتير مُختبَرة، ليس على مراجعة قانونية كاملة لجميع الفواتير التاريخية.
- نتائج PDPL المُدرَجة لأغراض إيضاحية — لا تُغني عن المستشار القانوني ولا المحاسب الضريبي المرخَّص.

- Composite illustrative case study — not tied to a specific real client.
- Penalty and improvement figures are based on illustrative methodological patterns and a limited test sample, not a comprehensive legal review.
- Compliance scores (PDPL, ZATCA) reflect Dealix's internal methodology — they do not constitute official compliance certification from ZATCA or SDAIA.
- The estimate of "SAR 37,500 protected" is based on a sample of tested invoices, not a full legal review of all historical invoices.
- PDPL findings included for illustrative purposes — they do not substitute for qualified legal counsel or a licensed tax advisor.

---

روابط ذات صلة: [CASE_STUDY_TECHNOLOGY_COMPANY_AR.md](./CASE_STUDY_TECHNOLOGY_COMPANY_AR.md) | [CASE_STUDY_HEALTHCARE_AR.md](./CASE_STUDY_HEALTHCARE_AR.md) | [CASE_STUDY_LOGISTICS_AR.md](./CASE_STUDY_LOGISTICS_AR.md) | [../05_governance_os/GOVERNANCE_DECISION_TYPES.md](../05_governance_os/GOVERNANCE_DECISION_TYPES.md)

---

**القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.**
