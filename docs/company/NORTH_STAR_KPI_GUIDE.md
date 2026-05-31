# دليل مؤشرات الأداء — النجم الشمالي | North Star KPI Guide

**الجمهور:** داخلي — المؤسس وفريق العمليات  
**Audience:** Internal — Founder and Operations Team  
**آخر تحديث | Last updated:** 2026-05-31  
**الإصدار | Version:** 1.0  
**المالك | Owner:** المؤسس / Founder

> هذا الملف يوسّع [`KPI_SYSTEM.md`](KPI_SYSTEM.md) و[`NORTH_STAR_METRICS.md`](NORTH_STAR_METRICS.md) بتفاصيل قابلة للقياس. عند التعارض يُقدَّم هذا الملف.
>
> This file extends [`KPI_SYSTEM.md`](KPI_SYSTEM.md) and [`NORTH_STAR_METRICS.md`](NORTH_STAR_METRICS.md) with measurable, owner-assigned detail. In case of conflict, this file takes precedence.

---

## ١. النجم الشمالي الوحيد | The Single North Star Metric

### عربي

**الإيراد المتكرر الشهري (MRR)** هو المقياس الرئيسي لـ Dealix في مرحلة التأسيس لسببين محددين:

**أولاً: الاستقرار.** عقود الـ Sprint تُنتج إيراداً نقدياً جيداً لكنها تتطلب مبيعات مستمرة لكل ريال. الـ MRR من عقود Managed Ops يتراكم — كل عقد جديد يُضاف فوق ما سبق دون أن يُلغي المبيعات القديمة.

**ثانياً: الإثبات.** عميل يدفع شهرياً لأشهر متعددة هو دليل مُتحقَّق على القيمة المُقدَّمة. لا مقياس آخر يُثبت جودة التسليم بنفس الوضوح.

الهدف التقديري: **100,000 ريال MRR بنهاية 2026** — هذا رقم توجيهي يستلزم مراجعة المؤسس كل ربع سنة.

### English

**Monthly Recurring Revenue (MRR)** is Dealix's primary metric at the founding stage for two specific reasons.

**First: stability.** Sprint contracts produce strong project cash but require a fresh sale for every new riyal. MRR from Managed Ops compounds — each new retainer adds to the floor, not in place of prior revenue.

**Second: proof.** A client paying month-over-month for multiple periods is verifiable evidence of delivered value. No other single metric demonstrates delivery quality as directly.

Estimated target: **SAR 100,000 MRR by end of 2026** — this is a directional figure subject to founder review each quarter.

---

## ٢. عائلات المؤشرات الخمس | The 5 KPI Families

### العائلة ١: مؤشرات الإيراد | Family 1: Revenue KPIs

| المؤشر | KPI | الهدف التقديري | التكرار | المالك |
|---|---|---|---|---|
| الإيراد المتكرر الشهري | MRR | 100,000 ريال بنهاية 2026 (تقدير) | يومي | المؤسس |
| صافي معدل الاحتفاظ | NRR | >= 110% | شهري | المؤسس |
| معدل تحول Sprint إلى عقد مستمر | Sprint-to-Retainer Conversion | >= 40% | شهري | المؤسس |
| تكلفة اكتساب العميل | CAC | < 3 أشهر من MRR العميل | ربع سنوي | المؤسس |

**ملاحظة على NRR:** معدل يتجاوز 100% يعني أن الإيراد من العملاء الحاليين ينمو، سواء بالتوسع في النطاق أو الترقية — دليل على تعمق القيمة وليس مجرد الاحتفاظ.

**Note on NRR:** A rate above 100% means revenue from existing clients is growing — through scope expansion or tier upgrades — which is evidence of deepening value delivery, not merely retention.

---

### العائلة ٢: مؤشرات صحة العميل | Family 2: Client Health KPIs

| المؤشر | KPI | الهدف | التكرار | المالك |
|---|---|---|---|---|
| متوسط درجة صحة المحفظة | Avg Portfolio Health Score | >= 75 | أسبوعي | مدير نجاح العميل |
| معدل تسليم Proof Pack في الموعد | Proof Pack Delivery Rate | 100% خلال 7 أيام من إغلاق الـ Sprint | أسبوعي | قائد التسليم |
| متوسط NPS | Average NPS | >= 8.5 | شهري | المؤسس |
| عملاء بصحة أقل من 60 | Clients with Health Score < 60 | = 0 | أسبوعي | المؤسس |

**ملاحظة على درجة الصحة:** المنهجية موثقة في [`../11_client_os/CAPABILITY_DASHBOARD.md`](../11_client_os/CAPABILITY_DASHBOARD.md). أي عميل يسجل أقل من 60 يستلزم خطة تصحيح خلال 72 ساعة.

**Note on Health Score:** Methodology is documented in [`../11_client_os/CAPABILITY_DASHBOARD.md`](../11_client_os/CAPABILITY_DASHBOARD.md). Any client scoring below 60 requires a correction plan within 72 hours.

---

### العائلة ٣: مؤشرات التسليم | Family 3: Delivery KPIs

| المؤشر | KPI | الهدف | التكرار | المالك |
|---|---|---|---|---|
| تسليم Sprint في الموعد | Sprint On-Time Delivery | >= 95% | أسبوعي | قائد التسليم |
| متوسط تحسين درجة جودة البيانات | Avg DQ Score Improvement | >= 20 نقطة لكل Sprint | لكل Sprint | قائد البيانات |
| معدل امتثال ZATCA (محفظة العملاء) | ZATCA Compliance Rate | 100% | شهري | المؤسس |

**ملاحظة على DQ Score:** المنهجية في [`../04_data_os/DATA_QUALITY_SCORE.md`](../04_data_os/DATA_QUALITY_SCORE.md). الـ 20 نقطة هدف أدنى — التحسينات الأعلى تُوثَّق في Proof Pack.

**Note on DQ Score:** Methodology lives in [`../04_data_os/DATA_QUALITY_SCORE.md`](../04_data_os/DATA_QUALITY_SCORE.md). The 20-point target is a floor — higher improvements are documented in the Proof Pack.

---

### العائلة ٤: مؤشرات المسار البيعي | Family 4: Pipeline KPIs

| المؤشر | KPI | الهدف التقديري | التكرار | المالك |
|---|---|---|---|---|
| قيمة المسار المؤهل | Qualified Pipeline Value | >= 250,000 ريال | أسبوعي | المؤسس |
| متوسط سرعة الصفقة | Avg Deal Velocity | <= 21 يوماً (Lead → Sprint) | أسبوعي | المؤسس |
| معدل الفوز (مؤهل → Sprint) | Win Rate (Qualified → Sprint) | >= 60% | شهري | المؤسس |

**ملاحظة التأهيل:** Lead مؤهل = تلبية معايير [`ICP.md`](ICP.md) + وجود صاحب قرار + ميزانية محددة + مشكلة موثقة. المسار غير المؤهل لا يُحسب.

**Qualification note:** A qualified lead meets [`ICP.md`](ICP.md) criteria, has an identified decision-maker, a confirmed budget, and a documented problem statement. Unqualified pipeline does not count.

---

### العائلة ٥: مؤشرات الحوكمة | Family 5: Governance KPIs

| المؤشر | KPI | الهدف | التكرار | المالك |
|---|---|---|---|---|
| معدل الامتثال لـ APPROVAL_FIRST | APPROVAL_FIRST Compliance Rate | 100% — لا إجراءات أحادية الجانب | يومي | المؤسس |
| الموافقات المعلقة مُقفلة خلال 48 ساعة | Pending Approvals Cleared ≤ 48h | 100% | يومي | المؤسس |
| حوادث الحوكمة | Governance Incidents | = 0 | يومي | المؤسس |

**ملاحظة:** حادثة الحوكمة = أي إجراء خارجي تم دون موافقة مسبقة، أو كشف PII غير مقصود، أو إرسال رسالة بدون صلاحية صريحة. راجع [`../05_governance_os/GOVERNANCE_OS.md`](../05_governance_os/GOVERNANCE_OS.md).

**Note:** A governance incident is any external action taken without prior approval, any unintended PII disclosure, or any message sent without explicit authorisation. See [`../05_governance_os/GOVERNANCE_OS.md`](../05_governance_os/GOVERNANCE_OS.md).

---

## ٣. جدول مراجعة المؤشرات | KPI Review Cadence

### يومي | Daily

- MRR الحالي مقارنة بالشهر الماضي
- الموافقات المعلقة (هدف: صفر تتجاوز 48 ساعة)
- الفواتير المتأخرة (هدف: صفر متجاوزة 14 يوماً)
- حوادث الحوكمة أو انتهاكات PII (هدف: صفر)

Current MRR vs. prior month | Pending approvals (target: zero older than 48h) | Overdue invoices (target: zero past 14 days) | Governance or PII incidents (target: zero).

### أسبوعي | Weekly

- قيمة المسار المؤهل وعدد الصفقات في كل مرحلة
- درجات صحة العملاء — تحديد أي عميل دون 60
- قائمة انتظار Proof Pack — هل تجاوز أي Sprint 7 أيام دون تسليم؟
- معدل التسليم في الموعد

Qualified pipeline value and stage distribution | Client health scores — flag any below 60 | Proof Pack queue — any Sprint past 7 days without delivery | On-time delivery rate.

### شهري | Monthly

- صافي معدل الاحتفاظ (NRR) وتحليل التوسع والانكماش
- تحليل تحسين درجة جودة البيانات عبر السبرينتات
- تحليل الاستبقاء والتقليص — هل هناك عميل قلّص نطاقه؟ لماذا؟
- معدل تحول Sprint إلى Retainer
- NPS وردود الفعل النوعية

NRR with expansion/contraction breakdown | DQ Score improvement analysis across sprints | Churn analysis — any scope reduction, reason documented | Sprint-to-Retainer conversion | NPS and qualitative feedback.

### ربع سنوي | Quarterly

- تكلفة اكتساب العميل (CAC) مقارنة بـ LTV المقدَّر
- مراجعة الأهداف التقديرية لنهاية العام وتعديلها إن لزم
- تحليل الـ Win Rate التراكمي
- مراجعة هيكل التكلفة مقارنة بالهامش الإجمالي

CAC vs. estimated LTV | Full-year target review and adjustment if warranted | Cumulative win rate analysis | Cost structure review vs. gross margin.

---

## ٤. بروتوكول العلامة الحمراء | Red Flag Protocol

### الشرط | Trigger

أي مؤشر يتجاوز **20% دون الهدف لمدة أسبوعين متتاليين أو أكثر** يستلزم تصعيداً فورياً للمؤسس مع تقرير سبب وخطة تصحيح خلال 48 ساعة.

Any KPI more than **20% below target for two or more consecutive weeks** requires immediate escalation to the founder with a root-cause note and a correction plan within 48 hours.

### أمثلة محددة | Specific Examples

| المؤشر | حد العلامة الحمراء |
|---|---|
| Sprint On-Time Delivery | < 76% لأسبوعين |
| Portfolio Health Score | < 60 لأسبوعين |
| Qualified Pipeline | < 200,000 ريال لأسبوعين |
| Governance Incidents | أي حادثة واحدة = تصعيد فوري |
| Proof Pack Delivery Rate | < 80% لأسبوعين |

**العلامات الحمراء الفورية** (لا تنتظر أسبوعين):

- أي حادثة حوكمة أو كشف PII
- عميل يُعلن نيته إنهاء العقد
- فاتورة متأخرة 30 يوماً أو أكثر
- أي إجراء خارجي دون موافقة مسبقة

**Immediate red flags** (no two-week wait):

- Any governance incident or PII disclosure
- A client signalling intent to terminate
- An invoice overdue 30 days or more
- Any external action taken without prior approval

---

## ٥. ما لا تُحسِّنه | What NOT to Optimise For

### المقاييس الوهمية التي يجب تجاهلها | Vanity Metrics to Ignore

المقاييس التالية قد تبدو إيجابية لكنها لا تترجم إلى إيراد مُتحقَّق أو قيمة مُسلَّمة. تتبعها تشتيت محوري.

The following metrics can appear positive but do not translate to verified revenue or delivered value. Tracking them is a distraction from the north star.

- **مشاهدات الصفحة وعدد المتابعين | Page views and follower count** — لا علاقة مباشرة بالإيراد في نموذج B2B المُوجَّه.
- **طلبات العروض بدون تأهيل | Demo requests without qualification** — طلب العرض لا يعني وجود نية شراء حقيقية.
- **عدد الـ Leads الإجمالي | Total lead count** — يهم فقط عدد الـ Leads المؤهلة بمعايير [`ICP.md`](ICP.md).
- **عدد المحادثات البيعية | Number of sales conversations** — المحادثات بدون قرار لا تُحسب.
- **نشاط وسائل التواصل الاجتماعي | Social media engagement** — يُقاس بالمقالات التي تُولِّد استفسارات مؤهلة، لا بالإعجابات.

إذا لم يرتبط مقياس ما بأحد مؤشرات العائلات الخمس أعلاه — فهو ليس أولوية تشغيلية.

If a metric does not link directly to one of the five KPI families above, it is not an operational priority.

---

## الروابط المرجعية | Cross-References

- [`KPI_SYSTEM.md`](KPI_SYSTEM.md) — تعريفات أساسية للمؤشرات
- [`NORTH_STAR_METRICS.md`](NORTH_STAR_METRICS.md) — المقياس الرئيسي التاريخي
- [`OPERATING_SCORECARD.md`](OPERATING_SCORECARD.md) — بطاقة المراجعة الأسبوعية
- [`FOUNDER_KPIS_AR.md`](FOUNDER_KPIS_AR.md) — قائمة المؤسس العشرة
- [`FINANCIAL_MODEL.md`](FINANCIAL_MODEL.md) — الأهداف المالية الاتجاهية
- [`../04_data_os/DATA_QUALITY_SCORE.md`](../04_data_os/DATA_QUALITY_SCORE.md) — منهجية درجة جودة البيانات
- [`../05_governance_os/GOVERNANCE_OS.md`](../05_governance_os/GOVERNANCE_OS.md) — سياسة الحوكمة
- [`../11_client_os/CAPABILITY_DASHBOARD.md`](../11_client_os/CAPABILITY_DASHBOARD.md) — درجة صحة العميل
- [`ICP.md`](ICP.md) — معايير تأهيل العميل المثالي

---

*جميع الأهداف الواردة في هذا الملف أرقام تقديرية وتستلزم مراجعة المؤسس كل ربع سنة. القيمة التقديرية ليست قيمة مُتحقَّقة.*

*All targets in this file are estimates and require founder review each quarter. Estimated value is not Verified value.*
