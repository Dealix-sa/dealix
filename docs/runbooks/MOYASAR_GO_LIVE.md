# Moyasar Go-Live Runbook — دليل تفعيل الدفع عبر ميسر

<!-- Owner: Founder (Sami) | Last reviewed: 2026-05-18 | Workstream G -->

> **Audience.** The founder. This runbook is written so a non-engineer can
> execute it end to end. It removes every obstacle to taking card payments
> through Moyasar **except one**: Sami's KYC signature and the live secret
> key, which only he can produce.
>
> **الجمهور.** المؤسس. هذا الدليل مكتوب ليُنفِّذه شخص غير تقني من البداية
> للنهاية. يزيل كل عائق أمام قبول الدفع بالبطاقة عبر ميسر **ما عدا واحداً**:
> توقيع KYC من سامي والمفتاح السرّي المباشر، وهما ما لا ينتجه سواه.

> **Freeze note.** Dealix is under an active Commercial Freeze
> (`../ops/COMMERCIAL_FREEZE.md`). This is a documentation-only runbook for
> the rung 0–1 delivery finish. It changes **no code** and enables **no live
> charges**. The live flip is a founder action, executed by Sami, not by
> any automated agent.

---

## 1. Why this matters — لماذا هذا مهم

**EN.** Moyasar payment-account activation is the company's one hard revenue
blocker. The platform code is shipped and verified. The `NO_LIVE_CHARGE`
hard gate in `auto_client_acquisition/payment_ops/orchestrator.py` refuses
every `moyasar_live` charge until the environment is explicitly flipped. The
interim bank-transfer path (`INTERIM_BANK_TRANSFER_CASH_PATH.md`) lets the
founder take money **today** without Moyasar; this runbook is the path to the
**automated** card flow once KYC clears.

**AR.** تفعيل حساب الدفع لدى ميسر هو القيد الوحيد الصعب على إيراد الشركة.
كود المنصة جاهز ومُتحقَّق منه. بوابة `NO_LIVE_CHARGE` في
`auto_client_acquisition/payment_ops/orchestrator.py` ترفض كل عملية شحن
`moyasar_live` حتى تُقلَب البيئة صراحةً. مسار التحويل البنكي المؤقت
(`INTERIM_BANK_TRANSFER_CASH_PATH.md`) يتيح للمؤسس تحصيل المال **اليوم** دون
ميسر؛ وهذا الدليل هو الطريق إلى المسار **الآلي** بالبطاقة بعد اعتماد KYC.

---

## 2. KYC document checklist — قائمة وثائق KYC

**EN.** A Saudi Moyasar merchant account requires the founder to upload the
following. Prepare clear PDF or photo scans before starting:

- Commercial Registration (السجل التجاري) — current, not expired.
- National ID of the authorized signatory (Sami).
- VAT registration certificate (شهادة التسجيل في ضريبة القيمة المضافة), if
  the business is VAT-registered.
- A bank account IBAN certificate in the **business** name — Moyasar settles
  to this account. This must be the same legal entity as the CR.
- National Address (العنوان الوطني) of the business.
- A short description of what Dealix sells: an approval-first
  revenue-operations radar for Saudi B2B (subscription + one-off services).
  Do not describe scraping, outreach automation, or guaranteed outcomes.

**AR.** يتطلب حساب التاجر السعودي لدى ميسر رفع الوثائق التالية. جهّز نسخاً
واضحة (PDF أو صور) قبل البدء:

- السجل التجاري — ساري، غير منتهٍ.
- الهوية الوطنية للمفوّض بالتوقيع (سامي).
- شهادة التسجيل في ضريبة القيمة المضافة، إن كان النشاط مسجّلاً.
- شهادة IBAN لحساب بنكي باسم **المنشأة** — يحوّل ميسر التسوية إليه. يجب أن
  يكون نفس الكيان القانوني الوارد في السجل التجاري.
- العنوان الوطني للمنشأة.
- وصف موجز لما تبيعه Dealix: رادار عمليات إيراد يعمل بموافقة المؤسس لقطاع
  B2B السعودي (اشتراك + خدمات لمرة واحدة). لا تذكر استخراج البيانات أو أتمتة
  التواصل أو نتائج مضمونة.

---

## 3. Account setup steps — خطوات إنشاء الحساب

**EN.**

1. Register the merchant account on the Moyasar dashboard with the business
   email and CR details.
2. Upload every document from Section 2. Submit for review.
3. Wait for Moyasar to approve the account. This is the manual KYC step that
   only Sami can complete; allow a few business days.
4. Once approved, open **API Keys** in the dashboard. You will see two key
   pairs: test keys (`sk_test_…` / `pk_test_…`) and live keys
   (`sk_live_…` / `pk_live_…`). The live keys appear only after approval.
5. Open **Webhooks** in the dashboard and note where you will register the
   webhook URL (Section 5).

**AR.**

1. سجّل حساب التاجر في لوحة ميسر ببريد المنشأة وبيانات السجل التجاري.
2. ارفع كل وثيقة من القسم 2 ثم قدّم الطلب للمراجعة.
3. انتظر اعتماد ميسر للحساب. هذه هي خطوة KYC اليدوية التي لا ينجزها سوى سامي؛
   اترك بضعة أيام عمل.
4. بعد الاعتماد، افتح **API Keys** في اللوحة. سترى زوجين من المفاتيح: مفاتيح
   اختبار (`sk_test_…` / `pk_test_…`) ومفاتيح مباشرة (`sk_live_…` /
   `pk_live_…`). تظهر المفاتيح المباشرة بعد الاعتماد فقط.
5. افتح **Webhooks** في اللوحة، ولاحظ مكان تسجيل رابط الـwebhook (القسم 5).

---

## 4. Where the keys live + the env flip — أين تُوضَع المفاتيح وكيف تُقلَب البيئة

**EN.** All keys and the mode flag are environment variables set in
**Railway** — never in a committed `.env`, never in the browser bundle.
Railway path: **Project → Environment → Service `web` → Variables**. After
adding variables, click **Review → Deploy** and wait for a green build
(see `../ops/ENV_UNLOCK_MATRIX.md`).

The exact variables — the live values are the ones to set at cutover:

| Variable | Live value | Read by |
|---|---|---|
| `MOYASAR_SECRET_KEY` | `sk_live_…` | `dealix/payments/moyasar.py` (HTTP Basic auth) |
| `MOYASAR_WEBHOOK_SECRET` | live webhook secret from dashboard | `payment_ops/reconciliation.py`, `dealix/payments/moyasar.py` |
| **`DEALIX_MOYASAR_MODE`** | **`live`** | `payment_ops/orchestrator.py` — the hard gate |

**The single flag that unlocks live charges is `DEALIX_MOYASAR_MODE`, and
its live value is `live`.** It is read in
`auto_client_acquisition/payment_ops/orchestrator.py` by the function
`_enforce_no_live_charge`: when a payment uses method `moyasar_live`, the
orchestrator raises `ValueError` ("moyasar_live requires
DEALIX_MOYASAR_MODE=live env var — NO_LIVE_CHARGE gate") unless
`DEALIX_MOYASAR_MODE` equals `live` exactly. Any other value — including
`test`, `sandbox`, or unset — keeps live charges blocked. The default is
treated as `sandbox`/`test`.

The helper `scripts/moyasar_live_cutover.py` is an interactive script the
founder may run: it validates the `sk_live_` key shape and **prints** the
exact Railway block to paste. It never writes the key to disk and never
charges a live card.

**AR.** كل المفاتيح وعلَم الوضع متغيّرات بيئة تُضبط في **Railway** — لا في
`.env` مرفوع للمستودع، ولا في حزمة المتصفح. مسار Railway:
**Project → Environment → Service `web` → Variables**. بعد إضافة المتغيّرات
اضغط **Review → Deploy** وانتظر بناءً أخضر (راجع
`../ops/ENV_UNLOCK_MATRIX.md`).

**العلَم الوحيد الذي يفتح الشحن المباشر هو `DEALIX_MOYASAR_MODE`، وقيمته
المباشرة `live`.** يُقرأ في
`auto_client_acquisition/payment_ops/orchestrator.py` عبر الدالة
`_enforce_no_live_charge`: عند استخدام طريقة `moyasar_live`، يرفع المُنسِّق
استثناء `ValueError` ما لم يكن `DEALIX_MOYASAR_MODE` مساوياً تماماً لـ
`live`. أي قيمة أخرى — `test` أو `sandbox` أو غير مضبوط — تُبقي الشحن
المباشر محجوباً. الافتراضي يُعامَل كـ`sandbox`/`test`.

السكربت المساعد `scripts/moyasar_live_cutover.py` تفاعلي ويجوز للمؤسس
تشغيله: يتحقّق من شكل مفتاح `sk_live_` و**يطبع** كتلة Railway الدقيقة
للّصق. لا يكتب المفتاح على القرص ولا يشحن بطاقة حقيقية.

---

## 5. Register the webhook — تسجيل الـwebhook

**EN.** In the Moyasar live dashboard under **Webhooks**, register the URL:

```
https://<production-host>/api/v1/payment-ops/webhook
```

Copy the signing secret Moyasar shows and set it as `MOYASAR_WEBHOOK_SECRET`
in Railway. The webhook is verified in
`auto_client_acquisition/payment_ops/reconciliation.py`
(`verify_webhook_signature`, HMAC-SHA256). If the secret is unset the
reconciler treats requests as test-mode — so the secret **must** be set
before the cutover is signed off.

**AR.** في لوحة ميسر المباشرة تحت **Webhooks**، سجّل الرابط:

```
https://<production-host>/api/v1/payment-ops/webhook
```

انسخ سرّ التوقيع الذي يعرضه ميسر واضبطه كـ`MOYASAR_WEBHOOK_SECRET` في
Railway. يُتحقَّق من الـwebhook في
`auto_client_acquisition/payment_ops/reconciliation.py`. إن لم يُضبط السرّ
تُعامَل الطلبات كوضع اختبار — لذا **يجب** ضبط السرّ قبل اعتماد الانتقال.

---

## 6. Safe test-charge procedure — إجراء دفعة الاختبار الآمنة

**EN.** Do not test live with a customer. Use a real card the founder owns,
and a tiny amount.

1. Confirm the mode flipped: `GET /api/v1/founder/launch-status` should show
   `moyasar.mode = live` and `webhook_secret_configured = true`.
2. Create a **1 SAR** invoice intent through the payment-ops state machine:
   `POST /api/v1/payment-ops/invoice-intent` with
   `{"customer_handle": "founder_smoke", "amount_sar": 1, "method": "moyasar_live"}`.
   If `DEALIX_MOYASAR_MODE` is not `live`, this returns `403` — that proves
   the gate; fix the env and retry.
3. Pay the 1 SAR with the founder's own card. Confirm the payment shows
   `paid` on the Moyasar dashboard.
4. Within ~30 seconds the webhook arrives at
   `/api/v1/payment-ops/webhook`. Check that `reconciliation.py` confirmed
   the payment and the state advanced to `payment_confirmed`.
5. Replay the same webhook from the Moyasar dashboard "redeliver" button.
   The reconciler is idempotent (`has_been_reconciled` / `mark_reconciled`)
   — no duplicate confirmation, no duplicate proof event.
6. Refund the 1 SAR from the Moyasar dashboard. Confirm the refund posts.

**AR.** لا تختبر مباشرةً مع عميل. استخدم بطاقة حقيقية يملكها المؤسس بمبلغ زهيد.

1. تأكّد من قلب الوضع: `GET /api/v1/founder/launch-status` يجب أن يُظهر
   `moyasar.mode = live` و`webhook_secret_configured = true`.
2. أنشئ نية فاتورة بمبلغ **1 ريال** عبر آلة الحالة:
   `POST /api/v1/payment-ops/invoice-intent` بـ
   `{"customer_handle": "founder_smoke", "amount_sar": 1, "method": "moyasar_live"}`.
   إن لم يكن `DEALIX_MOYASAR_MODE` يساوي `live` يعود `403` — هذا يثبت
   البوابة؛ صحّح البيئة وأعد المحاولة.
3. ادفع الريال ببطاقة المؤسس. تأكّد من ظهور الحالة `paid` في لوحة ميسر.
4. خلال ~30 ثانية يصل الـwebhook إلى `/api/v1/payment-ops/webhook`. تحقّق من
   أن `reconciliation.py` أكّد الدفعة وأن الحالة تقدّمت إلى
   `payment_confirmed`.
5. أعد إرسال نفس الـwebhook من زر "redeliver" في لوحة ميسر. المُطابِق
   idempotent — لا تأكيد مكرّر ولا حدث إثبات مكرّر.
6. استرجع الريال من لوحة ميسر. تأكّد من قيد الاسترجاع.

---

## 7. Reconciliation drill — تمرين المطابقة

**EN.** Run this at the end of the test-charge session and then weekly:

- The Moyasar dashboard daily total, the `data/payment_states.jsonl` ledger,
  and the bank settlement projection must agree on the same amount.
- For each `payment_confirmed` record, an `evidence_reference` must exist
  (the orchestrator refuses `confirm` without it). For Moyasar payments the
  reference is `moyasar:<payment_id>:<webhook_id>`.
- Any payment stuck before `payment_confirmed` after 48 hours is a friction
  item — record it and follow up. Append findings to
  `../ledgers/` per the freeze ("Recording to the ledgers").

**AR.** نفّذ هذا في ختام جلسة دفعة الاختبار ثم أسبوعياً:

- يجب أن يتطابق إجمالي لوحة ميسر اليومي مع سجل
  `data/payment_states.jsonl` ومع توقّع التسوية البنكية على نفس المبلغ.
- لكل سجل `payment_confirmed` يجب وجود `evidence_reference` (المُنسِّق يرفض
  `confirm` بدونه). لمدفوعات ميسر يكون المرجع
  `moyasar:<payment_id>:<webhook_id>`.
- أي دفعة متوقّفة قبل `payment_confirmed` بعد 48 ساعة بند احتكاك — سجّله
  وتابعه. أضِف النتائج إلى `../ledgers/` وفق التجميد.

---

## 8. Rollback — التراجع

**EN.** If anything fails, set `DEALIX_MOYASAR_MODE` back to `test`, restore
the `sk_test_…` key, redeploy, and confirm
`GET /api/v1/founder/launch-status` reports `mode` is not `live`. Fall back
to the interim bank-transfer path. A rollback is not a failure; an unrecorded
rollback is.

**AR.** عند أي فشل، أعِد `DEALIX_MOYASAR_MODE` إلى `test`، واسترجع مفتاح
`sk_test_…`، وأعد النشر، وتأكّد أن `GET /api/v1/founder/launch-status` لا
يُظهر `live`. ارجع لمسار التحويل البنكي المؤقت. التراجع ليس فشلاً؛ التراجع
غير المُسجَّل هو الفشل.

---

*Cross-references: [`INTERIM_BANK_TRANSFER_CASH_PATH.md`](INTERIM_BANK_TRANSFER_CASH_PATH.md),
[`../ops/COMMERCIAL_FREEZE.md`](../ops/COMMERCIAL_FREEZE.md),
[`../ops/ENV_UNLOCK_MATRIX.md`](../ops/ENV_UNLOCK_MATRIX.md),
[`../MOYASAR_LIVE_CUTOVER.md`](../MOYASAR_LIVE_CUTOVER.md),
[`../sales-kit/CUSTOMER_1_GO_LIVE_RUNBOOK.md`](../sales-kit/CUSTOMER_1_GO_LIVE_RUNBOOK.md),
[`../CANONICAL_PRODUCT_NARRATIVE.md`](../CANONICAL_PRODUCT_NARRATIVE.md).*

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.*
