# Proof Pack Factory — مصنع حزمة الإثبات (Distribution OS v1)

**الغرض:** بناء **حزمة إثبات** (Proof Pack) تُظهر سير العمل الحالي، ونقاط التسرّب، وفرصة الأتمتة، وطريقة القياس المتوقعة — بمستوى إثبات صريح `L0`–`L5`. الحزمة هي ما **يعيد البيع** للمرحلة التالية، والدليل قبل أي توسعة.

**مرجع الكود لمستويات الإثبات:** [`auto_client_acquisition/proof_engine/evidence.py`](../../auto_client_acquisition/proof_engine/evidence.py) (`EvidenceLevel`, الأوصاف AR/EN، و`assert_public_proof_allowed`).

**مراجع:** العرض: [PROPOSAL_FACTORY_AR.md](PROPOSAL_FACTORY_AR.md) · سياسة الجودة: [DRAFT_QUALITY_POLICY_AR.md](DRAFT_QUALITY_POLICY_AR.md) · قالب التسليم: [PROOF_PACK_TEMPLATE.md](../delivery/PROOF_PACK_TEMPLATE.md) · النظرة العامة: [PRODUCT_DISTRIBUTION_OS_AR.md](PRODUCT_DISTRIBUTION_OS_AR.md).

---

## 1) محتويات حزمة الإثبات

| # | المكوّن | ماذا يحتوي |
|---|---------|------------|
| 1 | سير العمل الحالي (current workflow) | كيف تتحرك الفرصة اليوم من دخول الـ lead إلى القرار |
| 2 | نقاط التسرّب (leakage points) | أين تضيع المتابعة، أين لا يوجد next action موثّق |
| 3 | فرصة الأتمتة (automation opportunity) | الخطوة المحدودة القابلة للحوكمة والأتمتة بأمان |
| 4 | طريقة القياس المتوقعة (expected measurement method) | كيف نقيس قبل/بعد — لا أرقام مخترعة |
| 5 | قائمة قبل/بعد (before/after checklist) | حالة الحقول/الخطوات قبل التدخل وبعده |
| 6 | مستوى الإثبات (evidence level) | `L0`–`L5` — انظر §2 |
| 7 | الخطوة التالية (next action) | القرار الواضح للمرحلة التالية |

> قاعدة: المقاييس في الحزمة **طريقة قياس**، لا وعد بنتيجة. الأرقام الفعلية تأتي من تشغيل/أدلة، لا من المولّد.

---

## 2) مستويات الإثبات (L0–L5)

المعاني **الدقيقة** كما في `evidence.py`:

| المستوى | الرمز | المعنى (AR) | المعنى (EN) |
|---------|-------|-------------|-------------|
| L0 | `L0_PLANNED` | مخطط — لم يُنفَّذ بعد | Planned — not executed |
| L1 | `L1_INTERNAL_DRAFT` | مسودة داخلية — غير جاهزة للعميل | Internal draft — not customer-ready |
| L2 | `L2_CUSTOMER_REVIEWED` | راجعها العميل — خاص | Customer reviewed — private |
| L3 | `L3_CUSTOMER_APPROVED` | وافق العميل — دليل مبيعات خاص | Customer approved — private sales proof |
| L4 | `L4_PUBLIC_APPROVED` | موافقة نشر عام — دراسة حالة | Public publish approved — case study |
| L5 | `L5_REVENUE_EXPANSION` | دليل إيراد/توسعة — بعد التزام/دفع | Revenue/expansion evidence — after written commitment / payment |

---

## 3) القاعدة الذهبية: لا تسويق عام دون L4 + موافقة

> **لا تُستخدم أي حزمة إثبات في تسويق عام تحت المستوى L4، وبدون موافقة صريحة للنشر.**

هذا تفرضه الدالة `assert_public_proof_allowed(level, consent_public=...)`:

- إن كان المستوى < L4 → `public_proof_requires_L4_minimum`.
- إن لم تكن هناك موافقة نشر → `public_proof_requires_explicit_consent`.

| الاستخدام | الحد الأدنى |
|-----------|-------------|
| داخلي فقط | L1 |
| مبيعات خاصة (مع العميل) | L3 |
| دراسة حالة عامة / تسويق | **L4 + موافقة نشر** |
| دليل توسعة/إيراد | L5 (بعد التزام كتابي/دفع) |

L0 وL1 **لا يُستخدمان في تسويق خارجي إطلاقاً**.

---

## 4) من الحزمة إلى التوسعة

```text
diagnostic → Proof Pack (L1 داخلي) → مراجعة العميل (L2) → موافقة العميل (L3)
→ [اختياري بموافقة نشر] دراسة حالة (L4) → دليل توسعة بعد دفع (L5)
```

- العرض/الريتينر لا يُبنى على حزمة دون **L3** (دليل مبيعات خاص بالعميل) — انظر [PROPOSAL_FACTORY_AR.md](PROPOSAL_FACTORY_AR.md) §6.
- أي دراسة حالة عامة تحتاج **L4 + موافقة موثّقة**؛ بلا أسماء أو PII دون إذن صريح.

---

## 5) حدود صريحة

- لا نشر عام تحت L4، ولا بدون موافقة — يفرضه الكود.
- لا أرقام نتائج مخترعة؛ المقاييس طريقة قياس أو من أدلة حقيقية.
- لا PII في الحزمة دون موافقة صريحة؛ استخدم تسميات مجهّلة.
- L5 فقط بعد التزام كتابي/دفع حيث ينطبق.

---

> القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.

*يُبنى في هذا الـ PR. آخر تحديث: 2026-06-02.*
