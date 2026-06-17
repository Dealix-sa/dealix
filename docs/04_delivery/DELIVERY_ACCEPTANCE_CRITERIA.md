# Delivery Acceptance Criteria — Dealix Sprint Acceptance — معايير قبول التسليم

These are the quality bars a Command Sprint must pass before it is marked "done." Status: INTERNAL — for founder and team use only. A sprint that fails any bar is incomplete, regardless of how much work was done. This file governs acceptance for the runbook [`COMMAND_SPRINT_DELIVERY_OS.md`](./COMMAND_SPRINT_DELIVERY_OS.md) and the offer [`../01_go_to_market/COMMAND_SPRINT_OFFER.md`](../01_go_to_market/COMMAND_SPRINT_OFFER.md). Module readiness is fixed by [`../00_platform_truth/MODULE_STATUS_MAP.md`](../00_platform_truth/MODULE_STATUS_MAP.md), where Delivery OS is INTERNAL.

هذه هي معايير الجودة التي يجب أن يجتازها سبرنت القيادة قبل وسمه بأنه "مكتمل". الحالة: INTERNAL — لاستخدام المؤسس والفريق فقط. والسبرنت الذي يسقط في أي معيار يكون ناقصاً مهما بُذل فيه من عمل. ويحكم هذا الملف القبول للدليل [`COMMAND_SPRINT_DELIVERY_OS.md`](./COMMAND_SPRINT_DELIVERY_OS.md) والعرض [`../01_go_to_market/COMMAND_SPRINT_OFFER.md`](../01_go_to_market/COMMAND_SPRINT_OFFER.md). وجاهزية الأنظمة محدّدة في [`../00_platform_truth/MODULE_STATUS_MAP.md`](../00_platform_truth/MODULE_STATUS_MAP.md) حيث نظام التسليم INTERNAL.

---

## The five acceptance bars — معايير القبول الخمسة

A sprint is "done" only when **all five** bars are met. Each maps to a binding non-negotiable.

السبرنت "مكتمل" فقط حين تتحقّق **المعايير الخمسة كلها.** وكلٌّ يقابل مبدأً مُلزِماً.

### 1. All folder files present — حضور كل ملفات المجلّد

Every file `00`–`10` exists in `customers/{company}/` and each meets its own "complete" bar from [`CUSTOMER_FOLDER_TEMPLATE.md`](./CUSTOMER_FOLDER_TEMPLATE.md). A missing or empty file fails acceptance.

كل ملف `00`–`10` موجود في `customers/{company}/` وكلٌّ يحقّق معيار "مكتمل" الخاص به من [`CUSTOMER_FOLDER_TEMPLATE.md`](./CUSTOMER_FOLDER_TEMPLATE.md). والملف الناقص أو الفارغ يسقط القبول.

### 2. Every claim sourced — كل ادعاء موثّق المصدر

No claim across any deliverable is un-sourced (#4). Every estimate is labeled an estimate; no deliverable states a guaranteed sales outcome. Opportunities are described as evidenced patterns, never as promised numbers.

لا ادعاء بلا مصدر في أي تسليم (#4). وكل تقدير موسوم كتقدير؛ ولا تسليم يذكر نتيجة مبيعات مضمونة. وتُوصَف الفرص كأنماط مُثبتة بالأدلة لا كأرقام موعودة.

### 3. Proof Pack score threshold met — تجاوز عتبة درجة حزمة الإثبات

The Proof Pack (`09_proof_pack.md`) follows [`PROOF_PACK_TEMPLATE.md`](./PROOF_PACK_TEMPLATE.md) and scores at the threshold below. Each of the seven questions is scored 0–2; the publish-permission field and Capital Asset reference are present.

تتبع حزمة الإثبات (`09_proof_pack.md`) قالب [`PROOF_PACK_TEMPLATE.md`](./PROOF_PACK_TEMPLATE.md) وتبلغ العتبة أدناه. يُسجَّل كل سؤال من السبعة بدرجة 0–2؛ ويحضر حقل إذن النشر ومرجع الأصل الرأسمالي.

| Score per question — درجة كل سؤال | Meaning — المعنى |
|---|---|
| 0 | Missing or unsourced — مفقود أو بلا مصدر |
| 1 | Present but thin — حاضر لكنه ضعيف |
| 2 | Present, sourced, decision-ready — حاضر وموثّق وجاهز للقرار |

**Pass threshold: at least 11 of 14, with no question scored 0, and the publish-permission field set (default: not permitted until written approval).**

**عتبة النجاح: 11 من 14 على الأقل، دون أن يُسجَّل أي سؤال 0، وضبط حقل إذن النشر (الافتراض: غير مسموح حتى اعتماد مكتوب).**

### 4. Governance / approval log complete — اكتمال سجل الحوكمة والاعتماد

`08_delivery_log.md` records all three governance gates from the runbook — payment gate, scope gate, and any external-action approval — each with an anonymized label and timestamp (#8). The log contains no PII: no email, phone, national ID, or real personal name (#6).

يسجّل `08_delivery_log.md` بوابات الحوكمة الثلاث من الدليل — بوابة الدفع، وبوابة النطاق، وأي اعتماد لإجراء خارجي — كلٌّ بتسمية مجهولة الهوية وطابع زمني (#8). ولا يحتوي السجل بيانات شخصية: بلا بريد أو هاتف أو هوية وطنية أو اسم حقيقي (#6).

### 5. At least one Capital Asset registered — تسجيل أصل رأسمالي واحد على الأقل

The Capital Asset reference in the Proof Pack names at least one reusable asset for the firm — a method, a template, or a scored dataset pattern (#11). A sprint with no registered asset fails acceptance.

يُسمّي مرجع الأصل الرأسمالي في حزمة الإثبات أصلاً واحداً قابلاً لإعادة الاستخدام للشركة على الأقل — طريقة أو قالباً أو نمط بيانات مُسجَّلاً (#11). والسبرنت بلا أصل مسجَّل يسقط القبول.

---

## Acceptance checklist — قائمة فحص القبول

| Bar — المعيار | Source rule — القاعدة | Pass? — اجتاز؟ |
|---|---|---|
| All files `00`–`10` present and complete | Folder template | `[ ]` |
| Every claim sourced; estimates labeled | #4 | `[ ]` |
| Proof Pack score ≥ 11/14, no 0s | #10 | `[ ]` |
| Three governance gates logged, no PII | #8, #6 | `[ ]` |
| At least one Capital Asset registered | #11 | `[ ]` |

Only when all five rows are checked may the Upsell Recommendation be written and the sprint handed off, per the runbook's handoff section.

فقط حين تُعلَّم الصفوف الخمسة جميعاً يجوز كتابة توصية الترقية وتسليم السبرنت، وفق قسم التسليم في الدليل.

---

## On failure — عند السقوط

If any bar fails, the sprint stays open and the gap is logged honestly in `08_delivery_log.md`. Acceptance is a discipline, not a formality; a slipped day is logged, not hidden. No handoff and no Upsell Recommendation occur on an unaccepted sprint.

إن سقط أي معيار، يبقى السبرنت مفتوحاً وتُسجَّل الفجوة بصدق في `08_delivery_log.md`. والقبول انضباط لا إجراء شكلي؛ واليوم المتأخّر يُسجَّل ولا يُخفى. ولا تسليم ولا توصية ترقية على سبرنت غير مقبول.

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
