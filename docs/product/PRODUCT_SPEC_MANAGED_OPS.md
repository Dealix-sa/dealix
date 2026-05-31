# مواصفات المنتج — Dealix Managed Ops
# Product Specification — Dealix Managed Ops

> **الجمهور:** فريق التسليم الداخلي، المستثمرون، العملاء المحتملون الذين يُراجعون قائمة الميزات.
> **Audience:** internal delivery team, investors, prospective clients reviewing the feature list.
>
> Managed Ops هو عقد إدارة عمليات إيرادات شهري مُحوكَم — ليس اشتراكاً في برمجية.
> Managed Ops is a monthly governed revenue operations management retainer — not a software subscription.

روابط: [INVESTOR_BRIEF_AR.md](../company/INVESTOR_BRIEF_AR.md) | [SPRINT_DELIVERY_PLAYBOOK.md](../03_commercial_mvp/SPRINT_DELIVERY_PLAYBOOK.md) | [../05_governance_os/APPROVAL_POLICY.md](../05_governance_os/APPROVAL_POLICY.md)

---

## 1. نظرة عامة على المنتج — Product Overview

**بالعربية:**
Dealix Managed Ops خدمة إدارة عمليات إيرادات شهرية تُقدَّم للشركات التي أتمت سبرنت التشخيص وأثبتت جاهزيتها للتشغيل المستمر. الخدمة تُحوّل المخرجات الفورية للسبرنت إلى نظام مُستدام يُراقب جودة البيانات، ويكشف عن تسريبات الإيرادات، ويضمن الامتثال لـ ZATCA وPDPL، ويُنتج تقارير موثَّقة — مع الحفاظ على مبدأ APPROVAL_FIRST لكل إجراء خارجي.

**الشركة المناسبة:**
- أتمت سبرنت التشخيص وحققت Proof Score 70+
- لديها مالك معيَّن لسير العمل
- تُصدر فواتير B2B بحجم منتظم
- تحتفظ ببيانات عملاء تخضع لـ PDPL
- تُريد نظام عمليات إيرادات قابل للتدقيق لا مجرد أداة

**الشركة غير المناسبة:**
- تريد أتمتة رسائل بالجملة دون موافقة مُسجَّلة
- ليس لديها مالك معيَّن لسير العمل
- لا تمتلك بيانات عملاء منظمة

**In English:**
Dealix Managed Ops is a monthly revenue operations management service for companies that have completed the diagnostic sprint and demonstrated readiness for ongoing operations. The service converts sprint outputs into a sustainable system that monitors data quality, surfaces revenue leakage, ensures ZATCA and PDPL compliance, and produces documented reports — while maintaining APPROVAL_FIRST for every external action.

**Right-fit company:**
- Completed the diagnostic sprint with Proof Score 70+
- Has a named workflow owner
- Issues B2B invoices at regular volume
- Holds customer data subject to PDPL
- Wants an auditable revenue operations system, not just a tool

**Wrong-fit company:**
- Wants bulk message automation without logged approval
- Has no named workflow owner
- Has no structured customer data

---

## 2. المستويات الثلاثة — Three Tiers

**بالعربية:**

| الميزة | Essential | Professional | Enterprise |
|---|---|---|---|
| السعر الشهري | 2,999 ريال | 3,999 ريال | 4,999 ريال |
| تقرير جودة البيانات (DQ) | شهري | شهري | أسبوعي |
| أبعاد DQ المُراقَبة | 6 | 6 | 6 + أبعاد مخصصة |
| مراقبة ZATCA | ✓ | ✓ | ✓ + تنبيهات فورية |
| حماية PDPL | ✓ | ✓ | ✓ + تدقيق ربع سنوي |
| قائمة أولويات الحسابات | 10 حسابات/شهر | 20 حساباً/شهر | غير محدودة |
| مسودات التواصل | حتى 8/شهر | حتى 15/شهر | غير محدودة |
| لوحة التحكم الصحية | 6 أبعاد | 6 + تخصيص | 6 + تخصيص + API |
| تحديث حزمة الإثبات | ربع سنوي | ربع سنوي | شهري |
| جلسات المراجعة | 1 × 45 دقيقة/شهر | 2 × 45 دقيقة/شهر | 4 × 60 دقيقة/شهر |
| تكامل CRM مخصص | — | ✓ | ✓ |
| دعم متعدد سير العمل | — | حتى 3 | غير محدود |
| مدير حساب مخصص | — | — | ✓ |

**In English:**

| Feature | Essential | Professional | Enterprise |
|---|---|---|---|
| Monthly price | SAR 2,999 | SAR 3,999 | SAR 4,999 |
| Data Quality (DQ) report | Monthly | Monthly | Weekly |
| DQ dimensions monitored | 6 | 6 | 6 + custom dimensions |
| ZATCA monitoring | Yes | Yes | Yes + real-time alerts |
| PDPL guard | Yes | Yes | Yes + quarterly audit |
| Account priority list | 10 accounts/month | 20 accounts/month | Unlimited |
| Communication drafts | Up to 8/month | Up to 15/month | Unlimited |
| Health dashboard | 6 dimensions | 6 + customization | 6 + customization + API |
| Proof Pack update | Quarterly | Quarterly | Monthly |
| Review sessions | 1 × 45 min/month | 2 × 45 min/month | 4 × 60 min/month |
| Custom CRM integration | — | Yes | Yes |
| Multi-workflow support | — | Up to 3 | Unlimited |
| Dedicated account manager | — | — | Yes |

---

## 3. المُسلَّمات الشهرية — Monthly Deliverables

**بالعربية — ما يتلقاه العميل كل شهر:**

1. **تقرير جودة البيانات الشهري:** درجة DQ الحالية مقارنةً بالشهر السابق، مُفصَّل عبر 6 أبعاد، مع قائمة مشاكل وإجراءات موصى بها.
2. **قائمة الأولويات المُحدَّثة:** أفضل 10 (أو 20) حساباً مُرتَّبة بمعايير شفافة مع جمل تفسيرية لكل حساب بالعربية والإنجليزية.
3. **تقرير مراقبة ZATCA:** حالة الامتثال لتنسيقات الفواتير النشطة، أي تحذيرات Fatoora خلال الشهر، توصيات تصحيح.
4. **تقرير مخاطر PDPL:** مراجعة جوازات المصادر، تنبيهات مدد الاحتفاظ المنتهية أو المقتربة من الانتهاء، حالة التوثيق.
5. **مسودات التواصل:** مسودات عربية وإنجليزية مُصنَّفة DRAFT_ONLY — لا إرسال دون موافقة مُسجَّلة.
6. **سجل الحوكمة الشهري:** جميع قرارات الحوكمة المُتخَّذة خلال الشهر مع النوع، السبب، هوية المُعتمِد، الوقت.
7. **لوحة التحكم الصحية:** 6 أبعاد مُحدَّثة (انظر القسم 4).
8. **جلسة المراجعة:** تقديم النتائج ومناقشة الأولويات مع مالك سير العمل.

**In English — what the client receives each month:**

1. **Monthly Data Quality Report:** current DQ score compared to previous month, detailed across 6 dimensions, with a problem list and recommended actions.
2. **Updated Priority List:** top 10 (or 20) accounts ranked on transparent criteria with explanatory sentences per account in Arabic and English.
3. **ZATCA Monitoring Report:** compliance status of active invoice formats, any Fatoora alerts during the month, correction recommendations.
4. **PDPL Risk Report:** Source Passport review, alerts for expired or near-expiring retention periods, documentation status.
5. **Communication Drafts:** Arabic and English drafts classified DRAFT_ONLY — no sending without logged approval.
6. **Monthly Governance Log:** all governance decisions made during the month with type, reason, approver identity, and timestamp.
7. **Health Dashboard:** 6 dimensions updated (see Section 4).
8. **Review Session:** findings presentation and priority discussion with the workflow owner.

---

## 4. لوحة تحكم الصحة — Health Score Dashboard

**بالعربية:**
لوحة تحكم Dealix الصحية تُقيّم صحة عمليات الإيرادات عبر 6 أبعاد. كل بُعد يُعطى درجة من 0–100. الدرجة الإجمالية هي متوسط مرجَّح.

| البُعد | التعريف | طريقة القياس |
|---|---|---|
| **1. جودة البيانات (DQ)** | نقاء وتكامل بيانات العملاء والحسابات | 6 مقاييس فرعية: تفرد، اكتمال، مطابقة، دقة، حداثة، اتساق |
| **2. امتثال ZATCA** | استيفاء متطلبات المرحلة الثانية للفوترة الإلكترونية | فحص تنسيقات الفواتير النشطة ضد مواصفات ZATCA الحالية |
| **3. سلامة PDPL** | وجود أساس قانوني موثَّق لجميع بيانات PII | جرد جوازات المصادر، الأساس القانوني، مدد الاحتفاظ |
| **4. تغطية الأولويات** | نسبة الحسابات ذات الأولوية الحالية التي دخلت في مسار متابعة نشط | حسابات مُتابَعة فعلياً / إجمالي الحسابات ذات الأولوية العالية |
| **5. معدل الموافقة (APPROVAL_FIRST)** | نسبة الإجراءات الخارجية التي حصلت على موافقة مُسجَّلة قبل التنفيذ | قرارات مُوافَق عليها / إجمالي القرارات المُقترَحة |
| **6. حداثة إثبات القيمة** | عمر آخر تحديث لحزمة الإثبات | أيام منذ آخر تحديث للـ Proof Pack |

**تصنيف الدرجة الإجمالية:**
- 80–100: وضع تشغيلي ممتاز
- 60–79: وضع معقول مع فرص تحسين محددة
- 40–59: يتطلب تدخلاً — توصية بتكثيف جلسات المراجعة
- أقل من 40: وضع حرج — يتطلب مراجعة نطاق الخدمة

**In English:**
Dealix's Health Dashboard evaluates revenue operations health across 6 dimensions. Each dimension is scored 0–100. The overall score is a weighted average.

| Dimension | Definition | Measurement Method |
|---|---|---|
| **1. Data Quality (DQ)** | Cleanliness and completeness of client and account data | 6 sub-metrics: uniqueness, completeness, conformance, accuracy, currency, consistency |
| **2. ZATCA Compliance** | Meeting Phase 2 e-invoicing requirements | Active invoice formats checked against current ZATCA specifications |
| **3. PDPL Integrity** | Documented lawful basis for all PII data | Source Passport inventory, lawful basis, retention period audit |
| **4. Priority Coverage** | Percentage of current priority accounts that entered an active follow-up track | Accounts actually followed up / total high-priority accounts |
| **5. APPROVAL_FIRST Rate** | Percentage of external actions that received logged approval before execution | Approved decisions / total proposed decisions |
| **6. Proof Freshness** | Age of the most recent Proof Pack update | Days since last Proof Pack update |

**Overall score classification:**
- 80–100: Excellent operational condition
- 60–79: Adequate condition with specific improvement opportunities
- 40–59: Requires intervention — recommendation to intensify review sessions
- Below 40: Critical condition — requires service scope review

---

## 5. مراقبة ZATCA — ZATCA Monitoring

**بالعربية — ما يُراجَع شهرياً:**

- **تنسيقات الفواتير النشطة:** يُفحَص كل تنسيق فاتورة يستخدمه العميل ضد مواصفات ZATCA المرحلة الثانية الحالية.
- **حالة الربط مع Fatoora:** التحقق من استمرارية الربط مع بيئة الإنتاج.
- **فواتير Fatoora المرفوضة:** تحديد أسباب الرفض وتوصيات التصحيح.
- **تحديثات ZATCA الجديدة:** مراجعة أي إصدارات أو توضيحات جديدة من ZATCA تؤثر على العميل.
- **تنبيهات الموجات القادمة:** إعلام العميل بمواعيد الموجات القادمة التي قد تؤثر على قطاعه.

**آلية الإبلاغ عن المشاكل:**
- درجة امتثال ZATCA تنخفض عن 80 → تنبيه أصفر في لوحة التحكم.
- فواتير مرفوضة نشطة من Fatoora → تنبيه أحمر + تقرير تصحيح طارئ.
- تنسيق فاتورة لا يستوفي المواصفات → إشعار فوري لمالك سير العمل.

**ملاحظة هامة:** Dealix يُقدّم التحليل والتوصيات. تصحيح أنظمة الفوترة هو مسؤولية الشركة ومزوّد ERP. لا يُعدِّل Dealix أنظمة العميل مباشرةً دون موافقة صريحة.

**In English — what is reviewed monthly:**

- **Active invoice formats:** each format the client uses is checked against current ZATCA Phase 2 specifications.
- **Fatoora connection status:** verification of ongoing connection to the production environment.
- **Fatoora-rejected invoices:** identification of rejection reasons and correction recommendations.
- **New ZATCA updates:** review of any new releases or clarifications from ZATCA affecting the client.
- **Upcoming wave alerts:** informing the client of upcoming wave deadlines that may affect their sector.

**Issue reporting mechanism:**
- ZATCA compliance score drops below 80 → yellow alert on dashboard.
- Active Fatoora-rejected invoices → red alert + emergency correction report.
- Invoice format failing specifications → immediate notification to workflow owner.

**Important note:** Dealix provides analysis and recommendations. Correcting billing systems is the responsibility of the company and its ERP provider. Dealix does not modify client systems directly without explicit approval.

---

## 6. حماية PDPL — PDPL Compliance Guard

**بالعربية — ما يُراقَب شهرياً:**

- **جرد جوازات المصادر:** فحص أن جميع مصادر البيانات المستخدمة في الخدمة لها جواز مصدر مُوقَّع وسارٍ.
- **الأساس القانوني:** التحقق من أن كل فئة من فئات البيانات الشخصية لها أساس قانوني موثَّق.
- **مدد الاحتفاظ:** تنبيهات للبيانات التي اقتربت من تاريخ انتهاء الاحتفاظ أو تجاوزته.
- **توافق الاستخدام:** مراجعة أن البيانات لا تُستخدَم خارج الغرض المُصرَّح به في الجواز.

**مبدأ APPROVAL_FIRST في سياق PDPL:**
- أي عملية بيانات جديدة (تصدير، مشاركة، معالجة) تتطلب جواز مصدر جديداً قبل التنفيذ.
- أي إرسال خارجي يستخدم بيانات شخصية يتطلب موافقة مُسجَّلة مسبقة.
- سجل الحوكمة يُبيّن كل قرار يخص البيانات الشخصية مع هوية المُعتمِد والوقت.

**In English — what is monitored monthly:**

- **Source Passport inventory:** verification that all data sources used in the service have signed, current Source Passports.
- **Lawful basis:** verification that each category of personal data has a documented lawful basis.
- **Retention periods:** alerts for data approaching or past its retention expiry.
- **Use alignment:** review that data is not used outside the purpose declared in the passport.

**APPROVAL_FIRST in the PDPL context:**
- Any new data operation (export, sharing, processing) requires a new Source Passport before execution.
- Any external communication using personal data requires prior logged approval.
- The governance log records every decision involving personal data with approver identity and timestamp.

---

## 7. تحديثات حزمة الإثبات — Proof Pack Updates

**بالعربية:**
حزمة الإثبات (Proof Pack) هي المستند الرئيسي الذي يُثبت القيمة التشغيلية للخدمة. تُحدَّث بشكل دوري وليس فقط في نهاية السبرنت.

**دورة التحديث:**
- Essential: ربع سنوياً (كل 3 أشهر)
- Professional: ربع سنوياً
- Enterprise: شهرياً

**ما يتضمنه تحديث حزمة الإثبات:**

1. درجة DQ الحالية مقارنةً بالخط الأساسي من السبرنت.
2. قائمة الأصول الرأسمالية المُضافة منذ آخر تحديث.
3. قرارات الحوكمة التراكمية للفترة.
4. مقاييس ZATCA وPDPL للفترة.
5. ملخص الإجراءات المُنجزة والفرص المُكتشَفة.
6. خارطة الإجراءات المقترحة للربع القادم.

**ملاحظة:** تحديثات الـ Proof Pack توثِّق ما أُنجز ومُلاحَظ. لا تُمثّل ضمانات بنتائج تجارية مُستقبلية.

**In English:**
The Proof Pack is the primary document demonstrating the operational value of the service. It is updated periodically, not only at sprint end.

**Update cycle:**
- Essential: quarterly (every 3 months)
- Professional: quarterly
- Enterprise: monthly

**Proof Pack update contents:**

1. Current DQ score compared to sprint baseline.
2. Capital assets added since last update.
3. Cumulative governance decisions for the period.
4. ZATCA and PDPL metrics for the period.
5. Summary of completed actions and discovered opportunities.
6. Proposed action map for the next quarter.

**Note:** Proof Pack updates document what was accomplished and observed. They do not represent guarantees of future commercial outcomes.

---

## 8. بوابة العميل — Retainer Portal

**بالعربية — ما يعرضه البوابة للعميل:**

| القسم | المحتوى |
|---|---|
| الصفحة الرئيسية | لوحة التحكم الصحية — 6 أبعاد مع درجات حالية وتاريخية |
| ZATCA | حالة الامتثال، آخر فحص، تنبيهات نشطة |
| PDPL | حالة جوازات المصادر، تنبيهات الاحتفاظ |
| قائمة الأولويات | أحدث قائمة مُرتَّبة مع التفسيرات |
| سجل الحوكمة | جميع القرارات المُسجَّلة، قابلة للتصفية |
| المسودات | مسودات DRAFT_ONLY المعلقة بانتظار موافقة |
| حزمة الإثبات | آخر نسخة من الـ Proof Pack قابلة للتحميل |
| التقارير | أرشيف التقارير الشهرية والربع سنوية |

**In English — what the portal shows the client:**

| Section | Content |
|---|---|
| Home | Health Dashboard — 6 dimensions with current and historical scores |
| ZATCA | Compliance status, last check, active alerts |
| PDPL | Source Passport status, retention alerts |
| Priority List | Latest ranked list with explanations |
| Governance Log | All logged decisions, filterable |
| Drafts | Pending DRAFT_ONLY drafts awaiting approval |
| Proof Pack | Latest downloadable Proof Pack version |
| Reports | Archive of monthly and quarterly reports |

---

## 9. مقاييس النجاح — Success Metrics

**بالعربية — كيف تقيس Dealix نجاح Managed Ops:**

| المقياس | التعريف | الهدف |
|---|---|---|
| مراقبة DQ | درجة جودة البيانات تُحافَظ عليها أو تتحسن شهرياً | لا انخفاض عن درجة الخط الأساسي |
| استجابة ZATCA | مدة تصحيح أي مشكلة امتثال بعد اكتشافها | أقل من 30 يوماً |
| معدل APPROVAL_FIRST | نسبة الإجراءات الخارجية بموافقة مُسجَّلة | 100% |
| نضارة الـ Proof Pack | عدد أيام منذ آخر تحديث | أقل من 92 يوماً (Essential/Professional) |
| رضا العميل (NPS) | درجة صافي المروّجين بعد 3 أشهر | 50+ (هدف) |
| توسع النطاق | هل طلب العميل خدمات إضافية؟ | مؤشر نوعي |

**In English — how Dealix measures Managed Ops success:**

| Metric | Definition | Target |
|---|---|---|
| DQ monitoring | Data quality score maintained or improved monthly | No decline from baseline |
| ZATCA response | Time to correct any compliance issue after discovery | Under 30 days |
| APPROVAL_FIRST rate | Percentage of external actions with logged approval | 100% |
| Proof Pack freshness | Days since last update | Under 92 days (Essential/Professional) |
| Client satisfaction (NPS) | Net Promoter Score after 3 months | 50+ (target) |
| Scope expansion | Has client requested additional services? | Qualitative indicator |

---

## 10. إجراءات الإلغاء — Exit Process

**بالعربية:**
إذا قرر العميل إنهاء العقد، تطبّق Dealix الإجراء التالي:

**فترة الإشعار:** 30 يوماً من تاريخ طلب الإنهاء.

**خلال فترة الإشعار:**
- تستمر جميع الخدمات حتى نهاية الفترة.
- يُجهَّز تقرير الخروج (Exit Report) يتضمن: درجة DQ النهائية، آخر تحديث للـ Proof Pack، قائمة الأصول الرأسمالية المُنتَجة، ملخص قرارات الحوكمة الكاملة.

**إعادة البيانات:**
- جميع بيانات العميل تُعاد له في تنسيق CSV أو JSON (حسب الاتفاق) خلال 15 يوماً من نهاية العقد.
- تُحذَف نسخ Dealix من بيانات العميل خلال 30 يوماً من نهاية العقد.
- يُصدَر شهادة حذف مُوقَّعة.

**الأصول التي تبقى مع العميل:**
- حزمة الإثبات الأخيرة.
- سجل الحوكمة الكامل.
- جوازات المصادر الموقعة.
- قواعد الدمج والأصول الرأسمالية المُنتَجة لبياناته.

**الأصول التي تبقى مع Dealix:**
- المنهجيات العامة والأصول الرأسمالية القابلة لإعادة الاستخدام عبر العملاء (مجهَّلة من بيانات العميل).

**In English:**
If the client decides to terminate the retainer, Dealix applies the following process:

**Notice period:** 30 days from the termination request date.

**During the notice period:**
- All services continue until the end of the period.
- An Exit Report is prepared including: final DQ score, last Proof Pack update, list of capital assets produced, complete governance decision summary.

**Data return:**
- All client data is returned in CSV or JSON format (per agreement) within 15 days of contract end.
- Dealix's copies of client data are deleted within 30 days of contract end.
- A signed deletion certificate is issued.

**Assets that remain with the client:**
- The final Proof Pack.
- Complete governance log.
- Signed Source Passports.
- Merge rules and capital assets produced for their data.

**Assets that remain with Dealix:**
- General methodologies and cross-client reusable capital assets (anonymized from client data).

---

## روابط مرجعية داخلية
## Internal Cross-References

- [INVESTOR_BRIEF_AR.md](../company/INVESTOR_BRIEF_AR.md) — الملخص التنفيذي للمستثمرين
- [UNIT_ECONOMICS_2026.md](../company/UNIT_ECONOMICS_2026.md) — اقتصاديات الوحدة
- [../03_commercial_mvp/SPRINT_DELIVERY_PLAYBOOK.md](../03_commercial_mvp/SPRINT_DELIVERY_PLAYBOOK.md) — دليل تسليم السبرنت
- [../05_governance_os/APPROVAL_POLICY.md](../05_governance_os/APPROVAL_POLICY.md) — سياسة APPROVAL_FIRST
- [../04_data_os/SOURCE_PASSPORT.md](../04_data_os/SOURCE_PASSPORT.md) — جواز المصدر
- [../07_proof_os/PROOF_PACK_STANDARD.md](../07_proof_os/PROOF_PACK_STANDARD.md) — معيار حزمة الإثبات

---

**القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.**
