# محرك التجديد — Dealix Renewal Engine

هذا الملف يحدّد **سلم البيع الإضافي** و**متى يظهر التجديد**. الكيان `renewal` يحمل الحقول حرفياً: `schedule_id`, `customer_id`, `plan`, `amount_sar`, `next_attempt_at`, `status` — ويعيد استخدام مفردات `renewal_scheduler` القائمة.

This file defines the **upsell ladder** and **when renewal appears**. The `renewal` entity reuses the existing `renewal_scheduler` vocabulary.

روابط / Related: [../commercial/OFFER_LADDER_AR.md](../commercial/OFFER_LADDER_AR.md) · [PROOF_PACK_FACTORY_AR.md](PROOF_PACK_FACTORY_AR.md) · [../commercial/PRICING_GUARDRAILS_AR.md](../commercial/PRICING_GUARDRAILS_AR.md) · [../delivery/DELIVERY_HANDOFF_AR.md](../delivery/DELIVERY_HANDOFF_AR.md) · [PAYMENT_HANDOFF_AR.md](PAYMENT_HANDOFF_AR.md)

---

## متى يظهر التجديد / When renewal appears

التجديد **لا يظهر** إلا بعد:

Renewal **appears only** after:

1. **دورة قيمة مكتملة** على المنتج الحالي (تسليم مقبول). / A completed value cycle on the current product (accepted delivery).
2. **حزمة دليل** بمستوى كافٍ (`evidence_level ≥ L3`) من [PROOF_PACK_FACTORY_AR.md](PROOF_PACK_FACTORY_AR.md). / A proof pack at a sufficient level.
3. **اقتراب نهاية الدورة** للاشتراكات الشهرية (`next_attempt_at`). / Cycle-end approaching for monthly plans.

> لا عرض تجديد مبني على وعد؛ التجديد يستند إلى قيمة موثَّقة. / No renewal pitch built on a promise; renewal rests on documented value.

---

## سلم البيع الإضافي / The upsell ladder

يعيد استخدام درجات [../commercial/OFFER_LADDER_AR.md](../commercial/OFFER_LADDER_AR.md) — التجديد قد يكون **تمديداً** لنفس المنتج أو **ترقية** للدرجة الأعلى بعد دليل:

Reuses the rungs in the offer ladder — renewal may be an **extension** of the same product or an **upgrade** to the next rung after proof:

| المنتج الحالي / Current | تمديد / Extend | ترقية بعد دليل / Upgrade after proof |
|---|---|---|
| العمليات المُدارة / Managed Ops | تجديد شهري بنفس السعر | حل ذكاء اصطناعي مخصص / Custom AI |
| Pilot Conversion | — (محدود المدة) | Monthly RevOps OS |
| Monthly RevOps OS — Starter | تجديد Starter | Growth (25k) ثم Scale (35k+) |
| Monthly RevOps OS — Growth | تجديد Growth | Scale (35k+) / Enterprise |
| Monthly RevOps OS — Scale | تجديد Scale | Enterprise AI Revenue OS |

> كل تجديد/ترقية مربوط بمنتج وسعر داخل [../commercial/PRICING_GUARDRAILS_AR.md](../commercial/PRICING_GUARDRAILS_AR.md). / Every renewal/upgrade links to a product and a price within guardrails.

---

## الحالات / States (`status`) — من `renewal_scheduler`

| الحالة / State | المعنى / Meaning |
|---|---|
| `scheduled` | محاولة تجديد مجدولة على `next_attempt_at`. / A renewal attempt scheduled. |
| `awaiting_founder` | بانتظار مراجعة وتأكيد المؤسس (السلوك الافتراضي للشهر الأول). / Awaiting founder review and confirm (default month-1 behavior). |
| `confirmed` | أكّد المؤسس الدورة يدوياً. / Founder manually confirmed the cycle. |
| `skipped` | تُخطِّيت الدورة (سبب موثَّق). / Cycle skipped (documented reason). |
| `failed` | تعذّر التجديد. / Renewal failed. |
| `auto_charged` | تحصيل تلقائي عبر مزوّد الدفع — **بعد** 3 دورات مؤكَّدة يدوياً فقط. / Auto-charged via the provider — only after 3 manually confirmed cycles. |

> حتى `auto_charged` يبقى ضمن اشتراك مزوّد الدفع وبتأهيل مسبق من المؤسس؛ الذكاء الاصطناعي لا يحصّل ولا يبدأ تحصيلاً. / Even `auto_charged` stays within the provider's subscription and prior founder eligibility; the AI neither charges nor initiates charging.

---

## التسلسل / Sequence

```text
delivery accepted → proof pack (L≥3) → renewal scheduled
→ awaiting_founder → confirmed (manual) ×3 → auto_charge_eligible
```

- الشهور الأولى: `awaiting_founder` ثم `confirmed` بقرار المؤسس لكل دورة. / Early months: `awaiting_founder` then founder-confirmed per cycle.
- بعد 3 تأكيدات يدوية، يصبح العميل مؤهَّلاً لـ `auto_charged` عبر اشتراك المزوّد. / After 3 manual confirms, the customer becomes eligible for `auto_charged`.

---

## قواعد ملزمة / Binding rules

1. لا تجديد بلا دليل بمستوى كافٍ. / No renewal without sufficient evidence.
2. لا ترقية درجة بلا شروط [../commercial/OFFER_LADDER_AR.md](../commercial/OFFER_LADDER_AR.md). / No rung upgrade without the ladder conditions.
3. لا تحصيل يبدأه الذكاء الاصطناعي؛ التأكيد المبكر للمؤسس. / No AI-initiated charging; early confirmation is the founder's.
4. السعر داخل الحدود المعتمدة دائماً. / Price always within approved bands.
5. لا ضمان نتائج في عرض التجديد. / No guaranteed results in the renewal pitch.

---

**القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.**
