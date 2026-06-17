# سياسة الأفعال الخارجية — External Actions Policy — Dealix

> **القاعدة الحاكمة:** أي فعل يعبر حدود Dealix هو **A3 فأعلى**، ويتطلب **موافقة المؤسس + قيد في سجل التدقيق (audit log)**.
> الوكلاء (agents) **يجهّزون** الفعل الخارجي، ولا **ينفّذونه** أبدًا بلا موافقة.
> هذه وثيقة سياسة **قابلة للإنفاذ**.

الجمهور: المؤسس، التشغيل، طبقة الوكلاء (Agent OS). النطاق: كل فعل يغادر حدود Dealix.

---

## 1. ما هو الفعل الخارجي — What Counts as External

أي فعل يصل طرفًا خارج Dealix، ومنه:

- **الرسائل (messages):** واتساب، بريد، أي تواصل مع طرف خارجي.
- **النشر (publishing):** case study، claim عام، محتوى، اسم/شعار عميل.
- **المدفوعات (payments):** أي حركة مالية صادرة أو التزام مالي.
- **مشاركة البيانات (data sharing):** تمرير بيانات لطرف ثالث أو sub-processor.
- **نداءات API لطرف ثالث (third-party API calls):** أي استدعاء يرسل بيانات خارج الحدود.

> EN: Any action that leaves Dealix's boundary — messages, publishing, payments, data sharing, third-party API calls — is external.

---

## 2. التصنيف — Classification

كل فعل خارجي = **A3** على الأقل. يرتفع التصنيف بحسب الأثر:

| الفعل الخارجي | Class | ملاحظة |
|---|---|---|
| إرسال رسالة/بريد لعميل | A3 | يدوي + موافقة + audit log |
| نشر case study (يحمل اسم عميل) | A2 + A3 | يلزم موافقة العميل الموثّقة على اسمه |
| نشر claim عام | A2 + A3 | يمر على [`CLAIMS_REGISTER.md`](CLAIMS_REGISTER.md) |
| مشاركة بيانات مع طرف ثالث | A3 / A4 | A4 إن لمست أساسًا قانونيًا/تعاقديًا |
| دفع / التزام مالي | A4 | المؤسس (+ مستشار) |
| حذف بيانات لدى طرف خارجي | A5 | dry-run + تأكيد مزدوج |

تعريفات الفئات الكاملة: [`HUMAN_APPROVAL_POLICY.md`](HUMAN_APPROVAL_POLICY.md).

---

## 3. قائمة فحص الفعل الخارجي — External-Action Checklist

لا يُنفَّذ فعل خارجي حتى تُجاب **كل** البنود التالية بوضوح وتُسجَّل:

1. **ماذا (what):** الفعل بالضبط، والمحتوى النهائي (artifact ref).
2. **لمن (to whom):** الطرف المتلقّي محدّد ومعروف، لا قائمة مجهولة.
3. **الدليل (evidence):** ملف دليل يبرّر الفعل (every action needs evidence).
4. **الموافقة (approval):** قيد موافقة المؤسس في Approval Register، A3+.
5. **القابلية للعكس (reversibility):** هل الفعل قابل للتراجع؟ إن لا، تأكيد إضافي.
6. **السجل (log):** قيد في audit log بعد التنفيذ يربط الفعل بقرار الموافقة.

> EN checklist: what · to whom · evidence · approval · reversibility · log. No external action ships without all six recorded.

### شكل قيد التدقيق — Audit-Log Entry

```json
{
  "audit_id": "AUD-2026-0001",
  "approval_ref": "APR-2026-0001",
  "class": "A3",
  "action": "send_whatsapp_draft",
  "recipient_ref": "account_4821",
  "artifact_ref": "drafts/lead_4821_intro.md",
  "evidence_ref": "research/account_4821_evidence.md",
  "reversible": true,
  "executed_by": "founder",
  "executed_at": "2026-06-05T09:20:00Z"
}
```

السجل **append-only**؛ لا تعديل بعد الإقفال، التصحيح بقيد جديد.

---

## 4. الربط بـ Agent OS — Prepare vs Execute

- الوكلاء **يجهّزون** الأفعال الخارجية حتى مستوى المسودة (A2): يصيغون الرسالة، يجمعون الدليل، يملؤون قائمة الفحص.
- الوكلاء **لا ينفّذون** أي A3+ إطلاقًا. يتوقفون عند بوابة الموافقة وينتظرون قرار المؤسس.
- لا يوجد مسار auto-execute في Dealix لأي فعل خارجي.

> EN: Agents may PREPARE external actions up to draft (A2). They never EXECUTE A3+ without founder approval. No auto-execute path exists.

التفصيل: [`../02_operating_systems/GOVERNANCE_OS.md`](../02_operating_systems/GOVERNANCE_OS.md).

---

## 5. الإنفاذ — Enforcement

- أي فعل خارجي بلا قيد موافقة + قيد تدقيق = **حادثة حوكمة (governance incident)** تُسجَّل وتُراجَع.
- لا نشر اسم عميل بلا موافقته الموثّقة (no client name publishing without approval).
- KPI: **صفر أفعال خارجية بلا موافقة وقيد تدقيق**.

---

## روابط مرجعية — Related

- [`HUMAN_APPROVAL_POLICY.md`](HUMAN_APPROVAL_POLICY.md)
- [`NO_SPAM_POLICY.md`](NO_SPAM_POLICY.md)
- [`CLAIMS_REGISTER.md`](CLAIMS_REGISTER.md)
- [`DATA_RETENTION.md`](DATA_RETENTION.md)
- [`../02_operating_systems/GOVERNANCE_OS.md`](../02_operating_systems/GOVERNANCE_OS.md)

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
