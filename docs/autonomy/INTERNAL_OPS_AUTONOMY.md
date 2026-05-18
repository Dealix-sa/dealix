# Dealix — استقلالية العمليات الداخلية · Internal Ops Autonomy

**الحالة / Status:** DRAFT — architecture
**المالك / Owner:** Sami (founder)
**آخر تحديث / Last updated:** 2026-05-18
**وثائق مرافقة / Companion docs:** `SALES_AUTONOMY_SYSTEM.md` · `AGENT_GOVERNANCE_AND_GUARDRAILS.md` · `../launch/MACHINE_ORCHESTRATION_MAP.md`

---

## الغرض · Purpose

تصف هذه الوثيقة أقوى نظام عمليات داخلية (غير مبيعات) يمكن لـDealix تشغيله، وأي دور ووكلاء يديرونه ذاتيًا. تصمّم المعمارية فقط؛ لا تأذن ببناء كود جديد. التجميد التجاري نشط.

This document describes the strongest internal (non-sales) operations system Dealix can run and which role and agents run each domain autonomously. It designs architecture only and authorizes no new code. The Commercial Freeze is active.

«ذاتي» هنا يعني نفس المعنى: المكينة تنفّذ كل التحضير والتحليل والمراقبة؛ المؤسس يوافق على كل فعل خارجي (إرسال / تحصيل).

"Autonomous" here means the same: the machine does all preparation, analysis, and monitoring; the founder approves every external action (send / charge).

---

## التسليم · Delivery

يملك دور `RoleName.CUSTOMER_SUCCESS` التسليم. المحرّك هو `run_sprint()` ذو الثماني خطوات في `auto_client_acquisition/delivery_factory/delivery_sprint.py`. تُجهَّز مهام التسليم كأفعال `delivery_task`، ويُجهَّز طلب الدليل كفعل `proof_request`. تُبنى الـProof Pack عبر `proof_os`. كل عبارة قيمة في الـProof Pack موسومة بتير `value_os`.

The `RoleName.CUSTOMER_SUCCESS` role owns delivery. The engine is the 8-step `run_sprint()` in `delivery_sprint.py`. Delivery work queues as `delivery_task` actions; proof requests queue as `proof_request`. The Proof Pack is built via `proof_os`, with every value statement tagged by a `value_os` tier.

---

## المالية · Finance

يملك دور `RoleName.FINANCE` المالية، عبر `auto_client_acquisition/payment_ops/orchestrator.py`. تُجهَّز التذكيرات كأفعال `payment_reminder`. **تأكيد الدفع يبدأه المؤسس دائمًا** — لا تحصيل حيّ تلقائي (`no_live_charge`). تُجدوَل التجديدات عبر الإيقاع الشهري (`monthly_cadence.yml`).

The `RoleName.FINANCE` role owns finance via `payment_ops/orchestrator.py`. Reminders queue as `payment_reminder` actions. Payment confirmation is always founder-initiated — no automatic live charge. Renewals are scheduled via the monthly cadence.

---

## الدعم · Support

تُجهَّز ردود الدعم كأفعال `support_reply_draft`. يفرز الوكيل التذاكر ويصوغ ردًا مقترحًا؛ المؤسس يوافق قبل أي رد خارجي.

Support replies queue as `support_reply_draft` actions. The agent triages tickets and drafts a proposed reply; the founder approves before any external reply.

---

## البيانات · Data

يبقي `data_os` كل مدخل نظيفًا وبموافقة: `compute_dq` يقيس جودة البيانات، و`SourcePassport` يثبت المصدر والموافقة على كل سجل. لا بيانات بلا جواز مصدر (`no_unconsented_data`).

`data_os` keeps every input clean and consented: `compute_dq` measures data quality, and `SourcePassport` stamps source and consent on every record. No data without a source passport.

---

## الحوكمة · Governance

يملك دور `RoleName.COMPLIANCE` الحوكمة. `governance_os` دائم التشغيل (always-on)، يتحقق من كل فعل عبر `approval_for_action` ويُصدر `GovernanceDecision`. هذا هو الوكيل الدائم — لا فعل يمر دون مروره عليه.

The `RoleName.COMPLIANCE` role owns governance. `governance_os` is always-on, validating every action via `approval_for_action` and issuing a `GovernanceDecision`. This is the always-on agent — no action passes without it.

---

## القيمة ورأس المال والتبنّي · Value, Capital, Adoption

- `value_os` يسجّل القيمة المتدرّجة عبر `add_event` بالتيرات: `estimated` · `observed` · `verified` · `client_confirmed`.
- `capital_os` يسجّل الأصول القابلة لإعادة الاستخدام عبر `add_asset`.
- `adoption_os` يحسب جاهزية الـretainer عبر `adoption_score`؛ ويكمّله `client_os.client_health_score`.

`value_os` logs tiered value via `add_event`. `capital_os` registers reusable assets via `add_asset`. `adoption_os` scores retainer-readiness via `adoption_score`, complemented by `client_os.client_health_score`.

---

## جدول النطاقات الداخلية · Internal domains table

| النطاق · Domain | دور الوكيل · Role agent | الـmodule الداعم · Backing module | المخرجات الذاتية · Autonomous outputs | ما يبقى بيد المؤسس · Founder-gated |
|---|---|---|---|---|
| التسليم · Delivery | `RoleName.CUSTOMER_SUCCESS` | `delivery_sprint.py` `run_sprint()`, `proof_os` | مسودات مهام التسليم، Proof Pack مُجهّز · delivery-task drafts, prepared Proof Pack | إرسال الـProof Pack للعميل · sending the Proof Pack (`delivery_task`, `proof_request`) |
| المالية · Finance | `RoleName.FINANCE` | `payment_ops/orchestrator.py` | مسودات تذكير، جدول تجديدات · reminder drafts, renewal schedule | إرسال التذكير وتأكيد الدفع · sending reminders, confirming payment (`payment_reminder`) |
| الدعم · Support | `RoleName.CUSTOMER_SUCCESS` | `approval_center` | فرز التذاكر، مسودة رد · ticket triage, reply draft | إرسال الرد · sending the reply (`support_reply_draft`) |
| البيانات · Data | `RoleName.COMPLIANCE` | `data_os` (`compute_dq`, `SourcePassport`) | درجة جودة، جواز مصدر · DQ score, source passport | قبول مصدر بلا موافقة موثّقة · accepting an unconsented source |
| الحوكمة · Governance | `RoleName.COMPLIANCE` | `governance_os` (`approval_for_action`) | `GovernanceDecision` على كل فعل · governance decision per action | تجاوز قرار حوكمة · overriding a governance decision |
| القيمة · Value | `RoleName.CEO` | `value_os` (`add_event`) | سجل قيمة متدرّج · tiered value log | ترقية تير إلى `verified`/`client_confirmed` · tier upgrade |
| رأس المال · Capital | `RoleName.CEO` | `capital_os` (`add_asset`) | سجل أصول قابلة لإعادة الاستخدام · reusable asset registry | — |
| التبنّي · Adoption | `RoleName.CUSTOMER_SUCCESS` | `adoption_os`, `client_os` | درجة جاهزية retainer، صحة عميل · retainer-readiness, client health | عرض الـretainer على العميل · pitching the retainer |

---

## المبدأ الحاكم · Governing principle

العمليات الداخلية تُحضَّر وتُراقَب ذاتيًا بالكامل؛ كل فعل يلمس عميلًا أو نقودًا يبقى بوابة موافقة. هذا يحمي `no_live_send`, `no_live_charge`, `no_silent_failures`, `no_unaudited_changes`.

Internal operations are fully self-prepared and self-monitored; every action that touches a customer or money stays an approval gate. This protects `no_live_send`, `no_live_charge`, `no_silent_failures`, and `no_unaudited_changes`.

---

> النتائج التقديرية ليست نتائج مضمونة / Estimated outcomes are not guaranteed outcomes.
