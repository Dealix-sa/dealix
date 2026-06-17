# Product Family Map — Dealix Offer Ladder — خريطة عائلة العروض

This document maps the Dealix offer family: what each rung is, who it is for, the gate that unlocks the next rung, and its status. It does not set prices — the only binding prices live in [`../01_go_to_market/PRICE_AUTHORITY.md`](../01_go_to_market/PRICE_AUTHORITY.md). It does not set readiness — the only binding statuses live in [`MODULE_STATUS_MAP.md`](./MODULE_STATUS_MAP.md). For the identity behind the family, see [`PLATFORM_SOURCE_OF_TRUTH.md`](./PLATFORM_SOURCE_OF_TRUTH.md).

يرسم هذا المستند عائلة عروض Dealix: ما هي كل درجة، ولمن، والبوّابة التي تفتح الدرجة التالية، وحالتها. لا يحدّد الأسعار — الأسعار المُلزِمة الوحيدة في [`../01_go_to_market/PRICE_AUTHORITY.md`](../01_go_to_market/PRICE_AUTHORITY.md). ولا يحدّد الجاهزية — الحالات المُلزِمة الوحيدة في [`MODULE_STATUS_MAP.md`](./MODULE_STATUS_MAP.md). ولهوية العائلة راجع [`PLATFORM_SOURCE_OF_TRUTH.md`](./PLATFORM_SOURCE_OF_TRUTH.md).

---

## 1. The ladder at a glance — السُّلّم في لمحة

| Rung | Offer | Status |
|---|---|---|
| 0 | Free Diagnostic / تشخيص مجاني | LIVE |
| 1 | Command Sprint (7 days) / سبرنت القيادة | LIVE |
| 2 | Data-to-Revenue Pack / حزمة البيانات إلى الإيراد | BETA |
| 3 | Managed Business OS — Starter Command / Business Ops | BETA |
| 4 | Custom AI Service Setup / تهيئة خدمة AI مخصّصة | INTERNAL |
| 5 | Enterprise / Partner / مؤسسات وشركاء | FUTURE |

Prices for every rung are quoted only from [`PRICE_AUTHORITY.md`](../01_go_to_market/PRICE_AUTHORITY.md). No rung is offered before its gate is cleared.

تُقتبس أسعار كل درجة فقط من [`PRICE_AUTHORITY.md`](../01_go_to_market/PRICE_AUTHORITY.md). ولا تُعرض أي درجة قبل اجتياز بوّابتها.

---

## 2. Rung 0 — Free Diagnostic — التشخيص المجاني

- **What it is:** A short, founder-led diagnostic call that maps one real opportunity and one bottleneck. No deliverable file, no external action. ما هو: مكالمة تشخيص قصيرة يقودها المؤسس ترسم فرصة حقيقية واحدة وعنق زجاجة واحداً. بلا ملف تسليم ولا فعل خارجي.
- **Who it is for:** Saudi B2B service companies evaluating whether the Sprint is worth a paid step. لمن: شركات الخدمات السعودية B2B التي تقيّم ما إذا كان السبرنت يستحق خطوة مدفوعة.
- **Gate to next rung:** A named opportunity plus the customer's stated intent to run the Sprint. البوّابة للدرجة التالية: فرصة مُسمّاة مع نيّة معلنة من العميل لتشغيل السبرنت.
- **Status:** LIVE. الحالة: LIVE.

---

## 3. Rung 1 — Command Sprint — سبرنت القيادة

- **What it is:** The shipped wedge — a 7-day engagement that runs the full loop once: see, decide, execute, prove. It produces a Command Pack and a Proof Pack. Detailed scope lives in [`../01_go_to_market/COMMAND_SPRINT_OFFER.md`](../01_go_to_market/COMMAND_SPRINT_OFFER.md). ما هو: الإسفين المُطلَق — ارتباط مدّته 7 أيام يُشغّل الحلقة كاملة مرة واحدة: يرى، يقرّر، ينفّذ، يُثبت. ينتج Command Pack وProof Pack.
- **Who it is for:** A single paying Saudi B2B company ready to test the loop on one real opportunity. لمن: شركة سعودية B2B واحدة تدفع وجاهزة لاختبار الحلقة على فرصة حقيقية واحدة.
- **Gate to next rung:** A delivered Proof Pack (non-negotiable #10) and confirmation the weekly rhythm is useful. البوّابة للدرجة التالية: Proof Pack مُسلَّم (البند #10) وتأكيد أن الإيقاع الأسبوعي مفيد.
- **Status:** LIVE. The 499 is a proof gate, not the company's price — see [`PRICE_AUTHORITY.md`](../01_go_to_market/PRICE_AUTHORITY.md) §2 for the progression. الحالة: LIVE. الـ499 بوّابة إثبات وليست سعر الشركة.

---

## 4. Rung 2 — Data-to-Revenue Pack — حزمة البيانات إلى الإيراد

- **What it is:** A standalone data and targeting package built from sourced, consented inputs — the Market Intelligence output packaged for a customer who wants the list and the map without the full Sprint. No scraping; consent and retention governed by Data OS. ما هو: حزمة بيانات واستهداف قائمة بذاتها مبنية على مدخلات مُوثَّقة وبموافقة — مخرَج استخبارات السوق مُحزَّماً لعميل يريد القائمة والخريطة دون السبرنت الكامل. بلا كشط؛ والموافقة والاحتفاظ يحكمهما نظام البيانات.
- **Who it is for:** Customers with their own sales capacity who need the opportunity map, not the delivery. لمن: عملاء لديهم قدرة مبيعات خاصة ويحتاجون خريطة الفرص لا التسليم.
- **Gate to next rung:** Evidence the pack drove at least one qualified conversation, plus interest in an ongoing rhythm. البوّابة للدرجة التالية: دليل أن الحزمة أنتجت محادثة مؤهّلة واحدة على الأقل، مع اهتمام بإيقاع مستمر.
- **Status:** BETA — usable in a controlled trial only. الحالة: BETA — قابلة للتجربة المحكومة فقط.

---

## 5. Rung 3 — Managed Business OS — النظام المُدار للأعمال

Two tiers, both BETA. Never offered before the customer has paid for a Sprint, received a Command Pack, and confirmed the rhythm is useful (see [`PRICE_AUTHORITY.md`](../01_go_to_market/PRICE_AUTHORITY.md) §3).

باقتان، كلاهما BETA. لا تُعرضان أبداً قبل أن يدفع العميل سبرنت، ويستلم Command Pack، ويؤكد أن الإيقاع مفيد.

- **Starter Command:** Command + Revenue + Proof, run on a monthly rhythm. For a company that wants the loop kept running on one workstream. القيادة + الإيراد + الإثبات على إيقاع شهري. لشركة تريد إبقاء الحلقة تعمل على مسار واحد.
- **Business Ops:** adds Client + Delivery for a company running multiple workstreams. تضيف العميل + التسليم لشركة تدير مسارات متعددة.
- **Who it is for:** Proven Sprint customers who want the loop managed continuously, not one-off. لمن: عملاء سبرنت مُثبَتون يريدون إدارة الحلقة باستمرار لا مرة واحدة.
- **Gate to next rung:** Stable monthly rhythm plus a need the standard tiers cannot meet (custom integration, training, SLA). البوّابة للدرجة التالية: إيقاع شهري مستقر مع حاجة لا تلبّيها الباقات القياسية.
- **Status:** BETA. الحالة: BETA.

---

## 6. Rung 4 — Custom AI Service Setup — تهيئة خدمة AI مخصّصة

- **What it is:** A one-time build that tailors the operating loop to a specific company's workflow, plus a monthly support fee. Still founder-and-team operated. ما هو: بناء لمرة واحدة يفصّل حلقة التشغيل على سير عمل شركة محدّدة، مع رسم دعم شهري. لا يزال يُشغّله المؤسس والفريق.
- **Who it is for:** Managed customers whose needs exceed the standard tiers. لمن: عملاء مُدارون تتجاوز احتياجاتهم الباقات القياسية.
- **Gate to next rung:** Repeatable, documented setup patterns and a partner-ready delivery runbook. البوّابة للدرجة التالية: أنماط تهيئة موثّقة قابلة للتكرار ودليل تسليم جاهز للشركاء.
- **Status:** INTERNAL — scaffolding exists for founder use; not a public offer. الحالة: INTERNAL — هيكل قائم لاستخدام المؤسس؛ ليس عرضاً عاماً.

---

## 7. Rung 5 — Enterprise / Partner — المؤسسات والشركاء

- **What it is:** Custom engagements with integrations, training, and SLA, and a partner channel that extends delivery through approved partners (Partner OS, Academy OS). ما هو: ارتباطات مخصّصة بتكاملات وتدريب واتفاقية مستوى خدمة، وقناة شركاء توسّع التسليم عبر شركاء معتمدين.
- **Who it is for:** Larger organizations and delivery partners — after the public launch and a referenceable case study exist. لمن: مؤسسات أكبر وشركاء تسليم — بعد توفّر الإطلاق العام ودراسة حالة مرجعية.
- **Gate to unlock:** Public-launch Go and a referenceable anonymized case study (see [`LAUNCH_CONTROL_TOWER.md`](./LAUNCH_CONTROL_TOWER.md) Go/No-Go). البوّابة للفتح: قرار إطلاق عام إيجابي ودراسة حالة مجهولة المصدر مرجعية.
- **Status:** FUTURE — prices are aspirational; never quote as available today. الحالة: FUTURE — الأسعار تطلّعية؛ لا تُقتبس كمتاحة اليوم.

---

## 8. The rule for the whole family — قاعدة العائلة كاملة

No rung is sold before its gate is cleared, no monthly tier before a paid Sprint and a Proof Pack, and no price stated except from [`PRICE_AUTHORITY.md`](../01_go_to_market/PRICE_AUTHORITY.md). Each rung still obeys the operating rule and the 11 non-negotiables: no scraping, no cold automation, no guaranteed outcomes, no external action without approval, no project without a Proof Pack.

لا تُباع أي درجة قبل اجتياز بوّابتها، ولا باقة شهرية قبل سبرنت مدفوع وProof Pack، ولا يُذكر سعر إلا من [`PRICE_AUTHORITY.md`](../01_go_to_market/PRICE_AUTHORITY.md). وكل درجة تخضع لقاعدة التشغيل والبنود الأحد عشر: لا كشط، ولا أتمتة باردة، ولا ضمان نتائج، ولا فعل خارجي بلا موافقة، ولا مشروع بلا Proof Pack.

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
