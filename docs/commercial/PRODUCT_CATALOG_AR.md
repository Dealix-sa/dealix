# كتالوج المنتجات — Dealix Revenue Execution OS — Product Catalog

> **مصدر الحقيقة للأسعار:** [DEALIX_REVOPS_PACKAGES_AR.md](DEALIX_REVOPS_PACKAGES_AR.md) و `autonomous_growth/product_catalog.py` — هذا الملف **لا يخترع أسعاراً جديدة**. أي اختلاف بين هذا الملف والمصدرين أعلاه يُحسم لصالح المصدرين.
>
> **Pricing source of truth:** [DEALIX_REVOPS_PACKAGES_AR.md](DEALIX_REVOPS_PACKAGES_AR.md) and `autonomous_growth/product_catalog.py`. This file introduces no new prices.

هذا الكتالوج هو المرجع التجاري الموحَّد لكل منتج في Dealix: ما هو، ووعده، ومتى نبيعه، ولمن، وحدوده السعرية، ومخرجاته، وما لا يشمله، والدليل المطلوب قبل البيع، ومتى يحتاج موافقة المؤسس. كل عرض يُرسَل لعميل **يجب** أن يُربَط بمنتج واحد من هذا الكتالوج عبر الحقل `product_id`.

This catalog is the unified commercial reference for every Dealix product: what it is, its promise, when we sell it, to whom, its price bands, deliverables, exclusions, the evidence required before selling, and when founder approval is needed. Every offer sent to a customer **must** link to one product here via the `product_id` field.

روابط ذات صلة / Related: [OFFER_LADDER_AR.md](OFFER_LADDER_AR.md) · [PRICING_GUARDRAILS_AR.md](PRICING_GUARDRAILS_AR.md) · [APPROVAL_POLICY_AR.md](APPROVAL_POLICY_AR.md) · [../distribution/REVENUE_EXECUTION_OS_AR.md](../distribution/REVENUE_EXECUTION_OS_AR.md) · [../distribution/PROPOSAL_FACTORY_AR.md](../distribution/PROPOSAL_FACTORY_AR.md)

---

## مسارا المنتجات / Two product tracks

Dealix يبيع عبر **مسارين متوازيين** بنفس الحوكمة وبأسعار معتمدة لا تتغير:

Dealix sells through **two parallel tracks** under the same governance with fixed, approved prices:

1. **السلم الخماسي للخدمة الذاتية (Self-serve ladder)** — من `autonomous_growth/product_catalog.py`: تشخيص مجاني → سبرينت ذكاء الإيرادات → حزمة البيانات → العمليات المُدارة → حل ذكاء اصطناعي مخصص.
2. **عقود RevOps الأعلى لمساً (Higher-touch RevOps)** — من [DEALIX_REVOPS_PACKAGES_AR.md](DEALIX_REVOPS_PACKAGES_AR.md): Revenue Diagnostic → Lead Intelligence Sprint → Pilot Conversion → Monthly RevOps OS → Enterprise AI Revenue OS.

> القاعدة: لا نخلط أسعار المسارين في عرض واحد. العميل يدخل من مسار، ويُرقَّى داخل مساره أو ينتقل للمسار الأعلى **بعد دليل** (راجع [OFFER_LADDER_AR.md](OFFER_LADDER_AR.md)).

---

## جدول مرجعي سريع / Quick reference

| product_id | الاسم AR | Name EN | المسار | السعر الأدنى | السعر الأعلى | مدة التسليم |
|---|---|---|---|---:|---:|---|
| `prod_diagnostic_v1` | تشخيص مجاني | Free Diagnostic | Self-serve | 0 | 0 | يوم واحد |
| `prod_sprint_v1` | سبرينت ذكاء الإيرادات | Revenue Intelligence Sprint | Self-serve | 499 | 499 | 7 أيام |
| `prod_data_pack_v1` | حزمة البيانات | Data Pack | Self-serve | 1,500 | 1,500 | 14 يوماً |
| `prod_managed_ops_v1` | العمليات المُدارة | Managed Ops | Self-serve | 2,999/شهر | 4,999/شهر | 30 يوماً |
| `prod_custom_ai_v1` | حل ذكاء اصطناعي مخصص | Custom AI | Self-serve | 5,000 | 25,000 | 90 يوماً |
| `revops_diagnostic` | Revenue Diagnostic | Revenue Diagnostic | RevOps | 3,500 | 3,500 | 3–5 أيام |
| `revops_sprint` | Lead Intelligence Sprint | Lead Intelligence Sprint | RevOps | 9,500 | 9,500 | حتى 10 أيام |
| `revops_pilot` | Pilot Conversion Sprint | Pilot Conversion Sprint | RevOps | 22,000 | 22,000 | 30 يوماً |
| `revops_os_monthly` | Monthly RevOps OS | Monthly RevOps OS | RevOps | 15,000/شهر | 35,000+/شهر | مستمر |
| `revops_enterprise` | Enterprise AI Revenue OS | Enterprise AI Revenue OS | RevOps | 85,000 إعداد | حسب SOW | حسب SOW |

> جميع الأسعار بالريال السعودي (SAR). نطاقات المفاوضة الموسّعة في [PRICING_GUARDRAILS_AR.md](PRICING_GUARDRAILS_AR.md) — للمؤسس فقط، لا تُعلَن ككل العروض.

---

## المسار الأول — السلم الخماسي للخدمة الذاتية / Track 1 — Self-serve ladder

### 1) تشخيص مجاني — Free Diagnostic — `prod_diagnostic_v1`

- **اسم المنتج / Name:** تشخيص مجاني / Free Diagnostic
- **الوعد التجاري / Promise:** جلسة 30 دقيقة تحدّد أكبر فرص الإيراد وأبرز نقاط الألم — بلا التزام وبلا تكلفة. / A 30-minute session that surfaces the top revenue opportunities and pain points — no commitment, no cost.
- **متى نبيعه / When:** أول نقطة دخول لعميل جديد أو غير مؤهَّل بعد. / First entry point for a new or not-yet-qualified prospect.
- **لمن / For whom:** أي حجم شركة، أي قطاع، `min_icp_score = 0.0`. / Any size, any sector.
- **السعر الأدنى / Min price:** 0
- **السعر الأعلى / Max price:** 0
- **مدة التسليم / Delivery:** يوم واحد / 1 day.
- **المخرجات / Deliverables:** خريطة نقاط الألم الرئيسية، توصية أولية بالمنتج المناسب. / Top pain-point map, initial product recommendation.
- **ما لا يشمله / Out of scope:** تحليل بيانات كامل، أي مخرج مكتوب موسّع، أي التزام تعاقدي. / Full data analysis, extended written deliverable, contractual commitment.
- **الدليل المطلوب قبل البيع / Evidence before selling:** لا يوجد — هذا هو مولِّد الدليل الأول؛ يُسجَّل `evidence_level` ابتدائياً عند **L0–L1**. / None — this generates the first evidence; `evidence_level` starts at **L0–L1**.
- **متى يحتاج موافقة / When approval needed:** الجدولة لا تحتاج موافقة؛ أي مخرج مكتوب يُرسَل للعميل يمر بطابور الموافقة. / Scheduling needs no approval; any written deliverable sent passes the approval queue.

### 2) سبرينت ذكاء الإيرادات — Revenue Intelligence Sprint — `prod_sprint_v1`

- **اسم المنتج / Name:** سبرينت ذكاء الإيرادات / Revenue Intelligence Sprint
- **الوعد التجاري / Promise:** أسبوع واحد يُنتج خريطة إيرادات مفصّلة مع 3 فرص قابلة للتطبيق فوراً مبنية على بيانات السوق السعودي. / One week producing a detailed revenue map with 3 immediately actionable opportunities grounded in Saudi market data.
- **متى نبيعه / When:** بعد تشخيص مجاني أظهر اهتماماً وحاجة واضحة. / After a free diagnostic surfaced clear interest and need.
- **لمن / For whom:** الشركات الصغيرة والمتوسطة، `min_icp_score = 0.3`. / Small and medium companies.
- **السعر الأدنى / Min price:** 499
- **السعر الأعلى / Max price:** 499 (سعر ثابت / fixed)
- **مدة التسليم / Delivery:** 7 أيام / 7 days.
- **المخرجات / Deliverables:** خريطة إيرادات مفصّلة، 3 فرص نمو قابلة للتطبيق. / Detailed revenue map, 3 actionable growth opportunities.
- **ما لا يشمله / Out of scope:** تنفيذ الفرص نيابة عن العميل، إرسال خارجي، تكامل CRM. / Executing opportunities for the customer, external sending, CRM integration.
- **الدليل المطلوب قبل البيع / Evidence before selling:** مخرج تشخيص أو فهم أولي للقطاع؛ `evidence_level ≥ L1`. / Diagnostic output or initial sector understanding; `evidence_level ≥ L1`.
- **متى يحتاج موافقة / When approval needed:** السعر ثابت فلا مفاوضة؛ التقرير النهائي يمر بطابور الموافقة قبل التسليم. / Fixed price, no negotiation; the final report passes the approval queue before delivery.

### 3) حزمة البيانات — Data Pack — `prod_data_pack_v1`

- **اسم المنتج / Name:** حزمة البيانات / Data Pack
- **الوعد التجاري / Promise:** حزمة شاملة: تحليل قطاعي عميق، ملفات ICP، ومعيارة أداء مقابل منافسي السوق السعودي. / A comprehensive pack: deep sector analysis, ICP profiles, and benchmarking against Saudi market competitors.
- **متى نبيعه / When:** عندما يحتاج العميل عمقاً في الاستهداف بعد السبرينت. / When the customer needs targeting depth after the sprint.
- **لمن / For whom:** صغيرة/متوسطة/كبيرة، `min_icp_score = 0.5`. / Small/medium/large.
- **السعر الأدنى / Min price:** 1,500
- **السعر الأعلى / Max price:** 1,500 (سعر ثابت / fixed)
- **مدة التسليم / Delivery:** 14 يوماً / 14 days.
- **المخرجات / Deliverables:** تحليل قطاعي عميق، ملفات ICP، معيارة أداء مقابل المنافسين. / Deep sector analysis, ICP profiles, competitor benchmarking.
- **ما لا يشمله / Out of scope:** قوائم مشتراة، scraping، تشغيل مستمر. / Bought lists, scraping, ongoing operations.
- **الدليل المطلوب قبل البيع / Evidence before selling:** سبرينت مكتمل أو فهم مؤكَّد للـ ICP؛ `evidence_level ≥ L2`. / Completed sprint or confirmed ICP understanding; `evidence_level ≥ L2`.
- **متى يحتاج موافقة / When approval needed:** السعر ثابت؛ الحزمة تمر بطابور الموافقة قبل التسليم. / Fixed price; the pack passes the approval queue before delivery.

### 4) العمليات المُدارة — Managed Ops — `prod_managed_ops_v1`

- **اسم المنتج / Name:** العمليات المُدارة / Managed Ops
- **الوعد التجاري / Promise:** إدارة شهرية للعمليات التسويقية والبيعية مع تقارير ومؤشرات أداء واضحة. / Monthly management of marketing and sales operations with reports and clear KPIs.
- **متى نبيعه / When:** بعد دليل قيمة متكرّر (سبرينت/حزمة بيانات) ورغبة في تشغيل مستمر. / After repeated value evidence and appetite for ongoing operations.
- **لمن / For whom:** متوسطة/كبيرة، `min_icp_score = 0.5`. / Medium/large.
- **السعر الأدنى / Min price:** 2,999 شهرياً / per month.
- **السعر الأعلى / Max price:** 4,999 شهرياً / per month.
- **مدة التسليم / Delivery:** 30 يوماً للإعداد ثم مستمر / 30-day onboarding then ongoing.
- **المخرجات / Deliverables:** إدارة كاملة للعمليات، تقارير أداء شهرية، مؤشرات نمو واضحة. / Full operations management, monthly reports, clear growth KPIs.
- **ما لا يشمله / Out of scope:** إرسال خارجي بدون موافقة، ضمان أرقام مبيعات، حلول مخصصة كاملة. / External sending without approval, guaranteed sales numbers, full bespoke builds.
- **الدليل المطلوب قبل البيع / Evidence before selling:** نتيجة موثَّقة من منتج أدنى + جهة قرار مؤكَّدة؛ `evidence_level ≥ L3`. / Documented result from a lower product + confirmed decision-maker; `evidence_level ≥ L3`.
- **متى يحتاج موافقة / When approval needed:** **كل** سعر داخل النطاق (2,999–4,999) يحتاج موافقة المؤسس؛ التسعير الشهري والتجديد يمران عبر بوابة الموافقة وطابور التسليم. / **Every** price within the band needs founder approval; monthly pricing and renewal pass the approval gate.

### 5) حل ذكاء اصطناعي مخصص — Custom AI — `prod_custom_ai_v1`

- **اسم المنتج / Name:** حل ذكاء اصطناعي مخصص / Custom AI
- **الوعد التجاري / Promise:** بناء حل مخصص من التصميم إلى النشر والتدريب والتكامل مع الأنظمة الحالية. / Building a bespoke solution from design to deployment, training, and integration.
- **متى نبيعه / When:** لعميل كبير بحاجة مثبتة وجاهزية تنفيذ. / For a large customer with proven need and execution readiness.
- **لمن / For whom:** كبيرة/مؤسسية، `min_icp_score = 0.7`. / Large/enterprise.
- **السعر الأدنى / Min price:** 5,000
- **السعر الأعلى / Max price:** 25,000
- **مدة التسليم / Delivery:** 90 يوماً / 90 days.
- **المخرجات / Deliverables:** حل مخصص، تكامل مع الأنظمة الحالية، تدريب الفريق وتسليمه. / Bespoke solution, integration, team training and handover.
- **ما لا يشمله / Out of scope:** نشر إنتاجي بلا حوكمة، كشف أسرار، ضمان نتائج رقمية. / Production deploy without governance, secret exposure, guaranteed numeric results.
- **الدليل المطلوب قبل البيع / Evidence before selling:** نطاق مكتوب (SOW)، جدوى تقنية مؤكَّدة، جهة قرار؛ `evidence_level ≥ L3` ويفضَّل L4. / Written SOW, confirmed technical feasibility, decision-maker; `evidence_level ≥ L3`, ideally L4.
- **متى يحتاج موافقة / When approval needed:** السعر النهائي، النطاق، وأي بند تكامل — **كلها** موافقة مؤسس إلزامية. / Final price, scope, and any integration clause — **all** require mandatory founder approval.

---

## المسار الثاني — عقود RevOps الأعلى لمساً / Track 2 — Higher-touch RevOps

> الأسعار والنطاق الكاملان في [DEALIX_REVOPS_PACKAGES_AR.md](DEALIX_REVOPS_PACKAGES_AR.md). أدناه ملخص تشغيلي بنفس الحقول.

### 6) Revenue Diagnostic — `revops_diagnostic`

- **الوعد / Promise:** تقرير تنفيذي: فجوات إيراد، شرائح، Top 10 فرص، وخطة انتقال للـ Sprint. / Executive report: revenue gaps, segments, Top 10 opportunities, transition plan to Sprint.
- **متى / When:** عميل B2B جاد يريد تقييماً مدفوعاً قبل التشغيل. / Serious B2B prospect wanting a paid assessment first.
- **لمن / For whom:** شركات B2B سعودية. / Saudi B2B companies.
- **السعر / Price:** 3,500 (مدى المفاوضة حتى ~4,500، للمؤسس فقط).
- **المدة / Delivery:** 3–5 أيام عمل.
- **المخرجات / Deliverables:** مراجعة عيّنة بيانات، 3 شرائح، 3 مشاكل إيراد، Top 10 فرص، تقرير PDF، خطة انتقال.
- **ما لا يشمله / Out of scope:** تنظيف كامل، إعداد CRM، حملات، تكاملات عميقة، تنفيذ outreach.
- **الدليل المطلوب / Evidence:** عيّنة بيانات من العميل وجهة قرار؛ `evidence_level ≥ L1`.
- **متى موافقة / Approval:** أي سعر فوق 3,500 موافقة مؤسس؛ التقرير يمر بطابور الموافقة.

### 7) Lead Intelligence Sprint — `revops_sprint` (العرض الافتراضي للبيع الآن)

- **الوعد / Promise:** بيانات مرتبة + dedupe + scoring + Top 50 + خطة 10 إجراءات + حتى 20 مسودة outreach + لوحة pipeline مصغّرة + تقرير تنفيذي. / Cleaned data, dedupe, scoring, Top 50, 10-action plan, up to 20 outreach drafts, mini pipeline board, executive report.
- **متى / When:** بعد Diagnostic ناجح أو عميل جاهز ببيانات. / After a successful Diagnostic or a data-ready customer.
- **لمن / For whom:** B2B سعودية تملك قائمة حسابات. / Saudi B2B with an accounts list.
- **السعر / Price:** 9,500 (مدى المفاوضة حتى ~18,000، للمؤسس فقط).
- **المدة / Delivery:** حتى 10 أيام عمل.
- **المخرجات / Deliverables:** كما في [OFFER_LEAD_INTELLIGENCE_SPRINT_AR.md](OFFER_LEAD_INTELLIGENCE_SPRINT_AR.md) — حتى 500 صف حساب، **المسودات مسودات فقط**.
- **ما لا يشمله / Out of scope:** إرسال فعلي لطرف ثالث، أتمتة LinkedIn، واتساب بارد، شراء قوائم، ضمان تحويل رقمي.
- **الدليل المطلوب / Evidence:** ملف بيانات + DPA + جهة قرار؛ `evidence_level ≥ L2`.
- **متى موافقة / Approval:** أي سعر فوق 9,500 موافقة مؤسس؛ المسودات والتقرير يمران بطابور الموافقة.

### 8) Pilot Conversion Sprint — `revops_pilot`

- **الوعد / Promise:** تشغيل أسبوعي للـ pipeline 30 يوماً مع تقارير، مسودات، تتبع فرص، وProof pack ختامي. / 30-day weekly pipeline operation with reports, drafts, opportunity tracking, and a closing proof pack.
- **متى / When:** بعد Sprint أظهر فرصاً تستحق تشغيلاً ممتداً. / After a Sprint surfaced opportunities worth extended operation.
- **لمن / For whom:** عميل ملتزم بمسؤولية مبيعات داخلية. / A customer owning internal sales responsibility.
- **السعر / Price:** 22,000 (مدى المفاوضة حتى ~45,000، للمؤسس فقط).
- **المدة / Delivery:** 30 يوماً.
- **المخرجات / Deliverables:** مراجعات أسبوعية، تحديث scoring، مسودات، سكربتات مكالمات، تتبع اجتماعات، لوحة فرص، Proof ledger أسبوعي، تقرير تنفيذي، Proof pack ختامي.
- **ما لا يشمله / Out of scope:** تكاملات ERP ثقيلة، بناء وكلاء مخصّصين كاملين، ضمان صفقات مغلقة.
- **الدليل المطلوب / Evidence:** نتيجة Sprint موثَّقة + جهة قرار؛ `evidence_level ≥ L3`.
- **متى موافقة / Approval:** السعر النهائي والنطاق موافقة مؤسس إلزامية.

### 9) Monthly RevOps OS — `revops_os_monthly`

- **الوعد / Promise:** تشغيل مستمر: صيانة scoring، تقارير، مسودات، CRM hygiene، ولوحات. / Ongoing operation: scoring maintenance, reports, drafts, CRM hygiene, dashboards.
- **متى / When:** بعد Pilot ناجح أو رغبة في تشغيل مستمر مثبت القيمة. / After a successful Pilot or proven ongoing appetite.
- **لمن / For whom:** عميل يحتاج RevOps مستمراً. / A customer needing continuous RevOps.
- **السعر / Price:** Starter 15,000/شهر · Growth 25,000/شهر · Scale 35,000+/شهر (Scale يُعرَّف في SOW).
- **المدة / Delivery:** مستمر.
- **المخرجات / Deliverables:** حسب المستوى — راجع [DEALIX_REVOPS_PACKAGES_AR.md](DEALIX_REVOPS_PACKAGES_AR.md).
- **ما لا يشمله / Out of scope:** إرسال خارجي بلا موافقة، ضمان أرقام، تكاملات ثقيلة خارج النطاق المتفق.
- **الدليل المطلوب / Evidence:** قيمة موثَّقة من Pilot/Sprint + جهة قرار؛ `evidence_level ≥ L3`.
- **متى موافقة / Approval:** المستوى الشهري والتجديد وأي تعديل سعر موافقة مؤسس.

### 10) Enterprise AI Revenue OS — `revops_enterprise`

- **الوعد / Promise:** تكاملات، حوكمة بيانات، مهام مخصّصة، تدريب، وSLA. / Integrations, data governance, bespoke tasks, training, SLA.
- **متى / When:** **لا يُعرض إلا** مع عميل كبير وجاهزية تنفيذ، بعد 3–5 عملاء Sprint ناجحين. / Offered **only** to a large customer with execution readiness, after 3–5 successful Sprint customers.
- **لمن / For whom:** مؤسسات. / Enterprises.
- **السعر / Price:** يبدأ من 85,000 إعداد + 35,000–120,000 شهرياً حسب SOW.
- **المدة / Delivery:** حسب SOW.
- **المخرجات / Deliverables:** تُعرَّف بالكامل في SOW.
- **ما لا يشمله / Out of scope:** أي بند خارج SOW الموقَّع، نشر بلا حوكمة، ضمان نتائج.
- **الدليل المطلوب / Evidence:** سجل عملاء ناجح + جدوى مؤكَّدة + جهة قرار تنفيذية؛ `evidence_level ≥ L4`.
- **متى موافقة / Approval:** كل بند — السعر، النطاق، SLA، التكامل — موافقة مؤسس إلزامية، ولا يُذكَر في الموقع العام كعرض افتراضي.

---

## قواعد ملزمة لكل المنتجات / Binding rules for all products

1. كل عرض يُربَط بمنتج عبر `product_id`؛ لا عرض بلا منتج. / Every offer links to a product via `product_id`.
2. لا سعر خارج الحدود المعتمدة هنا وفي [PRICING_GUARDRAILS_AR.md](PRICING_GUARDRAILS_AR.md). / No price outside the approved bands.
3. لا ضمان أرقام مبيعات أو تحويل أو ROI — تُستبدَل بـ«فرص مُثبتة بأدلة». / No guaranteed sales/conversion/ROI — replaced with "evidence-backed opportunities".
4. التسليم في العروض القياسية = **مسودات** للقنوات الخارجية، لا إرسال آلي. / Standard delivery = **drafts** for external channels, no auto-send.
5. كل مخرج يُرسَل للعميل يمر بطابور الموافقة (راجع [APPROVAL_POLICY_AR.md](APPROVAL_POLICY_AR.md)). / Every customer-facing deliverable passes the approval queue.

---

**القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.**
