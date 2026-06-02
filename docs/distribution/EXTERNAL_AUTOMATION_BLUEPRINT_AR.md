# External Automation Blueprint — مخطّط الأتمتة الخارجية (n8n) — External Automation Blueprint

> Purpose — الغرض: يحدّد هذا المستند سياسة استخدام n8n مع نظام تنفيذ الإيراد: التدفّقات الحتمية المسموحة مقابل الممنوعة. القاعدة الجوهرية: n8n مسموح للتدفّقات **الحتمية** (تذكير، مزامنة حالة، تجهيز)، وممنوع لأي تدفّق يجعل نموذجًا لغويًا يقرّر الإرسال أو يقوم بكَشط أو إرسال بارد.
>
> This document defines the n8n usage policy with the Revenue Execution OS: allowed deterministic flows versus forbidden ones. The core rule: n8n is allowed for deterministic flows (reminders, status sync, preparation), and forbidden for any flow where an LLM decides to send, or that scrapes or sends cold messages.

Cross-link — روابط: [CHANNEL_POLICY_AR.md](./CHANNEL_POLICY_AR.md) · [FOLLOWUP_ENGINE_AR.md](./FOLLOWUP_ENGINE_AR.md) · [PAYMENT_HANDOFF_AR.md](./PAYMENT_HANDOFF_AR.md) · [../references/REVENUE_EXECUTION_REFERENCE_LIBRARY.md](../references/REVENUE_EXECUTION_REFERENCE_LIBRARY.md) · [../05_governance_os/RUNTIME_GOVERNANCE.md](../05_governance_os/RUNTIME_GOVERNANCE.md).

---

## 1. المبدأ — The principle

n8n أداة أتمتة حتمية، تُستخدَم للتذكير والمزامنة والتجهيز — لا لاتخاذ قرار الإرسال. كل تدفّق مسموح يلتزم بثلاثة قيود:

n8n is a deterministic automation tool used for reminding, syncing, and preparing — not for deciding to send. Every allowed flow obeys three constraints:

- **حتمي** — لا قرار LLM يُحدِّد إجراءً خارجيًا.
- **لا إرسال خارجي للعملاء المحتملين** — الإرسال يبقى يدويًا بيد المؤسس (البند 8).
- **لا بيانات شخصية في السجلّات** — المعرّفات مجهولة (البند 6).

Deterministic; no external send to prospects; no PII in logs.

---

## 2. التدفّقات المسموحة (حتمية) — Allowed flows (deterministic)

| التدفّق — Flow | الوصف — Description | لماذا مسموح — Why allowed |
|---|---|---|
| استقبال العملاء المحتملين — Lead intake | استلام نموذج/إحالة وكتابته بمصدر مُعلَن | حتمي، لا إرسال، مصدر موثّق |
| تذكير الموافقة — Approval reminders | تذكير المؤسس بمسودات تنتظر قراره | تذكير داخلي، لا إرسال خارجي |
| تذكير المتابعة — Follow-up reminders | تذكير المؤسس بمتابعات مستحقّة | داخلي، القرار يبقى بشريًا |
| تجهيز حجز Calendly — Calendly booking prep | تجهيز رابط/فتحة للمؤسس ليؤكّدها | تجهيز، لا حجز نيابة عن أحد |
| مزامنة حالة HubSpot — HubSpot status sync | مزامنة حالة الصفقة (لا إرسال رسائل) | مزامنة حالة حتمية |
| حدث الدفع من Moyasar — Moyasar paid event | استقبال إشعار «مدفوع» لتحديث الحالة | حدث وارد، لا خصم ولا إرسال |
| الملخّص الأسبوعي — Weekly summary | تجميع مؤشرات الأسبوع للمؤسس | تقرير داخلي |

كل تدفّق أعلاه إمّا **وارد** (يستقبل بيانات) أو **داخلي** (يذكّر/يلخّص). لا تدفّق منها يرسل رسالة لعميل محتمل. Each flow above is either inbound or internal; none sends a message to a prospect.

---

## 3. التدفّقات الممنوعة — Forbidden flows

| التدفّق الممنوع — Forbidden flow | القاعدة المُنتهَكة — Violated rule |
|---|---|
| نموذج لغوي يقرّر الإرسال — LLM deciding to send | البند 8 (لا إجراء خارجي دون موافقة) |
| أتمتة واتساب بارد — Cold WhatsApp automation | البند 2 |
| أتمتة لينكدإن — LinkedIn automation | البند 3 |
| كَشط البيانات — Scraping | البند 1 |
| حذف بيانات — Deleting data | سلامة البيانات/التدقيق |
| تعديل الأسرار — Editing secrets | الأمن/أقل صلاحية |

> أي تدفّق يمنح n8n قدرة «إرسال للعميل» أو «قرار LLM بالإرسال» مرفوض في المراجعة، ولو بدا مفيدًا. الإرسال يبقى فعلًا بشريًا (راجع [CHANNEL_POLICY_AR.md](./CHANNEL_POLICY_AR.md)).

Any flow granting n8n a "send to customer" capability or an "LLM decides to send" path is rejected in review, however useful it seems.

---

## 4. حدود الصلاحية — Privilege boundaries

- **قراءة فقط حيث أمكن** — تفضَّل التدفّقات الواردة والقراءة على الكتابة.
- **لا مفاتيح إرسال** — لا تُمنَح n8n مفاتيح ترسل بريدًا/واتساب للعملاء المحتملين.
- **لا وصول للأسرار** — لا تعديل أو قراءة للأسرار الحسّاسة من تدفّق آلي.
- **سجلّ بلا بيانات شخصية** — كل سجل تدفّق خالٍ من PII (البند 6).

Read-only where possible; no send keys; no secret access; PII-free logs.

---

## 5. علاقة n8n بالطبقة — How n8n relates to the layer

n8n **حول** الطبقة، لا **داخل** قرارها. الطبقة تولّد المسودات وقرارات الحوكمة؛ n8n قد يذكّر المؤسس بمراجعتها أو يستقبل حدث «مدفوع» ليحدّث الحالة. لا يستبدل n8n الحلقة اليومية ولا موافقة المؤسس.

n8n sits around the layer, not inside its decisions. The layer generates drafts and governance decisions; n8n may remind the founder to review them or receive a "paid" event to update state. n8n replaces neither the daily loop nor founder approval.

---

## 6. مراجعة كل تدفّق جديد — Reviewing each new flow

قبل تفعيل أي تدفّق n8n جديد، أجب:

Before enabling any new n8n flow, answer:

1. هل هو حتمي (لا قرار LLM بالإرسال)؟
2. هل يرسل أي شيء لعميل محتمل؟ (يجب: لا)
3. هل يقرأ/يكتب بيانات شخصية؟ (يجب: لا)
4. هل يمسّ الأسرار أو يحذف بيانات؟ (يجب: لا)

أي «نعم» في 2–4 أو «لا» في 1 يعني رفض التدفّق. Any "yes" in 2–4 or "no" in 1 means the flow is rejected.

---

> القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value.
