# Lead Ops Final QA — الفحص النهائي لعمليات العملاء المحتملين

> QA checklist for the CRM and Lead Ops layer. The schema is validated by `scripts/commercial_crm_schema_verify.py` against `config/crm_pipeline_schema.json`. No personal sensitive data is collected or stored beyond what the schema allows, and nothing is sent externally.
>
> قائمة فحص لطبقة CRM وعمليات العملاء المحتملين. يُتحقق من المخطط بواسطة `scripts/commercial_crm_schema_verify.py` مقابل `config/crm_pipeline_schema.json`. لا تُجمع أو تُخزَّن بيانات شخصية حساسة بما يتجاوز ما يسمح به المخطط، ولا يُرسل أي شيء خارجيًا.

---

## EN — QA checklist

| # | Check | Pass criteria | Reference |
|---|---|---|---|
| 1 | Lead schema valid | Verifier passes; required fields present | `scripts/commercial_crm_schema_verify.py`, `config/crm_pipeline_schema.json` |
| 2 | CRM stages defined | New → Qualified → Contacted → Discovery → Diagnostic → Pilot → Retainer → Closed | `config/crm_pipeline_schema.json` |
| 3 | Suppression process | Suppressed leads are excluded from draft generation | draft factory + schema |
| 4 | Manual approval enforced | Every draft `requires_founder_approval=true`; no auto-send | draft queue flags |
| 5 | Reply classification | Replies tagged: interested / not now / not relevant / do-not-contact | CRM stage notes |
| 6 | Diagnostic booked | Stage updates when a paid diagnostic is scheduled | CRM stages |
| 7 | Pilot proposed | Stage updates when a pilot proposal is sent manually | CRM stages |
| 8 | Retainer conversion | Stage updates on Managed Ops agreement | CRM stages |
| 9 | Disqualification | Clear reason code recorded; lead removed from active outreach | CRM stages |
| 10 | Source tracking | Each lead has a source/vertical tag for attribution | `config/crm_pipeline_schema.json` |
| 11 | No personal sensitive data | No national ID, no sensitive personal data; email/phone only where schema permits and never before agreement | schema forbidden-field rules |

### Acceptance
- The schema verifier must pass with no errors.
- No forbidden field appears in any stored lead record.
- Every outbound draft references an approved, manually sent message — never an automated send.
- "Do-not-contact" is honored immediately and permanently via suppression.

---

## AR — قائمة الفحص

| # | الفحص | معيار النجاح | المرجع |
|---|---|---|---|
| 1 | صحة مخطط العميل | نجاح المدقق؛ الحقول المطلوبة موجودة | `scripts/commercial_crm_schema_verify.py`، `config/crm_pipeline_schema.json` |
| 2 | تعريف مراحل CRM | جديد ← مؤهَّل ← تم التواصل ← استكشاف ← تشخيص ← تجريبي ← عقد شهري ← مغلق | `config/crm_pipeline_schema.json` |
| 3 | عملية القمع | يُستبعد العملاء المقموعون من توليد المسودات | مصنع المسودات + المخطط |
| 4 | فرض الموافقة اليدوية | كل مسودة `requires_founder_approval=true`؛ لا إرسال تلقائي | أعلام طابور المسودات |
| 5 | تصنيف الردود | تُوسم الردود: مهتم / ليس الآن / غير ذي صلة / عدم التواصل | ملاحظات مراحل CRM |
| 6 | حجز التشخيص | تتحدث المرحلة عند جدولة تشخيص مدفوع | مراحل CRM |
| 7 | اقتراح التجريبي | تتحدث المرحلة عند إرسال عرض تجريبي يدويًا | مراحل CRM |
| 8 | تحويل العقد الشهري | تتحدث المرحلة عند اتفاق إدارة العمليات | مراحل CRM |
| 9 | الاستبعاد | تسجيل رمز سبب واضح؛ إزالة العميل من التواصل النشط | مراحل CRM |
| 10 | تتبع المصدر | لكل عميل وسم مصدر/قطاع للإسناد | `config/crm_pipeline_schema.json` |
| 11 | لا بيانات شخصية حساسة | لا هوية وطنية، لا بيانات شخصية حساسة؛ البريد/الهاتف فقط حيث يسمح المخطط وأبدًا قبل الاتفاق | قواعد الحقول الممنوعة في المخطط |

### القبول
- يجب أن ينجح مدقق المخطط دون أخطاء.
- لا يظهر أي حقل ممنوع في أي سجل عميل مخزَّن.
- كل مسودة صادرة تشير إلى رسالة معتمدة مُرسلة يدويًا — وليس إرسالًا آليًا.
- يُحترم "عدم التواصل" فورًا ودائمًا عبر القمع.

---

Related: [Final Launch Control Tower](../launch-control/00_FINAL_LAUNCH_CONTROL_TOWER.md) · [Go / No-Go Matrix](../launch-control/02_GO_NO_GO_MATRIX.md)

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
