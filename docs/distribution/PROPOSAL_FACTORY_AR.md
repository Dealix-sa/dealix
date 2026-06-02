# Proposal Factory — مصنع العروض — Proposal Factory

> Purpose — الغرض: يحدّد هذا المستند الأقسام الإلزامية لكل عرض، وربطها بالسلّم التجاري الخماسي. العرض مسودة `pending_approval` يقرّها المؤسس ويرسلها يدويًا؛ لا يُرسَل عرض دون مراجعته.
>
> This document defines the required proposal sections and maps them to the 5-rung commercial ladder. A proposal is a `pending_approval` draft the founder approves and sends manually; no proposal is sent unreviewed.

Cross-link — روابط: [PRODUCT_DISTRIBUTION_OS_AR.md](./PRODUCT_DISTRIBUTION_OS_AR.md) · [SECTOR_PRIORITIZATION_AR.md](./SECTOR_PRIORITIZATION_AR.md) · [PROOF_PACK_FACTORY_AR.md](./PROOF_PACK_FACTORY_AR.md) · [PAYMENT_HANDOFF_AR.md](./PAYMENT_HANDOFF_AR.md) · [../03_commercial_mvp/SPRINT_DELIVERY_PLAYBOOK.md](../03_commercial_mvp/SPRINT_DELIVERY_PLAYBOOK.md) · [../../templates/PROPOSAL_REVENUE_INTELLIGENCE_SPRINT.md.j2](../../templates/PROPOSAL_REVENUE_INTELLIGENCE_SPRINT.md.j2).

---

## 1. السلّم التجاري الخماسي — The 5-rung commercial ladder

كل عرض يُربَط بدرجة واحدة على هذا السلّم. لا تُخترَع أسعار خارجه.

Every proposal maps to exactly one rung. No prices are invented outside it.

| الدرجة — Rung | المنتج — Product | السعر — Price | الغرض — Purpose |
|---|---|---|---|
| Rung 0 | Free AI Ops Diagnostic | 0 SAR | إثبات الوجع وفتح العلاقة |
| Rung 1 | 7-Day Revenue Intelligence Sprint | 499 SAR | إثبات قيمة سريع |
| Rung 2 | Data-to-Revenue Pack | 1,500 SAR | تجهيز البيانات للإيراد |
| Rung 3 | Managed Revenue Ops | 2,999–4,999 SAR/mo | تشغيل مُدار شهري |
| Rung 4 | Custom AI Service Setup | 5,000–25,000 SAR + 1,000 SAR/mo | إعداد خدمة مخصّصة |
| Enterprise (slow track) | AI Governance Review | 25,000–50,000 SAR | مراجعة حوكمة مؤسسية |

ترتيب القطاع → أول عرض في [SECTOR_PRIORITIZATION_AR.md](./SECTOR_PRIORITIZATION_AR.md).

---

## 2. الأقسام الإلزامية للعرض — Required proposal sections

كل عرض يحتوي هذه الأقسام بالترتيب. عرض ينقصه أي قسم لا يُعتمَد.

Every proposal contains these sections in order. A proposal missing any section is not approved.

| # | القسم — Section | المحتوى — Content |
|---|---|---|
| 1 | الوضع والوجع — Situation & pain | المشكلة كما وصفها العميل، لا كما نتخيّلها |
| 2 | النطاق — Scope | ما يشمله العرض، بدقّة |
| 3 | الاستثناءات — Exclusions | ما لا يشمله العرض (مهم لإدارة التوقّعات) |
| 4 | المخرجات — Deliverables | قائمة التسليمات الملموسة |
| 5 | الدرجة والسعر — Rung & price | الدرجة على السلّم + السعر الثابت |
| 6 | الجدول الزمني — Timeline | المدّة والمراحل |
| 7 | الإثبات — Proof | كيف تُقاس القيمة + Proof Pack (للمشاريع المدفوعة) |
| 8 | الحدود — Limitations | ما لا يَعِد به العرض (لا مبيعات مضمونة) |
| 9 | الشروط والدفع — Terms & payment | شروط الدفع وتسليم الدفع |
| 10 | الخطوة التالية — Next step | دعوة إجراء واحدة واضحة |

> القسم 8 إلزامي بحدّة — Section 8 is strictly mandatory: لا عرض يَعِد بأرقام مبيعات أو نسب تحويل كحقيقة. نستخدم «فرص مُثبتة بأدلة» و«قيمة تقديرية» (البند 4، 5).

---

## 3. ربط الأقسام بالطبقات — Section-to-layer mapping

- الأقسام 2–4 (النطاق/الاستثناءات/المخرجات) تُغذّى من `sales_os` (أقسام العرض وعارضها).
- القسم 7 (الإثبات) يربط بـ Proof Pack من `proof_os` (راجع [PROOF_PACK_FACTORY_AR.md](./PROOF_PACK_FACTORY_AR.md)).
- القسم 9 (الدفع) يربط بتسليم الدفع (راجع [PAYMENT_HANDOFF_AR.md](./PAYMENT_HANDOFF_AR.md)).
- القيمة المذكورة تتبع تمييز Estimated/Observed/Verified من `value_os`.

Sections 2–4 are fed by `sales_os`; Section 7 links to a `proof_os` Proof Pack; Section 9 links to payment handoff; stated value follows `value_os` Estimated/Observed/Verified discipline.

---

## 4. حالة العرض وموافقته — Proposal state & approval

العرض مسودة من نوع `proposal`، تبدأ `pending_approval` وتحمل `governance_decision` و`evidence_level` (راجع [DRAFT_SYSTEM_SPEC_AR.md](./DRAFT_SYSTEM_SPEC_AR.md)). تُخزَّن في `data/revenue_execution/proposals.jsonl` وتُعرَض في `reports/distribution/PROPOSAL_DRAFT_REPORT.md`.

A proposal is a `proposal`-type draft starting `pending_approval`, carrying a `governance_decision` and `evidence_level`. Stored in `data/revenue_execution/proposals.jsonl`, surfaced in `reports/distribution/PROPOSAL_DRAFT_REPORT.md`.

بعد الموافقة، يُرسَل العرض يدويًا؛ وبعد 48 ساعة تُولَّد متابعة عرض (راجع [FOLLOWUP_ENGINE_AR.md](./FOLLOWUP_ENGINE_AR.md)). لا يبدأ تسليم الدفع إلا بعد اعتماد العرض وتثبيت السعر/النطاق/الشروط (راجع [PAYMENT_HANDOFF_AR.md](./PAYMENT_HANDOFF_AR.md)).

After approval, the proposal is sent manually; after 48 hours a proposal follow-up is generated. Payment handoff begins only after the proposal is approved and price/scope/terms are confirmed.

---

## 5. ربط الإثبات الإلزامي — Mandatory proof link

أي عرض مدفوع (Rung 1 وما فوق) يلتزم بأن المشروع سيُنتج Proof Pack (البند 10) وأصلًا رأسماليًا (البند 11). يُذكَر هذا صراحةً في القسم 7.

Any paid proposal (Rung 1 and above) commits that the project will produce a Proof Pack (non-negotiable #10) and a Capital Asset (#11). This is stated explicitly in Section 7.

---

> القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value.
