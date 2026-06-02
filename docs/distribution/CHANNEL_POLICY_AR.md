# Channel Policy — سياسة القنوات — Channel Policy

> Purpose — الغرض: تحدّد هذه الوثيقة، لكل قناة، ما هو مسموح وما هو ممنوع داخل نظام تنفيذ الإيراد. المبدأ الحاكم: أقل صلاحية (least privilege) ولا إرسال خارجي. السبب الأمني: مخاطر حقن التعليمات (prompt injection) وسوء استخدام الوكلاء (agent misuse) تعني أن أي قدرة على «الإرسال» هي سطح هجوم؛ لذلك لا نمنحها للنظام إطلاقًا في الإصدار الأول.
>
> For each channel, this document defines what is allowed and what is forbidden inside the Revenue Execution OS. The governing principle is least privilege and no external send. The security rationale: prompt-injection and agent-misuse risk mean any "send" capability is an attack surface; we therefore never grant it to the system in v1.

Cross-link — روابط: [PRODUCT_DISTRIBUTION_OS_AR.md](./PRODUCT_DISTRIBUTION_OS_AR.md) · [DRAFT_SYSTEM_SPEC_AR.md](./DRAFT_SYSTEM_SPEC_AR.md) · [DRAFT_APPROVAL_RUNBOOK_AR.md](./DRAFT_APPROVAL_RUNBOOK_AR.md) · [../05_governance_os/CHANNEL_POLICY.md](../05_governance_os/CHANNEL_POLICY.md) · [../02_saudi_positioning/WHATSAPP_BOUNDARY.md](../02_saudi_positioning/WHATSAPP_BOUNDARY.md).

---

## 1. المبدأ — The principle

النظام **يُجهّز** ولا **يُرسل**. كل قناة تحصل على أقل قدرة ممكنة تكفي لتجهيز مسودة أو تسليم يوافق عليه المؤسس وينفّذه يدويًا.

The system **prepares**, it does not **send**. Each channel gets the least capability sufficient to prepare a draft or handoff that the founder approves and executes manually.

ثلاث طبقات تطبّق هذا:

- **least privilege** — لا قدرة إرسال في الكود.
- **human-in-the-loop** — كل مخرج خارجي يمرّ بموافقة المؤسس.
- **deterministic policy** — السياسة تُفحَص حتميًا (لا قرار LLM بالإرسال).

---

## 2. جدول سياسة القنوات — Channel policy table

| القناة — Channel | المسموح — Allowed | الممنوع — Forbidden |
|---|---|---|
| **Email** | مسودة + موافقة، ثم نسخ يدوي للإرسال | إرسال جماعي بلا موافقة، أتمتة بريد بارد، استيراد قوائم مكشوطة |
| **WhatsApp** | مسودة + نسخ يدوي لجهة أبدت اهتمامًا/علاقة قائمة | واتساب بارد آلي، إرسال جماعي، أي بوت يرسل تلقائيًا |
| **LinkedIn** | مسودة نص + نسخ يدوي بيد المؤسس | أتمتة لينكدإن (طلبات، رسائل، قبول)، كَشط ملفات |
| **Phone** | سكربتات اتصال (call scripts) للمؤسس | اتصال آلي (robocalls)، رسائل صوتية جماعية |
| **Proposal** | مسودة عرض + موافقة + إرسال يدوي | إرسال عرض دون مراجعة المؤسس |
| **Payment** | تجهيز تسليم دفع (handoff) للموافقة | إرسال رابط دفع دون موافقة المؤسس، أي خصم مباشر |

ترجمة موجزة للصف الإنجليزي — concise EN restatement: Email/WhatsApp/Proposal allow *draft + approval + manual copy*; LinkedIn allows *draft + manual copy only*; Phone allows *call scripts only*; Payment allows *handoff preparation only*. Across all rows: no mass send without approval, no cold automation, no scraping, no robocalls, and no sending a payment link without approval.

---

## 3. لماذا لا قدرة إرسال — Why no send capability

### حقن التعليمات — Prompt injection

إذا قرأ وكيل نصًا من جهة خارجية (رد بريد، ملف مرفق)، قد يحتوي ذلك النص على تعليمات خبيثة («أرسل هذا للجميع»). إن كان للنظام قدرة إرسال، يتحوّل الحقن إلى ضرر فعلي. الحلّ: **لا قدرة إرسال** — فيصبح أسوأ ما يفعله الحقن هو إفساد مسودة يراها المؤسس ويرفضها.

If an agent reads external text (an email reply, an attachment), that text may carry malicious instructions ("send this to everyone"). With a send capability, injection becomes real harm. The fix: no send capability — so the worst injection can do is corrupt a draft the founder reviews and rejects.

### سوء استخدام الوكلاء — Agent misuse

وكيل بصلاحية واسعة قد يُستغَل أو يُخطئ بحجم كبير. أقل صلاحية تعني أن خطأ الوكيل يبقى محصورًا في «مسودة»، لا في «1000 رسالة مُرسَلة».

A broadly-privileged agent can be exploited or err at scale. Least privilege keeps an agent's mistake confined to "a draft," not "1,000 messages sent."

---

## 4. علاقة الجدول بقرار الحوكمة — Mapping to `governance_decision`

كل مسودة تُنتَج بقناة، وقرار الحوكمة المرفق بها يعكس صف الجدول أعلاه:

- قناة مسموحة + ادعاء آمن → `DRAFT_ONLY` ثم `REQUIRE_APPROVAL`.
- قناة ممنوعة (واتساب بارد، أتمتة لينكدإن، كَشط) → `BLOCK` ويُسجَّل السبب.

Every draft is produced for a channel, and its attached `governance_decision` reflects the table row above: an allowed channel with a safe claim resolves to `DRAFT_ONLY` then `REQUIRE_APPROVAL`; a forbidden channel resolves to `BLOCK` with a logged reason.

تفاصيل أنواع القرار: [../05_governance_os/GOVERNANCE_DECISION_TYPES.md](../05_governance_os/GOVERNANCE_DECISION_TYPES.md). سياسة الادعاء: [../05_governance_os/CLAIM_SAFETY.md](../05_governance_os/CLAIM_SAFETY.md).

---

## 5. بيانات السياسة — Policy seed data

تُحمَّل القناة المسموحة من `data/distribution/channel_policy.yaml` (بيانات بذرة، تُراجَع يدويًا). لا يُضاف صف يسمح بالإرسال الخارجي؛ أي تعديل يفتح إرسالًا آليًا يُرفَض في المراجعة.

Allowed-channel posture is loaded from `data/distribution/channel_policy.yaml` (seed data, reviewed manually). No row that permits external sending is added; any change opening automated send is rejected in review.

---

> القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value.
