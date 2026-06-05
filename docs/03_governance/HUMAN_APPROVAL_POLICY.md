# سياسة الموافقة البشرية — Human Approval Policy — Dealix

> **القاعدة الأساسية (Approval-First):** لا فعل خارجي يصدر من Dealix دون موافقة بشرية مُسجَّلة.
> الأنظمة (Agent OS) **تُجهِّز** (prepare)، والإنسان **يوافق ويُنفِّذ** (approve & execute).
> هذه وثيقة سياسة **قابلة للإنفاذ (enforceable)**، وليست توجيهًا اختياريًا.

الجمهور: المؤسس، فريق التشغيل، طبقة الوكلاء (agents). النطاق: كل فعل داخل أو خارج حدود Dealix.

---

## 1. تصنيفات الموافقة — Approval Classes (A0–A5)

| Class | الاسم | الوصف | من يوافق | تسجيل إلزامي |
|---|---|---|---|---|
| **A0** | مسودة داخلية — internal draft | محتوى أولي لم يخرج لأي طرف، حتى داخليًا للمراجعة الرسمية. | لا أحد (المُنشئ) | لا |
| **A1** | تحليل داخلي — internal analysis | بحث، scoring، تقرير داخلي، targeting لا يصل لأي طرف خارجي. | مالك المهمة | اختياري |
| **A2** | مسودة موجهة للعميل — customer-facing draft | عرض، رسالة، case study، claim جاهز للعرض على عميل أو الجمهور. | **المؤسس** | **نعم** |
| **A3** | فعل خارجي — external action | إرسال رسالة، نشر، مشاركة بيانات، نداء API لطرف ثالث، دفع. | **المؤسس** | **نعم + audit log** |
| **A4** | قانوني / مالي / أمني — legal·financial·security | توقيع DPA، التزام تعاقدي، تغيير صلاحيات، إفصاح أمني. | **المؤسس** (+ مستشار عند اللزوم) | **نعم + audit log** |
| **A5** | فعل مُدمِّر — destructive | حذف بيانات عميل، حذف backup، rollback إنتاجي، إنهاء حساب. | **المؤسس** (تأكيد مزدوج) | **نعم + audit log + dry-run** |

**القاعدة الحاكمة:** كل ما هو **A2 فأعلى** يتطلب **موافقة المؤسس** قبل التنفيذ. A0/A1 لا تتطلب موافقة لكنها لا تخرج من حدود Dealix إطلاقًا.

> Rule of thumb (EN): A0–A1 stay inside. A2+ needs founder approval. A3+ also needs an audit-log entry. A5 needs a dry-run first.

---

## 2. ما معنى "موافقة" — Definition of Approval

الموافقة ليست رسالة "تمام". الموافقة الصحيحة هي **قيد مُسجَّل (recorded decision)** يحتوي:

- **من (who):** هوية المُوافِق — المؤسس لكل ما هو A2+.
- **كيف (how):** قناة موثّقة (Approval Register / قناة موافقات محددة)، لا موافقة شفهية غير مسجّلة.
- **متى (when):** timestamp دقيق (UTC + AST).
- **القرار (decision):** `approved` / `rejected` / `approved_with_conditions`.
- **الشروط (conditions):** أي تعديل مطلوب قبل التنفيذ.
- **الأدلة (evidence):** الرابط للمسودة/الهدف ودليل الاستحقاق (every target needs evidence).

موافقة بدون هذه الحقول = **لا موافقة**. لا يُنفَّذ الفعل.

---

## 3. سجل الموافقات — Approval Register (field shape)

```json
{
  "approval_id": "APR-2026-0001",
  "class": "A3",
  "action": "send_whatsapp_draft",
  "artifact_ref": "drafts/lead_4821_intro.md",
  "target_ref": "account_4821",
  "evidence_ref": "research/account_4821_evidence.md",
  "requested_by": "ops",
  "requested_at": "2026-06-05T08:30:00Z",
  "approver": "founder",
  "decision": "approved_with_conditions",
  "conditions": "remove pricing line; send after 10:00 AST",
  "decided_at": "2026-06-05T09:05:00Z",
  "reversible": true,
  "audit_log_ref": "logs/audit/2026-06-05.json#APR-2026-0001"
}
```

السجل **append-only**: لا يُعدَّل قيد بعد إقفاله؛ يُضاف قيد جديد للتصحيح.

---

## 4. خريطة الأفعال الشائعة — Action → Class Map

| الفعل | Class | ملاحظة |
|---|---|---|
| توليد مسودة بحث داخلي | A0/A1 | لا تخرج خارجيًا |
| scoring / targeting داخلي | A1 | يحتاج evidence لكل هدف |
| تجهيز draft رسالة عميل | A2 | جاهز للعرض، لم يُرسَل |
| **إرسال draft واتساب** | **A3** | يدوي، بموافقة المؤسس فقط |
| إرسال بريد لعميل | A3 | يدوي + موافقة |
| **نشر case study** | **A2 + A3** | A2 للمحتوى، A3 للنشر؛ يلزم موافقة العميل على اسمه |
| نشر claim عام | A2 + A3 | يمر عبر [`CLAIMS_REGISTER.md`](CLAIMS_REGISTER.md) |
| مشاركة بيانات مع طرف ثالث | A3 / A4 | راجع [`EXTERNAL_ACTIONS_POLICY.md`](EXTERNAL_ACTIONS_POLICY.md) |
| توقيع DPA / التزام مالي | A4 | موافقة المؤسس + مستشار |
| **حذف بيانات عميل** | **A5** | dry-run + تأكيد مزدوج |
| rollback إنتاجي / حذف backup | A5 | تأكيد مزدوج |

---

## 5. الإنفاذ — Enforcement

- لا يوجد مسار auto-send لأي A3+ في Dealix.
- الوكلاء (agents) قد تصل بأفعالها حتى A2 (تجهيز) فقط، ثم تتوقف وتنتظر قيد موافقة.
- أي A3+ نُفِّذ بدون قيد في Approval Register = **حادثة حوكمة (governance incident)** تُسجَّل وتُراجَع.
- مؤشر KPI: **صفر أفعال خارجية بدون موافقة مُسجَّلة**.

---

## روابط مرجعية — Related

- [`EXTERNAL_ACTIONS_POLICY.md`](EXTERNAL_ACTIONS_POLICY.md)
- [`CLAIMS_REGISTER.md`](CLAIMS_REGISTER.md)
- [`NO_SPAM_POLICY.md`](NO_SPAM_POLICY.md)
- [`../governance/APPROVAL_MATRIX.md`](../governance/APPROVAL_MATRIX.md)
