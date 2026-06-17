# Human Approval Policy — Founder Approval Before External Action — سياسة الموافقة البشرية

> Governance OS status: **BETA**. This policy is enforced today in controlled trials.
> حالة نظام الحوكمة: **BETA**. هذه السياسة مُطبّقة اليوم في التجارب المحكومة.

Cross-links: [`MODULE_STATUS_MAP.md`](../00_platform_truth/MODULE_STATUS_MAP.md) · [`GOVERNANCE_OS.md`](../05_governance_os/GOVERNANCE_OS.md)

---

## EN — The approval-first principle

Dealix runs on one operating rule: **AI explores, analyzes, and recommends; deterministic workflows execute; humans approve critical external commitments.** No customer-facing external action leaves the system on its own. A founder approves it first.

This is not a courtesy step. It is a control. The system can draft a message, score an opportunity, or assemble a price option in seconds, but the decision to send, publish, or commit stays with a named human. The machine proposes; the founder disposes.

### What requires founder approval before it happens

Approval is mandatory for every action that touches a person, a market, or a commitment outside Dealix:

- **Outbound messages.** Any WhatsApp, email, or message draft addressed to a real recipient. Drafts are generated; sends are approved.
- **Publishing a customer name.** No customer, logo, quote, or case detail goes public until the customer consents and the founder approves. Until then, case material is labeled "Hypothetical / case-safe template".
- **Price commitments.** Any quoted price, discount, scope promise, or contractual term presented to a customer.
- **Public claims.** Any marketing or sales claim about results, capability, or compliance. These must already exist in [`CLAIMS_REGISTER.md`](./CLAIMS_REGISTER.md) as "Allowed".
- **Data sharing.** Sending any customer or third-party data outside the system.
- **Anything irreversible or reputational.** If undoing it would require an apology, it needs approval.

### The approval record

Every approval is logged. The record carries:

| Field | Meaning |
|---|---|
| Action ID | Unique reference for the proposed action |
| Action type | Message / publish / price / claim / data-share |
| Recipient or audience | Anonymized label, never raw PII |
| Draft reference | Pointer to the exact draft approved |
| Approver | Named founder/team member |
| Decision | Approve / reject / edit-and-resend |
| Timestamp | When the decision was made |
| Notes | Conditions or edits applied |

The record stores **no PII** — recipients are referenced by anonymized label, in line with our no-PII-in-logs rule.

### What this policy refuses

It refuses any path where an agent acts externally without a human and without identity. No agent runs without an identity; no external action runs without approval. These are non-negotiables, not preferences. The system will not auto-send, auto-publish, or auto-commit, even when it is confident.

### Why it matters

Trust is the product. A single un-approved send to the wrong recipient costs more than a week of careful work. Approval-first keeps speed in drafting while keeping judgment in commitment.

---

## AR — مبدأ الموافقة أولاً

تعمل Dealix بقاعدة تشغيلية واحدة: **الذكاء الاصطناعي يستكشف ويحلّل ويوصي؛ سير العمل الحتمي ينفّذ؛ والبشر يوافقون على الالتزامات الخارجية الحرجة.** لا يخرج أي إجراء خارجي موجّه للعميل من النظام تلقائياً. يوافق عليه المؤسس أولاً.

هذه ليست خطوة مجاملة، بل ضابط تحكّم. يستطيع النظام صياغة رسالة أو تقييم فرصة أو تجهيز خيار سعري في ثوانٍ، لكن قرار الإرسال أو النشر أو الالتزام يبقى بيد إنسان مُسمّى. الآلة تقترح، والمؤسس يقرّر.

### ما الذي يتطلب موافقة المؤسس قبل حدوثه

الموافقة إلزامية لكل إجراء يمسّ شخصاً أو سوقاً أو التزاماً خارج Dealix:

- **الرسائل الصادرة.** أي مسودة واتساب أو بريد أو رسالة موجّهة لمستلم حقيقي. تُصاغ المسودات، وتُعتمد عمليات الإرسال.
- **نشر اسم عميل.** لا يُنشر اسم عميل أو شعار أو اقتباس أو تفصيل حالة حتى يوافق العميل ويعتمد المؤسس. حتى ذلك الحين تُوسَم مواد الحالة بـ"نموذج افتراضي آمن".
- **الالتزامات السعرية.** أي سعر أو خصم أو وعد نطاق أو بند تعاقدي يُعرَض على العميل.
- **الادعاءات العامة.** أي ادعاء تسويقي أو بيعي عن النتائج أو القدرة أو الامتثال. يجب أن يكون موجوداً مسبقاً في [`CLAIMS_REGISTER.md`](./CLAIMS_REGISTER.md) بوصفه "مسموح".
- **مشاركة البيانات.** إرسال أي بيانات عميل أو طرف ثالث خارج النظام.
- **أي إجراء غير قابل للتراجع أو يمسّ السمعة.** إذا كان التراجع عنه يتطلب اعتذاراً، فهو يحتاج موافقة.

### سجل الموافقة

تُسجَّل كل موافقة. يحمل السجل:

| الحقل | المعنى |
|---|---|
| معرّف الإجراء | مرجع فريد للإجراء المقترح |
| نوع الإجراء | رسالة / نشر / سعر / ادعاء / مشاركة بيانات |
| المستلم أو الجمهور | وسم مجهول الهوية، لا بيانات شخصية خام |
| مرجع المسودة | مؤشر إلى المسودة المعتمدة بالضبط |
| المُعتمِد | مؤسس/عضو فريق مُسمّى |
| القرار | اعتماد / رفض / تعديل وإعادة إرسال |
| الطابع الزمني | وقت اتخاذ القرار |
| ملاحظات | الشروط أو التعديلات المطبّقة |

لا يخزّن السجل **أي بيانات شخصية** — يُشار إلى المستلمين بوسم مجهول، التزاماً بقاعدة عدم وضع البيانات الشخصية في السجلات.

### ما ترفضه هذه السياسة

ترفض أي مسار يتصرّف فيه وكيل خارجياً دون إنسان ودون هوية. لا يعمل وكيل بلا هوية؛ ولا يجري إجراء خارجي بلا موافقة. هذه محظورات غير قابلة للتفاوض، لا تفضيلات. لن يرسل النظام أو ينشر أو يلتزم تلقائياً، حتى عند ثقته.

### لماذا يهم هذا

الثقة هي المنتج. إرسالة واحدة غير معتمدة لمستلم خاطئ تكلّف أكثر من أسبوع عمل دقيق. الموافقة أولاً تُبقي السرعة في الصياغة والحُكم في الالتزام.

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
