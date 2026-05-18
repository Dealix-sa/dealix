# Interim Bank-Transfer Cash Path — مسار التحصيل المؤقت بالتحويل البنكي

<!-- Owner: Founder (Sami) | Last reviewed: 2026-05-18 | Workstream G -->

> **Audience.** The founder. This is how Dealix takes money **today**,
> without Moyasar live charges, while the Moyasar KYC is still pending
> (`MOYASAR_GO_LIVE.md`). It is a manual bank-transfer flow mapped exactly
> onto the existing `payment_ops` state machine in code — no new endpoints,
> no new code.
>
> **الجمهور.** المؤسس. هذه طريقة تحصيل Dealix للمال **اليوم** دون شحن مباشر
> عبر ميسر، بينما لا يزال اعتماد KYC قيد الانتظار (`MOYASAR_GO_LIVE.md`).
> إنها مسار تحويل بنكي يدوي مُسقَط حرفياً على آلة حالة `payment_ops` الموجودة
> في الكود — بلا endpoints جديدة وبلا كود جديد.

> **Freeze note.** This runbook supports the rung 0–1 delivery finish, which
> the Commercial Freeze (`../ops/COMMERCIAL_FREEZE.md`) explicitly permits.
> The first paid step is the 499 SAR 7-Day Revenue Proof Sprint
> (`../CANONICAL_PRODUCT_NARRATIVE.md`). No guaranteed-outcome language.

---

## 1. Why this path — لماذا هذا المسار

**EN.** Card activation through Moyasar is the one hard revenue blocker and
depends on a manual KYC action only the founder can complete. It does not
need to block revenue. The `payment_ops` state machine already supports a
`bank_transfer` method that requires no live-charge env flip. The founder
sends bank details, the customer transfers, the founder records the receipt
as manual evidence and confirms. Revenue is real and audit-linked to
delivery — without Moyasar.

**AR.** تفعيل البطاقة عبر ميسر هو القيد الصعب الوحيد على الإيراد، ويعتمد على
إجراء KYC يدوي لا ينجزه سوى المؤسس. لا داعي لأن يوقف الإيراد. آلة حالة
`payment_ops` تدعم أصلاً طريقة `bank_transfer` التي لا تتطلب قلب بيئة الشحن
المباشر. يرسل المؤسس بيانات البنك، يحوّل العميل، ثم يسجّل المؤسس الإيصال
كإثبات يدوي ويؤكّد. الإيراد حقيقي ومرتبط تدقيقياً بالتسليم — دون ميسر.

---

## 2. The state machine — آلة الحالة

**EN.** Defined in `auto_client_acquisition/payment_ops/orchestrator.py`
(`_TRANSITIONS` truth table). The bank-transfer path walks these states:

| State | Meaning | EN |
|---|---|---|
| `invoice_intent` | Invoice created — **not revenue** | starting state |
| `invoice_sent_manual` | Bank details sent to customer | manual send |
| `payment_pending` | Waiting on the customer's transfer | optional waypoint |
| `payment_evidence_uploaded` | Transfer receipt recorded | evidence in |
| `payment_confirmed` | Founder confirmed — **this is revenue** | revenue |
| `delivery_kickoff` | Delivery unlocked | Sprint can run |

`voided` and `refunded` are terminal exits. The hard rule in the router
header: `invoice_created != revenue`; `payment_confirmed = revenue` (only
after an `evidence_reference`); delivery starts only after
`payment_confirmed`.

**AR.** مُعرَّفة في `auto_client_acquisition/payment_ops/orchestrator.py`
(جدول `_TRANSITIONS`). مسار التحويل البنكي يمرّ بهذه الحالات:

| الحالة | المعنى |
|---|---|
| `invoice_intent` | أُنشئت الفاتورة — **ليست إيراداً** |
| `invoice_sent_manual` | أُرسلت بيانات البنك للعميل |
| `payment_pending` | بانتظار تحويل العميل (محطة اختيارية) |
| `payment_evidence_uploaded` | سُجّل إيصال التحويل |
| `payment_confirmed` | أكّد المؤسس — **هذا هو الإيراد** |
| `delivery_kickoff` | فُتح التسليم |

`voided` و`refunded` مخرجان نهائيان. القاعدة الصارمة: إنشاء الفاتورة ليس
إيراداً؛ `payment_confirmed` هو الإيراد (فقط بعد `evidence_reference`)؛
التسليم يبدأ فقط بعد `payment_confirmed`.

---

## 3. Step-by-step flow — الخطوات بالتفصيل

The endpoints below are the real ones in `api/routers/payment_ops.py`.

### Step 1 — Create the invoice intent — إنشاء نية الفاتورة

**EN.** `POST /api/v1/payment-ops/invoice-intent`

```json
{
  "customer_handle": "<customer name>",
  "amount_sar": 499,
  "method": "bank_transfer"
}
```

Save the returned `payment_id`. The response includes
`warning_invoice_not_revenue: "invoice_intent != revenue"` — an invoice is
not money. Use `method: "bank_transfer"`; this path never touches
`moyasar_live`, so the `NO_LIVE_CHARGE` gate is irrelevant here.

**AR.** احفظ `payment_id` العائد. الرد يتضمّن تنبيه أن الفاتورة ليست إيراداً.
استخدم `method: "bank_transfer"`؛ هذا المسار لا يمسّ `moyasar_live` إطلاقاً.

### Step 2 — Send the IBAN / bank details — إرسال بيانات التحويل

**EN.** Send the customer the **business** account name, IBAN, and bank,
plus a clear reference to put on the transfer (use the `payment_id` or the
customer handle). The amount must match the invoice; for the Sprint that is
499 SAR. Send this from the founder's own channel — Dealix never sends
external messages without explicit founder approval. This is the
`invoice_sent_manual` state of the machine; the founder records the send.

**AR.** أرسل للعميل اسم حساب **المنشأة** والـIBAN واسم البنك، مع مرجع واضح
يُكتب على التحويل (استخدم `payment_id` أو اسم العميل). يجب أن يطابق المبلغ
الفاتورة؛ للـSprint هو 499 ريال. أرسلها من قناة المؤسس نفسه — Dealix لا
يرسل رسائل خارجية دون موافقة صريحة من المؤسس. هذه حالة `invoice_sent_manual`.

### Step 3 — Customer transfers — تحويل العميل

**EN.** The customer makes the bank transfer. While waiting, the payment is
in `payment_pending` (or still `invoice_sent_manual`). Do nothing automated;
just wait for the receipt.

**AR.** يُجري العميل التحويل. أثناء الانتظار تكون الدفعة في `payment_pending`
(أو ما زالت `invoice_sent_manual`). لا إجراء آلي؛ فقط انتظر الإيصال.

### Step 4 — Record the transfer receipt as manual evidence — تسجيل الإيصال كإثبات يدوي

**EN.** When the customer sends the bank-transfer receipt, record it:

`POST /api/v1/payment-ops/manual-evidence`

```json
{
  "payment_id": "<id from step 1>",
  "evidence_reference": "<bank reference / receipt number>"
}
```

`evidence_reference` must be at least 5 characters — use the bank
transaction reference number. The state advances to
`payment_evidence_uploaded`. This **records** the evidence; it is **not**
revenue yet — confirmation is a separate human step on purpose.

**AR.** عند استلام إيصال التحويل سجّله عبر `manual-evidence`. يجب أن يكون
`evidence_reference` خمسة أحرف على الأقل — استخدم رقم مرجع المعاملة البنكية.
تتقدّم الحالة إلى `payment_evidence_uploaded`. هذا **يسجّل** الإثبات؛ وليس
إيراداً بعد — التأكيد خطوة بشرية منفصلة بشكل مقصود.

### Step 5 — Founder confirms the payment — تأكيد المؤسس للدفعة

**EN.** After verifying the funds actually landed in the business bank
account:

`POST /api/v1/payment-ops/confirm`

```json
{
  "payment_id": "<id>",
  "confirmed_by": "<founder name>"
}
```

The orchestrator refuses to confirm unless an `evidence_reference` exists
and the state is `payment_evidence_uploaded`. On success the state becomes
`payment_confirmed` and the response carries `is_revenue_now: true`. **This
is the moment revenue is real.**

**AR.** بعد التحقّق من وصول المبلغ فعلياً إلى حساب المنشأة، نفّذ `confirm`.
يرفض المُنسِّق التأكيد ما لم يوجد `evidence_reference` وتكن الحالة
`payment_evidence_uploaded`. عند النجاح تصبح الحالة `payment_confirmed`
ويحمل الرد `is_revenue_now: true`. **هذه هي لحظة تحقّق الإيراد.**

### Step 6 — Kick off delivery — بدء التسليم

**EN.** `POST /api/v1/payment-ops/{payment_id}/kickoff-delivery`

The state moves to `delivery_kickoff` and a `delivery_kickoff_id` is issued.
That id is the **audit link** between payment and delivery — keep it. The
response `next_action` tells you to run the Sprint with the customer's data,
passing `delivery_kickoff_id` as `engagement_id`. Delivery (`POST
/api/v1/sprint/run`) is documented in
`../sales-kit/CUSTOMER_1_GO_LIVE_RUNBOOK.md`.

**AR.** تنتقل الحالة إلى `delivery_kickoff` ويُصدَر `delivery_kickoff_id`.
هذا المعرّف هو **رابط التدقيق** بين الدفعة والتسليم — احتفظ به. حقل
`next_action` في الرد يخبرك بتشغيل الـSprint ببيانات العميل، ممرّراً
`delivery_kickoff_id` كـ`engagement_id`. التسليم موثّق في
`../sales-kit/CUSTOMER_1_GO_LIVE_RUNBOOK.md`.

---

## 4. Check state at any time — فحص الحالة في أي وقت

**EN.** `GET /api/v1/payment-ops/{payment_id}/state` returns the current
record and an `is_revenue` flag (true once status is `payment_confirmed` or
`delivery_kickoff`). Use it before each step to confirm where the payment
stands. Records are persisted to `data/payment_states.jsonl`.

**AR.** `GET /api/v1/payment-ops/{payment_id}/state` يعيد السجل الحالي وعلَم
`is_revenue` (صحيح متى صارت الحالة `payment_confirmed` أو `delivery_kickoff`).
استخدمه قبل كل خطوة. تُحفظ السجلّات في `data/payment_states.jsonl`.

---

## 5. Saudi invoicing — الفوترة السعودية

**EN.** Issue a VAT-compliant invoice for the transfer. Bank transfer is the
payment rail; ZATCA e-invoicing (`../../integrations/zatca.py`) is the
invoice record. The transfer must carry the business name, fall within a
reasonable window of the agreed date, and match or exceed the invoice
amount. Email the customer a ZATCA-compliant receipt after confirmation.

**AR.** أصدر فاتورة متوافقة مع ضريبة القيمة المضافة عن التحويل. التحويل
البنكي هو وسيلة الدفع؛ والفوترة الإلكترونية ZATCA
(`../../integrations/zatca.py`) هي سجل الفاتورة. يجب أن يحمل التحويل اسم
المنشأة، وأن يقع ضمن نافذة معقولة من التاريخ المتفق عليه، وأن يطابق مبلغ
الفاتورة أو يزيد. أرسل للعميل إيصالاً متوافقاً مع ZATCA بعد التأكيد.

---

## 6. Reconciliation — المطابقة

**EN.** Weekly, reconcile three sources against each other: the business
bank statement, the `data/payment_states.jsonl` ledger, and the issued
invoices. Every `payment_confirmed` record must have a matching bank line
and a matching invoice. Any `payment_evidence_uploaded` record older than
48 hours without confirmation, or any confirmed payment without a bank line,
is a friction item — record it in `../ledgers/` and resolve it.

**AR.** أسبوعياً، طابِق ثلاثة مصادر: كشف حساب المنشأة، وسجل
`data/payment_states.jsonl`، والفواتير الصادرة. كل سجل `payment_confirmed`
يجب أن يقابله بند بنكي وفاتورة. أي سجل `payment_evidence_uploaded` أقدم من
48 ساعة دون تأكيد، أو دفعة مؤكّدة بلا بند بنكي، بند احتكاك — سجّله في
`../ledgers/` وعالجه.

---

## 7. When to retire this path — متى يُتقاعَد هذا المسار

**EN.** Keep the bank-transfer path as a permanent alternative even after
Moyasar goes live — it is the fallback when a webhook is delayed or a
customer prefers a transfer. Once `MOYASAR_GO_LIVE.md` is complete, card
payments use `method: "moyasar_live"`; bank transfer stays available with
`method: "bank_transfer"`.

**AR.** أبقِ مسار التحويل البنكي بديلاً دائماً حتى بعد تفعيل ميسر — فهو
الاحتياط عند تأخّر webhook أو عند تفضيل العميل للتحويل. بعد اكتمال
`MOYASAR_GO_LIVE.md` تستخدم مدفوعات البطاقة `method: "moyasar_live"`؛ ويبقى
التحويل البنكي متاحاً بـ`method: "bank_transfer"`.

---

*Cross-references: [`MOYASAR_GO_LIVE.md`](MOYASAR_GO_LIVE.md),
[`../ops/COMMERCIAL_FREEZE.md`](../ops/COMMERCIAL_FREEZE.md),
[`../ops/LAAS_INVOICING_SOP.md`](../ops/LAAS_INVOICING_SOP.md),
[`../sales-kit/CUSTOMER_1_GO_LIVE_RUNBOOK.md`](../sales-kit/CUSTOMER_1_GO_LIVE_RUNBOOK.md),
[`../CANONICAL_PRODUCT_NARRATIVE.md`](../CANONICAL_PRODUCT_NARRATIVE.md).*

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.*
