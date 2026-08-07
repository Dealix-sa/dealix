# تسليم الدفع — Dealix Payment Handoff

هذا الملف يحدّد **شروط ما قبل الدفع** وحالاته. الكيان `payment_handoff` يحمل الحقول حرفياً: `id`, `proposal_id`, `customer_id`, `product_id`, `amount_sar`, `status`, `approvals` — وداخل `approvals`: `proposal_approved`, `scope_confirmed`, `price_confirmed`, `decision_maker_confirmed`, `risk_reviewed`, `founder_approved`.

This file defines the **payment preconditions** and states. The `payment_handoff` entity carries the fields above verbatim.

> **لا تحصيل مالي يتم بواسطة الذكاء الاصطناعي.** التسليم للدفع = تجهيز وتأكيد فقط؛ التحصيل عبر مزوّد الدفع وبقرار المؤسس.
>
> **No charging is performed by the AI.** Handoff = preparation and confirmation only; charging happens through the payment provider by founder decision.

روابط / Related: [PROPOSAL_FACTORY_AR.md](PROPOSAL_FACTORY_AR.md) · [PROSPECT_OS_AR.md](PROSPECT_OS_AR.md) · [../commercial/PRICING_GUARDRAILS_AR.md](../commercial/PRICING_GUARDRAILS_AR.md) · [../commercial/APPROVAL_POLICY_AR.md](../commercial/APPROVAL_POLICY_AR.md) · [../delivery/DELIVERY_HANDOFF_AR.md](../delivery/DELIVERY_HANDOFF_AR.md)

---

## الشروط المسبقة / Preconditions (`approvals`)

لا ينتقل العميل إلى الدفع إلا بعد تحقّق **كل** هذه الموافقات؛ كلٌ علم منطقي (boolean) في `approvals`:

A prospect reaches payment only after **all** approvals below hold; each is a boolean in `approvals`:

| المفتاح / Key | الشرط / Condition |
|---|---|
| `proposal_approved` | العرض معتمَد (`proposal.approval_status = approved`). / The proposal is approved. |
| `scope_confirmed` | النطاق وخارج النطاق مؤكَّدان كتابياً. / Scope and out-of-scope confirmed in writing. |
| `price_confirmed` | السعر النهائي مثبَّت داخل الحدود المعتمدة. / Final price fixed within approved bands. |
| `decision_maker_confirmed` | جهة القرار مؤكَّدة (`prospect.decision_maker`). / Decision-maker confirmed. |
| `risk_reviewed` | المخاطر روجِعت ولا مانع امتثالي. / Risk reviewed, no compliance blocker. |
| `founder_approved` | موافقة المؤسس الصريحة على التسليم للدفع. / Explicit founder approval for the handoff. |

> أي علم غير محقَّق ⇒ لا تسليم للدفع. / Any unmet flag ⇒ no handoff.

---

## الحالات / States (`status`)

| الحالة / State | المعنى / Meaning |
|---|---|
| `pending_preconditions` | بعض الموافقات لم تكتمل. / Some approvals incomplete. |
| `ready_for_handoff` | كل الموافقات مكتملة. / All approvals complete. |
| `handed_off` | سُلِّم للمؤسس/مزوّد الدفع للتحصيل. / Handed to the founder/provider for charging. |
| `paid` | تأكَّد الدفع. / Payment confirmed. |
| `failed` | تعذّر الدفع. / Payment failed. |
| `cancelled` | أُلغِي قبل التحصيل. / Cancelled before charging. |

> الانتقال إلى `ready_for_handoff` لا يحدث إلا بعد كل علامات `approvals`. والذكاء الاصطناعي لا يتجاوز `ready_for_handoff` — التحصيل خطوة بشرية. / `ready_for_handoff` requires all approval flags. The AI never proceeds past `ready_for_handoff` — charging is a human step.

---

## التسلسل / Sequence

```text
proposal (approved) → preconditions (all approvals) → ready_for_handoff
→ founder charges via provider → paid → delivery_handoff
```

- عند `paid`، يتحوّل العميل إلى `won` في [PROSPECT_OS_AR.md](PROSPECT_OS_AR.md) ويبدأ [../delivery/DELIVERY_HANDOFF_AR.md](../delivery/DELIVERY_HANDOFF_AR.md). / On `paid`, the prospect becomes `won` and delivery handoff begins.
- `amount_sar` يطابق السعر المعتمَد في العرض؛ لا مبلغ خارج الحدود. / The amount matches the approved proposal price; nothing outside bands.

---

## قواعد ملزمة / Binding rules

1. **لا تحصيل بواسطة الذكاء الاصطناعي** بأي حال. / No charging by the AI under any circumstance.
2. لا تسليم للدفع بلا اكتمال `approvals` الست. / No handoff without all six approvals.
3. `amount_sar` داخل حدود [../commercial/PRICING_GUARDRAILS_AR.md](../commercial/PRICING_GUARDRAILS_AR.md). / Amount within pricing guardrails.
4. لا PII دفع في السجل التشغيلي؛ مرجع فقط. / No payment PII in the operational record; reference only.
5. القرار النهائي بالتحصيل للمؤسس. / The final charging decision belongs to the founder.

---

**القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.**
