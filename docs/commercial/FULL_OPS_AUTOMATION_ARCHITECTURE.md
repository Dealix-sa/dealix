<!-- Owner: Founder | Date: 2026-05-18 | Launch Master Plan -->

# معمارية الأتمتة الكاملة — Full-Ops Automation Architecture

> **الثابت الجوهري:** الأتمتة **تُولّد وتُجمّع**؛ الإنسان **يوافق ويُرسِل ويُحصِّل**.
> لا live send، لا live charge، لا إجراء خارجي ذاتي.
> **Core invariant:** Automation generates and assembles; humans approve and send/charge.
> No live send, no live charge, no autonomous external action.

> **إفصاح:** «Full-Ops» تعني أتمتة كل سير عمل داخلي حتى — وليس بعد — بوابة الموافقة البشرية.
> Full-Ops = automate every internal workflow up to, never past, the human-approval gate.

---

## النطاق / Scope

يصف هذا الملف **معمارية الأتمتة الكاملة** لـ Dealix: المعمارية ثلاثية الطبقات لـ RevOps (Data → Process → Technology)، ودورة الحياة المؤتمتة من التقاط الـ lead حتى التجديد، والمكان الدقيق الذي تجلس فيه بوابة الموافقة البشرية في كل خطوة. الملف **تصميمي** — يُصمَّم الآن وتُبنى مكوّناته عند فتح بوابة كل محرك، خاصة G2 (Full-Ops Automation). الملف يعمل ضمن **Commercial Freeze** النشط ([COMMERCIAL_FREEZE.md](../ops/COMMERCIAL_FREEZE.md)): التجميد هو آلية الحوكمة — لا تُبنى أتمتة جديدة لدرجات 2–5 حتى يفتح طلب حقيقي بوابتها.

This document defines Dealix's Full-Ops automation architecture: the three-layer RevOps stack, the automated lead-to-renewal lifecycle, and the exact placement of the human-approval gate at every step. It is a design document; components build when each engine's gate opens. It invents no prices — the canonical source is [OFFER_LADDER_AND_PRICING.md](../OFFER_LADDER_AND_PRICING.md).

---

## 1) المعمارية ثلاثية الطبقات — The 3-Layer RevOps Architecture

أتمتة RevOps الموثوقة تُبنى على ثلاث طبقات متتابعة. لا قفز فوق طبقة: بيانات غير نظيفة تُفسد العملية، وعملية غير معيارية تُفسد التقنية.

| الطبقة / Layer | الغرض | المكوّن الجوهري |
|----------------|-------|------------------|
| **Data layer** — طبقة البيانات | مصدر حقيقة واحد للـ leads والحسابات والاشتراكات | Source Passport لكل lead، consent table، لا PII في السجلات |
| **Process layer** — طبقة العملية | مراحل معيارية قابلة للتدقيق والتكرار | معيار SOAEN، بوابات QA، Revenue Truth Labels على كل مخرَج |
| **Technology layer** — طبقة التقنية | تنفيذ الأتمتة ضمن حوكمة | FastAPI routers + cron scripts + scheduled agents تحت `governance_os` و`tool_guardrail_gateway` |

### 1.1 طبقة البيانات — Data Layer

- **مصدر حقيقة واحد:** كل lead وحساب واشتراك يعيش في سجل واحد — لا نسخ متضاربة.
- **Source Passport لكل lead:** كل lead يحمل جواز مصدر يُسجّل من أين جاء، وفق `source_registry` و`forbidden_sources` — لا scraping، لا قوائم مشتراة.
- **Consent table:** جدول قبول صريح يربط كل lead بموافقته على التواصل وعلى الدفع — لا تواصل ولا شحن بلا قيد في هذا الجدول.
- **لا PII في السجلات:** السجلات (logs) تحمل معرّفات مجهّلة لا بريداً ولا هاتفاً ولا هوية وطنية ولا أسماء حقيقية.

The data layer is one source of truth. Every lead carries a Source Passport governed by the source registry; a consent table binds every lead to explicit communication and payment consent; logs carry anonymized identifiers, never PII.

### 1.2 طبقة العملية — Process Layer

- **معيار SOAEN:** كل سير عمل يحمل الحقول الخمسة Source → Owner → Approval → Evidence → Next Action قبل أن يُعدّ تشغيلاً. التفاصيل: [DEALIX_STANDARD.md](DEALIX_STANDARD.md).
- **بوابات QA:** لا مخرَج موجّه للعميل يصدر بدون مراجعة QA بشرية.
- **Revenue Truth Labels:** كل رقم وكل ادعاء يحمل تسمية تكشف نوع دليله (Estimate / Observed / Client-confirmed / Payment-confirmed / Repeated workflow / Retainer-ready). التفاصيل: [REVENUE_TRUTH_LABELS.md](REVENUE_TRUTH_LABELS.md).

The process layer standardizes every stage via the SOAEN standard, enforces QA gates, and stamps a Revenue Truth Label on every output.

### 1.3 طبقة التقنية — Technology Layer

- **FastAPI routers:** المسارات القائمة (`api/routers/`) تستقبل الـ leads وتدير الـ pipeline.
- **Cron scripts:** سكربتات مجدولة (عائلة `dealix_*_pack`) تجمّع التقارير والحزم.
- **Scheduled agents تحت حوكمة:** كل وكيل مجدول يمرّ عبر `governance_os` و`tool_guardrail_gateway` — لا أداة تتجاوز حاجز الحوكمة.

The technology layer reuses existing FastAPI routers, cron scripts, and scheduled agents — all running under the `governance_os` and `tool_guardrail_gateway` governance modules.

---

## 2) دورة الحياة المؤتمتة — The Automated End-to-End Lifecycle

دورة الحياة الكاملة: التقاط → تأهيل → تشخيص → صياغة → تجميع Proof Pack → تجهيز فاتورة → تسليم → onboarding → تجديد. الأتمتة **تجهّز** كل خطوة؛ بوابة الموافقة البشرية تجلس عند كل إجراء خارجي ومالي.

| المرحلة / Stage | مُؤتمت (Automated) | بوابة بشرية (Human-gated) | المحرك المالك |
|-----------------|---------------------|----------------------------|----------------|
| Lead capture — التقاط | استقبال الـ lead، Source Passport، قيد consent | — (داخلي) | E3 Diagnostic & Intake |
| Qualification — تأهيل | dedupe، scoring، تصنيف ICP | — (داخلي) | E1 Revenue Activation |
| Diagnostic — تشخيص | تشغيل التشخيص المجاني، توليد تقرير صفحة واحدة | مراجعة المؤسس قبل التسليم | E3 Diagnostic & Intake |
| Drafting — صياغة المسودات | توليد مسودات عروض ومسودات outreach | **موافقة بشرية قبل أي إرسال (no live send)** | E2 Founder Sales |
| Proof pack assembly — تجميع حزمة الأدلة | تجميع المخرجات، إلصاق Revenue Truth Labels | **بوابة QA + موافقة المؤسس** | E4 Proof |
| Invoice prep — تجهيز الفاتورة | توليد payment link وفاتورة مرتبطة بـ SOW | **موافقة المؤسس + قبول صريح من العميل (no live charge)** | E6 Billing & Finance |
| Delivery — التسليم | تجميع تقرير التسليم والحزمة النهائية | **بوابة QA قبل التسليم للعميل** | E5 Delivery |
| Onboarding — الإدماج | تجهيز قائمة إدماج ووصول للمنصة | موافقة المؤسس على تفعيل الوصول | E10 CS & Expansion |
| Renewal — التجديد | مسودة تذكير تجديد ومسودة dunning | **قبول صريح متجدد من العميل (no live charge)** | E6 Billing & Finance |

**القراءة الصحيحة للجدول:** كل خطوة «داخلية» تُؤتمت بالكامل. كل خطوة فيها **إرسال خارجي** أو **تحصيل مالي** أو **مخرَج موجّه للعميل** تتوقف عند بوابة بشرية. الأتمتة لا تتجاوز هذه البوابات أبداً.

The lifecycle automates every internal step. Every step involving an external send, a charge, or a customer-facing output stops at a human gate. Automation never crosses these gates.

---

## 3) الثابت الجوهري وكيف يُفرَض — The Core Invariant & Enforcement

**الثابت:** الأتمتة تُولّد وتُجمّع؛ الإنسان يوافق ويُرسِل ويُحصِّل.

هذا الثابت ليس وعداً تحريرياً — هو مفروض باختبارات حوكمة:

| الاختبار / Test | ما يفرضه |
|------------------|----------|
| `no_live_send` | لا مسار يُرسل رسالة خارجية بدون موافقة بشرية مسجّلة |
| `no_live_charge` | لا مسار يخصم من بطاقة عميل بدون قبول صريح موثّق |
| `governance` (governance_os) | كل إجراء وكيل يمرّ عبر `tool_guardrail_gateway` — لا تجاوز للحاجز |

أي تغيير يكسر أحد هذه الاختبارات يُرفَض في CI. هذا هو السبب في أن «Full-Ops» تظل آمنة مهما اتسعت الأتمتة: التوسّع يحدث **داخل** البوابات، لا حولها.

The invariant is enforced by the `no_live_send`, `no_live_charge`, and governance tests. Any change that breaks them is rejected in CI. Full-Ops scales inside the gates, never around them.

---

## 4) الـ non-negotiables داخل المعمارية — Non-Negotiables in the Architecture

المعمارية هي المكان الذي تُنفَّذ فيه الـ11 non-negotiable عملياً:

- **لا scraping / لا قوائم مشتراة** — مفروض في طبقة البيانات عبر Source Passport و`forbidden_sources`.
- **لا cold WhatsApp / LinkedIn automation** — لا قناة خارجية في طبقة التقنية بلا بوابة موافقة.
- **لا fake proof / لا ادعاء بلا مصدر** — مفروض في طبقة العملية عبر Revenue Truth Labels و SOAEN.
- **لا وعد ROI أو نتائج مضمونة** — كل رقم تقديري يحمل تسمية Estimate.
- **لا PII في السجلات** — مفروض في طبقة البيانات.
- **لا مخرَج AI للعميل بلا QA** — بوابة QA في طبقة العملية.
- **لا live send / لا live charge / لا إجراء خارجي بلا موافقة / لا تقدّم مرحلة بلا دليل** — مفروض في دورة الحياة وباختبارات الحوكمة.

---

## روابط داخلية / Cross-links

- [DEALIX_STANDARD.md — معيار SOAEN](DEALIX_STANDARD.md)
- [REVENUE_TRUTH_LABELS.md — تسميات حقيقة الإيراد](REVENUE_TRUTH_LABELS.md)
- [Financial Model — النموذج المالي وآلة المال](FINANCIAL_MODEL.md)
- [Agent Operating Model — نموذج التشغيل والوكلاء](AGENT_OPERATING_MODEL.md)
- [Launch & Scale Master Plan — الخطة الرئيسية](LAUNCH_MASTER_PLAN.md)
- [Commercial Freeze — آلية الحوكمة](../ops/COMMERCIAL_FREEZE.md)
- [Offer Ladder & Pricing — المصدر القانوني للأسعار](../OFFER_LADDER_AND_PRICING.md)

---

*القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value.*
