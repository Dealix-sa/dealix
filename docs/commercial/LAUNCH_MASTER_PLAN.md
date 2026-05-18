<!-- Owner: Founder | Date: 2026-05-18 | Launch Master Plan -->

# خطة Dealix الرئيسية للتدشين والتوسع — Launch & Scale Master Plan

> **قاعدة ذهبية:** كل محرك يُصمَّم الآن، ويُبنى فقط عند فتح بوابة الإيراد الخاصة به. لا بناء قبل دليل طلب حقيقي. لا تقدّم مرحلة بلا دليل مُتحقَّق.

هذا الملف هو **النسخة الرسمية في المستودع** لخطة التدشين المعتمدة على مستوى الـ CEO. هو **فهرس رئيسي** (master index): مختصر وقابل للمسح، يربط كل وثيقة تنفيذية بمكانها. التفاصيل العميقة تعيش في الملفات المرتبطة، لا هنا.

## النطاق / Scope

- **هذا الملف:** الاستراتيجية الحاكمة (Revenue-Gated Automation Ladder)، تعريف Full-Ops، جدول المحركات الاثني عشر، المراحل الخمس وبواباتها، مقاييس North Star، إجراءات الأسبوع الأول.
- **ليس هذا الملف:** قائمة أسعار (المصدر القانوني: [`../OFFER_LADDER_AND_PRICING.md`](../OFFER_LADDER_AND_PRICING.md))، ولا مواصفات محرك تفصيلية ([`ENGINE_SPECS.md`](ENGINE_SPECS.md))، ولا معايير البوابات التفصيلية ([`GATE_CRITERIA.md`](GATE_CRITERIA.md)).
- **الجمهور:** المؤسس والوكلاء التشغيليون (dealix-pm / dealix-sales / dealix-delivery / dealix-content / dealix-engineer).

## السياق / Context

- **الإيراد اليوم = صفر.** القيد ليس الكود — المنصة جاهزة ومُتحقَّق منها.
- **العائق الحقيقي هو البيع، لا البناء.** كل ساعة تُصرف في البناء بدل البيع لها قيمة متوقعة سالبة الآن.
- **بوابة Moyasar هي البوابة الحرجة.** بلا قبول دفع حيّ لا يوجد عرض مدفوع، وبلا عرض مدفوع لا يوجد إثبات حركة.
- **Commercial Freeze نشط** ([`../ops/COMMERCIAL_FREEZE.md`](../ops/COMMERCIAL_FREEZE.md)) — التجميد هنا **آلية حوكمة** وليس عائقاً: يحوّل الجهد من البناء إلى التشغيل والبيع حتى يثبت أول Pilot مدفوع الحركة.
- **السردية مُوحّدة:** Dealix تُباع كـ Software + Service + AI Operations للشركات السعودية B2B — تنظيم بيانات، تحديد فرص، مسودات آمنة، تقارير تنفيذية مربوطة بـ Proof — لا «AI عام».

## الاستراتيجية الحاكمة — Revenue-Gated Automation Ladder

المبدأ: **كل المحركات تُصمَّم الآن، وكل محرك يُبنى عند فتح بوابة الإيراد الخاصة به.**

- التصميم رخيص؛ البناء قبل الطلب مكلف ويهرب من البيع.
- كل بوابة (G0–G4) تفتح صلاحية بناء محددة + درجة في سلم الخدمات + رفعاً جزئياً للتجميد.
- لا قفزة درجات: الدرجة تُفتح فقط بعد إثبات موثق من الدرجة السابقة (انظر [`../OFFER_LADDER_AND_PRICING.md`](../OFFER_LADDER_AND_PRICING.md)).
- البناء عند الطلب فقط — تحكمه [`../sales-kit/CONDITIONAL_BUILD_TRIGGERS.md`](../sales-kit/CONDITIONAL_BUILD_TRIGGERS.md): لا إشارة سوق → لا بناء.

## تعريف Full-Ops بدقة — The Full-Ops Definition

«Full-Ops» تعني: **أتمتة كل سير عمل داخلي حتى — وليس بعد — بوابة الموافقة البشرية.**

| يُؤتمت بالكامل (داخلي) | يبقى بشرياً / مُبَوَّباً (خارجي ومالي) |
|---|---|
| تجهيز البيانات، dedupe، scoring، تجميع التقارير | كل إرسال خارجي (رسالة، outreach) — موافقة بشرية صريحة |
| توليد مسودات Proof Pack وتقارير تنفيذية | كل تحصيل مالي (charge) — تأكيد يدوي، لا live charge |
| تحديث السجلات (ledgers)، تتبع pipeline داخلياً | تقدّم أي مرحلة في pipeline — يتطلب دليلاً مُتحقَّقاً |
| تجهيز مسودات المحتوى وأصول AEO | نشر أي مخرج AI للعميل — بعد QA بشري فقط |

القاعدة الواحدة: **كل محرك يتوقف عند بوابة موافقة بشرية.** الأتمتة تجهّز القرار؛ الإنسان يتخذه.

## المحركات الاثنا عشر — The 12 Engines (جدول ملخص)

المواصفات الكاملة لكل محرك: [`ENGINE_SPECS.md`](ENGINE_SPECS.md).

| # | المحرك | بوابة الفتح | الوكيل المالك | الحالة |
|---|--------|-------------|----------------|--------|
| E1 | Revenue Activation (Moyasar، payment links، invoices) | G0 | dealix-engineer | يُصمَّم الآن — يُبنى عند G0 |
| E2 | Founder Sales | الآن | dealix-sales / founder | نشط الآن |
| E3 | Diagnostic & Intake | الآن | dealix-sales | نشط الآن |
| E4 | Proof | G1 | dealix-delivery | يُصمَّم الآن — يُبنى عند G1 |
| E5 | Delivery | G1 | dealix-delivery | يُصمَّم الآن — يُبنى عند G1 |
| E6 | Billing & Finance | G2 | dealix-engineer | يُصمَّم الآن — يُبنى عند G2 |
| E7 | Content & AEO | الآن | dealix-content | نشط الآن |
| E8 | Demand | G2 | dealix-content / dealix-sales | يُصمَّم الآن — يُبنى عند G2 |
| E9 | Partner & Channel | G3 | dealix-pm | يُصمَّم الآن — يُبنى عند G3 |
| E10 | CS & Expansion | G2 | dealix-delivery | يُصمَّم الآن — يُبنى عند G2 |
| E11 | Commercial Control Tower | الآن | dealix-pm | نشط الآن |
| E12 | Autonomous Ops Loop | G3 → G4 | dealix-pm / dealix-engineer | يُصمَّم الآن — يُبنى عند G3 |

المحركات النشطة الآن (E2 / E3 / E7 / E11) متوافقة مع التجميد بالكامل. البقية تُصمَّم الآن وتُبنى عند بوابتها.

## المراحل الخمس والبوابات — The 5 Phases & Gates

المعايير التفصيلية القابلة للتحقق لكل بوابة: [`GATE_CRITERIA.md`](GATE_CRITERIA.md).

| المرحلة | المدى الزمني | البوابة المغلِقة | معيار الخروج الجوهري |
|---|---|---|---|
| **P0 — Revenue Unlock** | أيام 1–14 | **G0** | Moyasar حيّ + أول عرض مدفوع متاح للبيع |
| **P1 — Proof & Repeatability** | أيام 15–45 | **G1** | 3 pilots مدفوعة + 3 Proof Packs + 1 case study + سير عمل Sprint موثّق |
| **P2 — Full-Ops Automation** | أيام 46–90 | **G2** | سير العمل تكرّر ≥3 مرات + أول retainer + MRR ~15–25K |
| **P3 — Scale & Channels** | أيام 91–180 | **G3** | MRR ≥50K + 10 شركاء + inbound مُثبَت + أول توظيف مبيعات |
| **P4 — Category & Platform** | أيام 181–365 | **G4** | MRR ≥150K + اقتصاد وحدة موجب + CAC payback ≤8 أشهر |

> **G1 هو شرط الخروج من Commercial Freeze:** أول pilot مدفوع مُسلَّم + Proof Pack مُعتمَد من العميل بمستوى دليل L3+.

## مقاييس النجاح و North Star

- **النجم الشمالي (North Star):** **Proof Packs المُسلَّمة والمدفوعة** — لا تسجيلات، لا متابعون، لا dashboards فارغة.
- مقاييس داعمة موثّقة بدليل: pilots مدفوعة، MRR مؤكَّد في billing، تكرار سير العمل في delivery ledger، رضا العميل ≥4/5.
- مرجع المقاييس الداخلية الكامل: [`NORTH_STAR_METRICS_AR.md`](NORTH_STAR_METRICS_AR.md).
- **لا ادعاء أرقام مبيعات أو ROI كحقيقة** — كل رقم «تقديري» أو «نمط case-safe».

## إجراءات الأسبوع الأول — Immediate Week-1 Actions

1. تفعيل Moyasar وإنشاء payment link اختباري ناجح — مالك: dealix-engineer (محرك E1، بوابة G0).
2. قفل أول عرض مدفوع للبيع: 7-Day Revenue Proof Sprint بسعر 499 SAR — مالك: dealix-sales.
3. تشغيل warm-list outreach عبر موافقة يدوية لكل رسالة — مالك: founder / dealix-sales (محرك E2).
4. تجهيز Diagnostic & Intake للعرض المجاني — مالك: dealix-sales (محرك E3).
5. نشر محتوى case-style مُجهَّل و AEO — مالك: dealix-content (محرك E7).
6. تشغيل برج التحكم التجاري يومياً بحدث إثبات واحد على الأقل — مالك: dealix-pm (محرك E11، [`COMMERCIAL_CONTROL_TOWER.md`](COMMERCIAL_CONTROL_TOWER.md)).

## المراجع التنفيذية — Plan Documents

- [`ENGINE_SPECS.md`](ENGINE_SPECS.md) — مواصفات المحركات الاثني عشر.
- [`GATE_CRITERIA.md`](GATE_CRITERIA.md) — معايير البوابات G0–G4.
- [`FINANCIAL_MODEL.md`](FINANCIAL_MODEL.md) — النموذج المالي وآلة المال.
- [`AGENT_OPERATING_MODEL.md`](AGENT_OPERATING_MODEL.md) — نموذج تشغيل الوكلاء.
- [`FULL_OPS_AUTOMATION_ARCHITECTURE.md`](FULL_OPS_AUTOMATION_ARCHITECTURE.md) — معمارية أتمتة Full-Ops.
- [`../ops/COMMERCIAL_FREEZE.md`](../ops/COMMERCIAL_FREEZE.md) — التجميد التجاري النشط.
- [`../OFFER_LADDER_AND_PRICING.md`](../OFFER_LADDER_AND_PRICING.md) — سلم الخدمات والأسعار (canonical).
- [`../sales-kit/CONDITIONAL_BUILD_TRIGGERS.md`](../sales-kit/CONDITIONAL_BUILD_TRIGGERS.md) — محفّزات البناء عند الطلب.

## فهرس وثائق docs/commercial/

- [`README.md`](README.md) · [`DEALIX_REVOPS_PACKAGES_AR.md`](DEALIX_REVOPS_PACKAGES_AR.md) · [`DEALIX_AI_OPERATING_COMPANY_AR.md`](DEALIX_AI_OPERATING_COMPANY_AR.md)
- [`COMMERCIAL_CONTROL_TOWER.md`](COMMERCIAL_CONTROL_TOWER.md) · [`NORTH_STAR_METRICS_AR.md`](NORTH_STAR_METRICS_AR.md) · [`OFFER_MATRIX.md`](OFFER_MATRIX.md)
- [`SALES_MOTIONS.md`](SALES_MOTIONS.md) · [`DISCOVERY_SCRIPT.md`](DISCOVERY_SCRIPT.md) · [`OBJECTION_ENGINE.md`](OBJECTION_ENGINE.md) · [`SALES_QA.md`](SALES_QA.md)
- [`OFFER_LEAD_INTELLIGENCE_SPRINT_AR.md`](OFFER_LEAD_INTELLIGENCE_SPRINT_AR.md) · [`DEALIX_STANDARD.md`](DEALIX_STANDARD.md) · [`DEALIX_METHOD.md`](DEALIX_METHOD.md)
- [`DELIVERY_QA.md`](DELIVERY_QA.md) · [`SAMPLE_PROOF_PACK.md`](SAMPLE_PROOF_PACK.md) · [`CUSTOMER_SUCCESS_PLAYBOOK.md`](CUSTOMER_SUCCESS_PLAYBOOK.md)
- [`DEMAND_MODEL.md`](DEMAND_MODEL.md) · [`AEO_STRATEGY.md`](AEO_STRATEGY.md) · [`PARTNER_ONBOARDING_KIT.md`](PARTNER_ONBOARDING_KIT.md)
- [`AFFILIATE_REVIEW_WORKFLOW.md`](AFFILIATE_REVIEW_WORKFLOW.md) · [`PRICING_EXPERIMENTS.md`](PRICING_EXPERIMENTS.md) · [`ENTERPRISE_MOTION.md`](ENTERPRISE_MOTION.md)
- [`HOMEPAGE_CONVERSION_ARCHITECTURE.md`](HOMEPAGE_CONVERSION_ARCHITECTURE.md) · [`REVENUE_TRUTH_LABELS.md`](REVENUE_TRUTH_LABELS.md) · [`CODE_MAP_OS_TO_MODULES_AR.md`](CODE_MAP_OS_TO_MODULES_AR.md)

---

*القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value.*
