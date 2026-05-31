# دراسة حالة — شركة تقنية سعودية B2B (مُجهَّلة الهوية)
# Case Study — Saudi B2B Technology Company (Anonymized)

> **دراسة حالة توضيحية — بناءً على نتائج Sprint نموذجية في قطاع التقنية**
> **Illustrative case study — based on typical Sprint findings in the technology sector**
>
> هذه دراسة حالة توضيحية مُركَّبة. لا تُشير إلى عميل حقيقي محدد. جميع الأرقام والسيناريوهات مبنية على أنماط منهجية نموذجية متوقعة في قطاع تقنية B2B السعودي. الأسماء والتفاصيل التعريفية محذوفة امتثالاً لنظام حماية البيانات الشخصية (PDPL).
>
> This is a composite illustrative case study. It does not refer to any specific real client. All figures and scenarios are based on typical methodological patterns expected in Saudi B2B technology sector engagements. Names and identifying details are removed in compliance with PDPL.

روابط: [SPRINT_DELIVERY_PLAYBOOK.md](../03_commercial_mvp/SPRINT_DELIVERY_PLAYBOOK.md) | [PROOF_PACK_STANDARD.md](../07_proof_os/PROOF_PACK_STANDARD.md) | [PRODUCT_SPEC_MANAGED_OPS.md](../product/PRODUCT_SPEC_MANAGED_OPS.md)

---

## ملف الشركة — Company Profile

| الخاصية | التفاصيل |
|---|---|
| القطاع | تقنية B2B — SaaS للمؤسسات / B2B Technology — Enterprise SaaS |
| الحجم | 85 موظفاً (تقدير) |
| الموقع | الرياض |
| نوع العمل | بيع مباشر للمؤسسات + عقود سنوية |
| التحدي الرئيسي | فجوة إيرادية مرئية في بيانات العملاء المحتملين وضعف تشغيل الإيرادات |
| التصنيف | مُجهَّل — لا اسم حقيقي، لا أرقام إيراد فعلية |

---

## المشكلة — The Problem

**بالعربية:**
الشركة كانت تعمل في سوق B2B SaaS للمؤسسات وتمتلك قاعدة عملاء محتملين في CRM تحتوي على أكثر من 400 سجل. المشكلة لم تكن نقص الفرص، بل غياب النظام الذي يُحدد أيّها يستحق الاهتمام الفوري.

ثلاثة أعراض محددة دفعت المؤسس لطلب السبرنت:

1. **جودة بيانات منخفضة:** تكرار حسابات، معلومات تواصل منتهية الصلاحية، غياب تحديد صانع القرار في أكثر من 40% من السجلات.
2. **غياب الأولوية:** فريق المبيعات يُخصّص وقتاً متساوياً لحسابات ذات احتمالية متباينة.
3. **مخاطر امتثال غير مُعالَجة:** بيانات شخصية مُخزَّنة دون جواز مصدر مُوقَّع — مخاطرة PDPL قائمة.

**In English:**
The company operated in enterprise B2B SaaS and held a CRM with over 400 prospect records. The problem was not a shortage of opportunities but the absence of a system to identify which warranted immediate attention.

Three specific symptoms prompted the founder to request the sprint:

1. **Low data quality:** duplicate accounts, expired contact information, missing decision-maker identification in over 40% of records.
2. **No prioritization:** the sales team allocated equal time to accounts with very different probability profiles.
3. **Unaddressed compliance risk:** personal data stored without a signed Source Passport — active PDPL exposure.

---

## رحلة الـ 7 أيام — The 7-Day Journey

**بالعربية:**

### اليوم الأول — تأهيل المصدر والمدخلات

قبل استيراد أي بيانات، وقّع مالك سير العمل من جانب العميل على جواز المصدر (Source Passport) المُحدَّد:
- المالك: العميل
- نوع المصدر: تصدير CRM
- الاستخدام المسموح به: السبرنت فقط
- علامة PII: نعم
- مدة الاحتفاظ: 90 يوماً

تم استيراد ملف CSV يحتوي على 412 سجلاً. لا عملية على البيانات قبل توقيع جواز المصدر — هذا شرط غير قابل للتفاوض (APPROVAL_FIRST).

### اليوم الثاني — قياس جودة البيانات

حُسِبت درجة جودة البيانات (DQ) عبر 6 أبعاد:
- **النتيجة الأولية: 61/100**
- الأبعاد الضعيفة: التفرد (18 حساباً مكرراً)، الاكتمال (35% من السجلات تفتقر إلى منصب صانع القرار)، المطابقة (تنسيقات أرقام الهواتف متضاربة)

### اليوم الثالث والرابع — تنظيف البيانات والتصنيف

- دُمجت الحسابات المكررة الـ 18 وفق قواعد دمج موثَّقة.
- صُنِّف الـ 394 حساباً المتبقية وفق 3 معايير شفافة: الملاءمة (Fit)، قوة الإشارة (Signal Strength)، مخاطر الحوكمة (Governance Risk).
- رُفعت درجة DQ بعد التنظيف إلى **78/100**.

### اليوم الخامس — مراجعة الحوكمة

أُجريت مراجعة الحوكمة وفق بروتوكول APPROVAL_FIRST. نتائج سجل الحوكمة:
- **قرارات مُسجَّلة:** 9
- **مسودات مُوقَّفة (BLOCK):** 2 — واحدة تضمنت ادعاءً بمعلومة غير مصدرية، وواحدة وعدت بنتيجة محددة مضمونة
- **مسودات تحتاج موافقة (REQUIRE_APPROVAL):** 3
- **مسودات تحتاج تنقية بيانات شخصية (REDACT):** 1
- **الباقي:** مُسلَّمة كمسودات فقط (DRAFT_ONLY) — لا إرسال تلقائي

**ثلاثة مصادر لتسريب الإيرادات تم تحديدها في اليوم الخامس:**
1. 8 عقود قابلة للتجديد لم تُتابَع — قيمة تقديرية 22,000 ريال في السنة.
2. 14 حساباً يمتلك تاريخ مشاركة حديثاً لكن لا خطوة تالية محددة.
3. فجوة تصنيف قطاعي تُعيق تخصيص الرسائل — جميع الحسابات تتلقى رسالة عامة واحدة.

### اليوم السادس — إعداد الحزمة

أُعِدَّت حزمة الإثبات (Proof Pack) بـ 14 قسماً. أُعِدَّت أيضاً مسودة عرض مسار العقد الشهري.

### اليوم السابع — تسليم حزمة الإثبات

تسليم Proof Pack كامل + جلسة مراجعة مع المؤسس.

**In English:**

### Day 1 — Source Qualification and Inputs

Before any data import, the client's workflow owner signed the defined Source Passport:
- Owner: client
- Source type: CRM export
- Allowed use: sprint only
- PII flag: yes
- Retention: 90 days

A CSV with 412 records was imported. No data processing before Source Passport signature — a non-negotiable requirement (APPROVAL_FIRST).

### Day 2 — Data Quality Measurement

Data Quality score (DQ) computed across 6 dimensions:
- **Initial score: 61/100**
- Weak dimensions: uniqueness (18 duplicate accounts), completeness (35% of records missing decision-maker title), conformance (inconsistent phone number formats)

### Days 3–4 — Data Cleaning and Scoring

- 18 duplicate accounts merged following documented merge rules.
- Remaining 394 accounts scored on 3 transparent criteria: Fit, Signal Strength, Governance Risk.
- DQ score after cleaning: **78/100**.

### Day 5 — Governance Review

Governance review conducted under the APPROVAL_FIRST protocol. Governance log results:
- **Decisions logged:** 9
- **Blocked drafts (BLOCK):** 2 — one contained an unsourced claim, one promised a guaranteed specific outcome
- **Approval-required drafts (REQUIRE_APPROVAL):** 3
- **Redaction-required drafts (REDACT):** 1
- **Remainder:** delivered as DRAFT_ONLY — no automatic sending

**Three revenue leakage sources identified on Day 5:**
1. 8 renewable contracts not tracked — estimated value 22,000 SAR annually.
2. 14 accounts with recent engagement history but no defined next step.
3. Sector classification gap preventing message targeting — all accounts receiving one generic message.

### Day 6 — Pack Preparation

Proof Pack assembled with 14 sections. Monthly retainer proposal prepared.

### Day 7 — Proof Pack Delivery

Full Proof Pack delivered with founder review session.

---

## مخرجات السبرنت — Sprint Outputs

**بالعربية:**

| المخرج | التفاصيل |
|---|---|
| درجة جودة البيانات الأولية | 61/100 |
| درجة جودة البيانات بعد التنظيف | 78/100 |
| حسابات مكررة دُمجت | 18 |
| مصادر تسريب إيرادات مُحددة | 3 |
| حسابات مُرتَّبة في قائمة الأفضل 10 | 10 |
| مسودات تواصل (عربي + إنجليزي) | 12 مسودة |
| مسودات اجتازت مراجعة الحوكمة | 6 (كمسودات فقط) |
| مسودات مُوقَّفة لمخالفة معايير الامتثال | 2 |
| درجة حزمة الإثبات (Proof Score) | 79/100 |
| أصول رأسمالية مُسجَّلة | 2 |

**In English:**

| Output | Detail |
|---|---|
| Initial data quality score | 61/100 |
| Post-cleaning data quality score | 78/100 |
| Duplicate accounts merged | 18 |
| Revenue leakage sources identified | 3 |
| Accounts in ranked top-10 list | 10 |
| Communication drafts (AR + EN) | 12 drafts |
| Drafts cleared governance review | 6 (as DRAFT_ONLY) |
| Drafts blocked for compliance failure | 2 |
| Proof Pack score | 79/100 |
| Capital assets registered | 2 |

---

## ردود الفعل التوضيحية للمؤسس — Illustrative Founder Reaction

> **ملاحظة:** هذه الاقتباسات افتراضية توضيحية تُمثّل نوع ردود الفعل المتوقع في هذا السيناريو. لا تُمثّل قولاً حرفياً لعميل حقيقي.
> **Note:** These quotes are illustrative hypotheticals representing the type of reaction expected in this scenario. They do not represent the literal words of a real client.

**بالعربية:**
"كنت أعتقد أن مشكلتنا في الإيرادات هي مشكلة مبيعات. لكن السبرنت أثبت أن المشكلة في البيانات أولاً — 18 حساباً مكرراً و8 عقود لم نتابعها كانت كافية لتغيير كيفية تفكيري في الأولويات."

**In English:**
"I thought our revenue problem was a sales problem. The sprint demonstrated it is a data problem first — 18 duplicate accounts and 8 untracked contracts were enough to change how I think about prioritization."

---

## الإجراءات الموصى بها — Recommended Actions

**بالعربية:**

| الأولوية | الإجراء | الأثر التقديري |
|---|---|---|
| عالية | متابعة 8 عقود قابلة للتجديد فوراً | 22,000 ريال قيمة تقديرية سنوياً |
| عالية | تفعيل الـ 14 حساباً ذات الإشارة الحديثة | فرص إيرادات مُثبتة بأدلة، غير مُقدَّرة |
| متوسطة | بناء تصنيف قطاعي لقاعدة الحسابات | تحسين معدل الاستجابة للرسائل (تقدير) |
| متوسطة | توثيق أساس قانوني لجميع بيانات PII | إزالة مخاطرة PDPL القائمة |

جميع الأرقام تقديرات. لا تُمثّل ضمانات بنتائج فعلية.

**In English:**

| Priority | Action | Estimated Impact |
|---|---|---|
| High | Follow up on 8 renewable contracts immediately | SAR 22,000 estimated annual value |
| High | Activate 14 accounts with recent signals | Evidenced revenue opportunities, not quantified |
| Medium | Build sector classification for account base | Estimated improvement in message response rate |
| Medium | Document lawful basis for all PII data | Removes active PDPL exposure |

All figures are estimates. They do not represent guarantees of actual outcomes.

---

## ماذا يتضمن Managed Ops لهذا العميل — What Managed Ops Includes for This Client

بعد Proof Score 79/100 وموافقة المؤسس، وقّع العميل على **Managed Ops Professional بسعر 3,999 ريال/شهر**.

**بالعربية — نطاق العقد الشهري:**

- مراقبة جودة البيانات شهرياً مع تقرير مقارن.
- تحديث قائمة الأولويات العشرة شهرياً وفق أحدث الإشارات.
- مراجعة حوكمة شهرية لجميع قرارات الإجراءات الخارجية (APPROVAL_FIRST محفوظ).
- مراقبة امتثال ZATCA: فحص شهري لصيغ الفواتير والربط مع Fatoora.
- تحديث حزمة الإثبات (Proof Pack) ربع سنوي.
- تقرير مخاطر PDPL شهري: مراجعة جوازات المصادر ومدد الاحتفاظ.
- لوحة تحكم صحة الإيرادات: 6 أبعاد مُحدَّثة شهرياً.
- جلسة مراجعة شهرية واحدة (60 دقيقة) مع مالك سير العمل.

**In English — Monthly Retainer Scope:**

- Monthly data quality monitoring with a comparative report.
- Monthly update of the top-10 priority list based on latest signals.
- Monthly governance review of all external action decisions (APPROVAL_FIRST maintained).
- ZATCA compliance monitoring: monthly check of invoice formats and Fatoora integration.
- Quarterly Proof Pack update.
- Monthly PDPL risk report: review of Source Passports and retention periods.
- Revenue Health Dashboard: 6 dimensions updated monthly.
- One monthly review session (60 minutes) with the workflow owner.

---

## القيمة المُلاحَظة — Observed Value (Estimated, not verified)

| المقياس | الوضع قبل السبرنت | الوضع بعد السبرنت | التصنيف |
|---|---|---|---|
| درجة جودة البيانات | 61/100 | 78/100 | مُقدَّر |
| حسابات مكررة | 18 | 0 | موثَّق |
| مصادر تسريب إيرادات مُعروفة | 0 | 3 | موثَّق |
| قيمة عقود غير مُتابَعة | غير معروفة | 22,000 ريال (تقدير) | مُقدَّر |
| مخاطرة PDPL غير مُعالَجة | قائمة | مُحددة وخُطِّط لمعالجتها | موثَّق |

**هذه الأرقام تصف ما أنتجه السبرنت من تحسينات داخلية. لا تُمثّل تحققاً من نتائج المبيعات أو تسارع في خط الأنابيب.**

**These figures describe what the sprint produced in internal improvements. They do not represent verification of sales outcomes or pipeline acceleration.**

---

## حدود هذه الحالة — Limitations

- دراسة حالة توضيحية مُركَّبة — غير مرتبطة بعميل حقيقي مُحدد.
- أرقام قيمة العقود المُقدَّرة مبنية على بيانات الشركة الداخلية التوضيحية، لا على قياسات سوق مستقلة.
- التحويل إلى Managed Ops قرار فردي للعميل — لا يُمثّل نمطاً مضموناً.
- التحسن في درجة DQ من 61 إلى 78 يعكس تنظيف البيانات، لا بالضرورة تحسناً في الأداء التجاري.

- Composite illustrative case study — not tied to a specific real client.
- Estimated contract value figures are based on internal illustrative data, not independent market measurements.
- Conversion to Managed Ops is an individual client decision — not a guaranteed pattern.
- DQ improvement from 61 to 78 reflects data cleaning, not necessarily commercial performance improvement.

---

روابط ذات صلة: [case_001_anonymized.md](./case_001_anonymized.md) | [case_002_anonymized.md](./case_002_anonymized.md) | [CASE_STUDY_LOGISTICS_AR.md](./CASE_STUDY_LOGISTICS_AR.md)

---

**القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.**
