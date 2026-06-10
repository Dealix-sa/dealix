# External Actions Policy — No External Action Without Approval — سياسة الإجراءات الخارجية

> Governance OS status: **BETA**. Enforced in controlled trials.
> حالة نظام الحوكمة: **BETA**. مُطبّقة في التجارب المحكومة.

Cross-links: [`MODULE_STATUS_MAP.md`](../00_platform_truth/MODULE_STATUS_MAP.md) · [`GOVERNANCE_OS.md`](../05_governance_os/GOVERNANCE_OS.md) · [`HUMAN_APPROVAL_POLICY.md`](./HUMAN_APPROVAL_POLICY.md) · [`NO_SPAM_POLICY.md`](./NO_SPAM_POLICY.md)

---

## EN — The rule

No customer-facing external action happens without founder approval. This is the operating rule made concrete: AI explores, analyzes, and recommends; deterministic workflows execute; humans approve critical external commitments. The system may draft and prepare any external action, but it may not perform one. Dealix never implies it sends external messages on a customer's behalf without explicit approval.

### Allowed vs forbidden actions

| Action | Allowed? | Condition |
|---|---|---|
| Draft an outbound message | Yes | Human writes or reviews; never auto-sent |
| Send an approved message | Yes | One-by-one, founder-approved, opt-out respected |
| Assemble a price option | Yes | Quoted only after founder approval |
| Publish a customer name or logo | Yes | Only with customer consent and founder approval |
| Use a marketing claim | Yes | Only if "Allowed" in [`CLAIMS_REGISTER.md`](./CLAIMS_REGISTER.md) |
| Auto-send WhatsApp / email | No | Forbidden; human approves each send |
| Cold WhatsApp automation | No | Forbidden as service and internal tool |
| LinkedIn automation | No | No bots, no auto-messaging, no scraping |
| Mass / batch outreach | No | About 5 manual sends per day, maximum |
| Act as an agent without identity | No | No agent runs without an identity |
| Any irreversible external commitment | No | Requires explicit founder approval first |

### How drafts flow through the approval gate

1. **Explore.** The system researches and recommends an action with sourced reasoning.
2. **Draft.** A deterministic workflow assembles the exact artifact — message, price option, or public claim.
3. **Stage.** The draft enters the approval gate with an anonymized recipient label. No raw PII is logged.
4. **Approve.** A named founder reviews and chooses: approve, reject, or edit-and-resend.
5. **Execute.** Only an approved draft is sent, published, or committed.
6. **Record.** The decision is logged per [`HUMAN_APPROVAL_POLICY.md`](./HUMAN_APPROVAL_POLICY.md), with no PII in the record.

Nothing skips the gate. The system will not send, publish, or commit on its own, even when confident. Speed lives in drafting; judgment lives in approval.

---

## AR — القاعدة

لا يحدث أي إجراء خارجي موجّه للعميل دون موافقة المؤسس. هذه هي القاعدة التشغيلية مُجسَّدة: الذكاء الاصطناعي يستكشف ويحلّل ويوصي؛ سير العمل الحتمي ينفّذ؛ والبشر يوافقون على الالتزامات الخارجية الحرجة. للنظام أن يصوغ ويجهّز أي إجراء خارجي، لكن ليس له أن ينفّذه. ولا تُلمّح Dealix أبداً أنها ترسل رسائل خارجية نيابةً عن العميل دون موافقة صريحة.

### المسموح مقابل المحظور

| الإجراء | مسموح؟ | الشرط |
|---|---|---|
| صياغة رسالة صادرة | نعم | يكتبها أو يراجعها إنسان؛ لا تُرسَل تلقائياً |
| إرسال رسالة معتمدة | نعم | واحدة تلو الأخرى، بموافقة المؤسس، مع احترام إلغاء الاشتراك |
| تجهيز خيار سعري | نعم | يُعرَض السعر بعد موافقة المؤسس فقط |
| نشر اسم عميل أو شعار | نعم | بموافقة العميل واعتماد المؤسس فقط |
| استخدام ادعاء تسويقي | نعم | فقط إن كان "مسموح" في [`CLAIMS_REGISTER.md`](./CLAIMS_REGISTER.md) |
| إرسال واتساب / بريد تلقائي | لا | محظور؛ يوافق إنسان على كل إرسال |
| أتمتة واتساب باردة | لا | محظورة كخدمة وكأداة داخلية |
| أتمتة لينكدإن | لا | لا روبوتات، لا مراسلة تلقائية، لا كشط |
| تواصل بالجملة / دفعات | لا | نحو 5 إرساليات يدوية في اليوم كحدّ أقصى |
| التصرّف كوكيل بلا هوية | لا | لا يعمل وكيل بلا هوية |
| أي التزام خارجي غير قابل للتراجع | لا | يتطلب موافقة مؤسس صريحة أولاً |

### كيف تمرّ المسودات عبر بوابة الموافقة

1. **الاستكشاف.** يبحث النظام ويوصي بإجراء مع تعليل موثّق بمصدر.
2. **الصياغة.** يجمع سير عمل حتمي القطعة بالضبط — رسالة أو خيار سعر أو ادعاء عام.
3. **التهيئة.** تدخل المسودة بوابة الموافقة بوسم مستلم مجهول. لا تُسجَّل بيانات شخصية خام.
4. **الموافقة.** يراجع مؤسس مُسمّى ويختار: اعتماد أو رفض أو تعديل وإعادة إرسال.
5. **التنفيذ.** تُرسَل أو تُنشَر أو يُلتزَم بمسودة معتمدة فقط.
6. **التسجيل.** يُسجَّل القرار وفق [`HUMAN_APPROVAL_POLICY.md`](./HUMAN_APPROVAL_POLICY.md)، دون بيانات شخصية في السجل.

لا شيء يتخطى البوابة. لن يرسل النظام أو ينشر أو يلتزم من تلقاء نفسه، حتى عند ثقته. السرعة في الصياغة، والحُكم في الموافقة.

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
