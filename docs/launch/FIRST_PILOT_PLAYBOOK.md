# Dealix — دليل أول Pilot مدفوع · First Paid Pilot Playbook

**الحالة / Status:** DRAFT
**المالك / Owner:** Sami (founder)
**آخر تحديث / Last updated:** 2026-05-18
**وثائق مرافقة / Companion docs:** `MOYASAR_ACTIVATION_RUNBOOK.md` · `MACHINE_ORCHESTRATION_MAP.md` · `../ops/CUSTOMER_ONBOARDING_DAY_BY_DAY.md` · `../V14_FOUNDER_DAILY_OPS.md`

---

## الغرض · Purpose

هذه الوثيقة هي المسار الكامل لتسليم أول Pilot مدفوع بلا أخطاء. كل الكود المذكور مكتمل — الوثيقة تربط القطع في تسلسل واحد قابل للتنفيذ.

This is the end-to-end playbook to deliver the first paid pilot flawlessly. All code referenced is complete; this document binds the pieces into one executable sequence.

العرض المدفوع هو **499 SAR — `revenue_proof_sprint_499`** (نقطة الدخول الرسمية). راجع `docs/COMMERCIAL_WIRING_MAP.md` لسجل الأسعار الكامل.

---

## المسار من البداية للنهاية · The delivery path

| # | المرحلة · Stage | الأداة · Module | المخرج · Output |
|---|---|---|---|
| 1 | Intake · الاستقبال | `landing/diagnostic.html` → `api/routers/diagnostic.py` | تشخيص مجاني، 6 أسئلة |
| 2 | Qualification · التأهيل | `auto_client_acquisition/sales_os/` + `icp_scorer.py` | درجة ICP + قرار تأهيل |
| 3 | Offer · العرض | عرض 499 SAR | Proposal ثنائي اللغة |
| 4 | Invoice · الفاتورة | `payment_ops/orchestrator.py` `create_invoice_intent()` | نية فاتورة |
| 5 | Payment · الدفع | `confirm_payment()` | دفع مؤكَّد — بمبادرة المؤسس + إثبات |
| 6 | Kickoff · الانطلاق | `kickoff_delivery()` | engagement يربط الدفع بالتسليم |
| 7 | Sprint · السبرنت | `delivery_factory/delivery_sprint.py` `run_sprint()` | 8 خطوات خلال 7 أيام |
| 8 | Handoff · التسليم | Proof Pack | 14 قسمًا ثنائي اللغة، PDF |

### 1. Intake · الاستقبال

التشخيص المجاني (`free_mini_diagnostic`، 0 SAR): 6 أسئلة عبر `landing/diagnostic.html` تصل إلى `api/routers/diagnostic.py`. هذه نقطة الالتقاط الأولى — لا التزام، لا دفع.

### 2. Qualification · التأهيل

`auto_client_acquisition/sales_os/` يجري التأهيل، و`icp_scorer.py` يعطي درجة المطابقة مع الـICP. القرار: هل العميل مناسب لـSprint بـ499 SAR؟

### 3. Offer · العرض

عند التأهيل، يُقدَّم عرض `revenue_proof_sprint_499`. ابنِ proposal ثنائي اللغة (AR + EN) بنفس البنية والطول.

### 4. Invoice · الفاتورة

`create_invoice_intent()` ينشئ نية الفاتورة. القناة قد تكون `bank_transfer` أو `cash_in_person` اليوم، أو `moyasar_live` بعد تفعيل Moyasar — راجع [`MOYASAR_ACTIVATION_RUNBOOK.md`](MOYASAR_ACTIVATION_RUNBOOK.md).

### 5. Payment · الدفع

`confirm_payment()` **يتطلب إثباتًا أولًا** (evidence first) ولا يُستدعى إلا **بمبادرة المؤسس**. لا تأكيد تلقائي — هذا غير القابل للتفاوض `no_live_charge`.

### 6. Kickoff · الانطلاق

`kickoff_delivery()` ينشئ الـengagement الذي يربط الدفع المؤكَّد بالتسليم. لا تسليم بلا دفع مؤكَّد مسبقًا.

### 7. السبرنت — 7 أيام · The 7-day sprint

`run_sprint()` في `delivery_factory/delivery_sprint.py` ينفّذ **8 خطوات**:

1. kickoff
2. DQ score (جودة البيانات)
3. account scoring
4. draft generation
5. governance review
6. Proof Pack assembly (14 قسمًا)
7. capital assets
8. retainer-readiness check

### 8. Proof Pack handoff · التسليم

Proof Pack من 14 قسمًا، ثنائي اللغة، يُحوَّل إلى PDF ويُسلَّم للعميل للمراجعة. القيم تحمل وسوم `value_os`: estimated / observed / verified / client_confirmed — لا تُرفَع قيمة إلى verified بلا دليل.

---

## التشغيل التجريبي · Dry-run (قبل أول عميل حقيقي)

قبل أول عميل حقيقي، شغّل المسار كاملًا في وضع الاختبار لإثبات أن الـpipeline يعمل من طرف إلى طرف:

- استخدم **فاتورة اختبار بـ1 SAR — وضع اختبار فقط (test-mode only)**. ليست سعر عميل.
- نفّذ الخطوات 1→8 بالكامل.
- تحقق: هل ظهر التشخيص؟ هل سجّل الـICP درجة؟ هل تأكّد الدفع بإثبات؟ هل وُلِّد Proof Pack بـ14 قسمًا؟
- لا تنتقل إلى عميل حقيقي قبل أن يمرّ الـdry-run نظيفًا.

Before the first real customer, run the whole flow in test mode (a 1 SAR test invoice — test mode only) to prove the pipeline end to end.

---

## إيقاع المؤسس يومًا بيوم · Day-by-day founder rhythm

اتبع الإيقاع التفصيلي في [`../ops/CUSTOMER_ONBOARDING_DAY_BY_DAY.md`](../ops/CUSTOMER_ONBOARDING_DAY_BY_DAY.md) والروتين اليومي في [`../V14_FOUNDER_DAILY_OPS.md`](../V14_FOUNDER_DAILY_OPS.md).

| اليوم · Day | تركيز المؤسس · Founder focus |
|---|---|
| Day 0 | تأكيد الدفع + `kickoff_delivery()` |
| Day 1 | DQ score + account scoring — مراجعة جودة البيانات |
| Day 2–3 | draft generation — مراجعة المسودات قبل أي إرسال |
| Day 4 | governance review — تمرير البوابات |
| Day 5–6 | Proof Pack assembly — مراجعة الـ14 قسمًا |
| Day 7 | handoff + retainer-readiness — تسليم PDF للعميل |

---

## غير القابل للتفاوض · Non-negotiables honored

- **لا إرسال تلقائي** — `no_live_send`. كل خطوة خارجية تمرّ بموافقة المؤسس.
- **موافقة المؤسس عند كل حدّ خارجي** — راجع [`MACHINE_ORCHESTRATION_MAP.md`](MACHINE_ORCHESTRATION_MAP.md).
- **Proof Pack إلزامي** — لا تسليم بلا حزمة دليل من 14 قسمًا.
- **لا نتائج مضمونة** — القيم موسومة بـ`value_os`؛ لا وعد بأرقام مبيعات.

---

> النتائج التقديرية ليست نتائج مضمونة / Estimated outcomes are not guaranteed outcomes.
