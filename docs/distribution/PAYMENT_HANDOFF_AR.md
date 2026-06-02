# Payment Handoff — تسليم الدفع — Payment Handoff

> Purpose — الغرض: يحدّد هذا المستند حالات تسليم الدفع والقاعدة الصارمة: **لا رابط دفع دون عرض مُعتمَد + تثبيت السعر/النطاق/الشروط + موافقة المؤسس**. روابط Moyasar المرجعية تُفعَّل بيد المؤسس فقط (founder-flipped). لا خصم مباشر ولا إرسال آلي لأي رابط دفع.
>
> This document defines payment-handoff states and the strict rule: no payment link without an approved proposal, confirmed price/scope/terms, and founder approval. Reference Moyasar links are founder-flipped only. No live charge, no automated sending of any payment link.

Cross-link — روابط: [PROPOSAL_FACTORY_AR.md](./PROPOSAL_FACTORY_AR.md) · [PROOF_PACK_FACTORY_AR.md](./PROOF_PACK_FACTORY_AR.md) · [RENEWAL_ENGINE_AR.md](./RENEWAL_ENGINE_AR.md) · [../wave6/MANUAL_PAYMENT_CONFIRMATION_CHECKLIST.md](../wave6/MANUAL_PAYMENT_CONFIRMATION_CHECKLIST.md) · [../transformation/CTO_MOYSASAR_PHASE3_GATE_AR.md](../transformation/CTO_MOYSASAR_PHASE3_GATE_AR.md).

---

## 1. القاعدة الصارمة — The strict rule

لا يُجهَّز رابط دفع إلا بعد تحقّق ثلاثة شروط معًا:

A payment link is prepared only after three conditions are met together:

1. **عرض مُعتمَد** — `proposal` بحالة `approved` (راجع [PROPOSAL_FACTORY_AR.md](./PROPOSAL_FACTORY_AR.md)).
2. **تثبيت السعر/النطاق/الشروط** — متّفق عليها كتابيًا مع العميل.
3. **موافقة المؤسس على التسليم** — إقرار صريح على تسليم الدفع نفسه.

وحتى بعد التجهيز، **النظام لا يُرسل الرابط**؛ المؤسس ينسخه ويرسله يدويًا، ثم يقلب الحالة بنفسه.

Even after preparation, the system does not send the link; the founder copies and sends it manually, then flips the state himself.

---

## 2. حالات تسليم الدفع — Payment handoff states

| الحالة — State | المعنى — Meaning |
|---|---|
| `draft` | تسليم دفع مُولَّد، قبل المراجعة |
| `pending_approval` | بانتظار موافقة المؤسس (الشروط الثلاثة تُفحَص هنا) |
| `approved` | اعتمده المؤسس؛ جاهز للنسخ اليدوي |
| `sent` | أرسله المؤسس يدويًا للعميل |
| `paid` | تأكّد الدفع (يقلبها المؤسس يدويًا بعد دليل) |
| `expired` | انتهت صلاحية الرابط دون دفع |
| `cancelled` | أُلغِي التسليم |

### مسار الحالات — State flow

```text
draft → pending_approval → approved → sent → paid
                              ↓          ↓
                          cancelled   expired | cancelled
```

تُخزَّن في `data/revenue_execution/payment_handoffs.jsonl` (قابل للتجاوز عبر `DEALIX_REVX_PAYMENT_HANDOFFS_PATH`).

---

## 3. قاعدة الإيراد — The revenue rule

الإيراد لا يُحتسَب إلا عند `paid` بعد قلب المؤسس اليدوي للحالة استنادًا إلى دليل. الحالات `draft`/`pending_approval`/`approved`/`sent` **ليست إيرادًا**. هذا يطابق قائمة تأكيد الدفع اليدوي (راجع [../wave6/MANUAL_PAYMENT_CONFIRMATION_CHECKLIST.md](../wave6/MANUAL_PAYMENT_CONFIRMATION_CHECKLIST.md)).

Revenue counts only at `paid`, after the founder manually flips the state based on evidence. `draft`/`pending_approval`/`approved`/`sent` are not revenue. This matches the manual payment-confirmation checklist.

| الحالة — State | إيراد؟ — Revenue? |
|---|---|
| `sent` | لا — رابط مُرسَل ليس دفعًا |
| `paid` (بعد دليل + قلب يدوي) | نعم |

---

## 4. روابط Moyasar — Moyasar links

الروابط المرجعية تُفعَّل بيد المؤسس فقط (founder-flipped). لا خصم مباشر (no live charge) — وهذه بوّابة دستورية. النظام لا ينشئ ولا يرسل رابطًا حيًّا؛ أقصى ما يفعله تجهيز مسودة تسليم دفع للموافقة.

Reference links are founder-flipped only. No live charge — a constitutional gate. The system neither creates nor sends a live link; the most it does is prepare a payment-handoff draft for approval.

تفاصيل بوّابة Moyasar: [../transformation/CTO_MOYSASAR_PHASE3_GATE_AR.md](../transformation/CTO_MOYSASAR_PHASE3_GATE_AR.md).

---

## 5. متابعة الدفع — Payment follow-up

بعد قلب الحالة إلى `sent` يدويًا، يولّد المحرّك مسودة `payment_followup` بعد 24 ساعة (راجع [FOLLOWUP_ENGINE_AR.md](./FOLLOWUP_ENGINE_AR.md)). المتابعة مسودة `pending_approval`، لا إرسال آلي.

After the state is manually flipped to `sent`, the engine generates a `payment_followup` draft after 24 hours. The follow-up is a `pending_approval` draft, not an auto-send.

---

## 6. ما لا يفعله النظام — What the system will not do

- لا يرسل رابط دفع دون الشروط الثلاثة (§1) وموافقة المؤسس (البند 8).
- لا ينفّذ خصمًا مباشرًا (no live charge).
- لا يقلب الحالة إلى `paid` تلقائيًا — المؤسس فقط، بعد دليل.
- لا يبدأ تسليم الدفع قبل اعتماد العرض.

The system will not: send a link without the three conditions and founder approval; perform a live charge; auto-flip to `paid`; or begin handoff before proposal approval.

> بدء التسليم — Delivery kickoff: يبدأ فقط عند `paid` أو التزام مكتوب موقّع، تمامًا كما في قائمة تأكيد الدفع اليدوي. وإلا تبقى الحالة محجوبة.

---

> القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value.
