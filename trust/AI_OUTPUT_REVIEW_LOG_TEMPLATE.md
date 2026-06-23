# AI Output Review Log Template

قالب سجل مراجعة مخرجات الذكاء الاصطناعي

## الغرض

توحيد كيفية تسجيل كل مخرج ذكاء اصطناعي يُراجَع قبل الاستخدام
الخارجي. كل مخرج LLM يستخدم في سياق خارجي (إيميل، واتساب،
رسالة نصية، محتوى عام) يجب أن يُسجَّل في هذا السجل.

## الحقول الإلزامية

| الحقل | الوصف | مثال |
|---|---|---|
| `review_id` | معرّف فريد للمراجعة | `rev-2026-06-23-001` |
| `draft_id` | معرّف المسودة المراجَعة | `draft-demo-acc-001-ar` |
| `source` | مصدر المخرج (سكربت/مسار) | `scripts/generate_outreach_drafts.py` |
| `channel` | القناة المستهدفة | `email` / `whatsapp` / `sms` / `public` |
| `destination` | الوجهة (مُقَنَّعة) | `ah***@example.sa` |
| `model` | النموذج المولِّد | `deepseek-chat` |
| `generated_at` | توقيت التوليد | `2026-06-23T14:30:00+03:00` |
| `reviewer` | المراجِع | `Sami` |
| `reviewed_at` | توقيت المراجعة | `2026-06-23T15:00:00+03:00` |
| `review_status` | نتيجة المراجعة | `approved` / `rejected` / `revisions_requested` |
| `issues_found` | القضايا المكتشفة | `["forbidden_claim:guaranteed roi"]` |
| `corrective_action` | الإجراء التصحيحي | `removed guaranteed claim, added evidence ref` |
| `consent_record_id` | معرّف سجل الموافقة (للتواصل) | `con_12345` |
| `suppression_checked` | تم فحص قائمة الإيقاف؟ | `true` / `false` |
| `notes` | ملاحظات إضافية | نص حرّ |

## قالب السجل (JSON)

```json
{
  "review_id": "rev-2026-06-23-001",
  "draft_id": "draft-demo-acc-001-ar",
  "source": "scripts/generate_outreach_drafts.py",
  "channel": "email",
  "destination": "ah***@example.sa",
  "model": "deepseek-chat",
  "generated_at": "2026-06-23T14:30:00+03:00",
  "reviewer": "Sami",
  "reviewed_at": "2026-06-23T15:00:00+03:00",
  "review_status": "approved",
  "issues_found": [],
  "corrective_action": "",
  "consent_record_id": "con_12345",
  "suppression_checked": true,
  "notes": "Draft clean, approved for send."
}
```

## مسار المراجعة

1. **التوليد**: المخرج يُحفظ كمسودة بحالة `draft`.
2. **الفحص التلقائي**: `audit_draft_text()` + `audit_claim_safety()`.
3. **المراجعة البشرية**: المراجِع يفحص المحتوى، يسجّل القضايا،
   يقرّر الحالة.
4. **الإجراء**: `approved` → جاهز للإرسال (مع فحص الإيقاف)؛
   `rejected` → إعادة التوليد؛ `revisions_requested` → تعديل.
5. **التوثيق**: السجل يُحفظ في `business/_data/ai_output_review_log.json`.

## القواعد

- **لا إرسال بدون سجل مراجعة مكتمل بحالة `approved`**.
- **لا تخطّي المراجعة البشرية** لأي مخرج LLM خارجي.
- **كل ادعاء ممنوع يُسجَّل** في `issues_found`.
- السجل متاح للتدقيق من الهيئة عند الحاجة.

## الاختبارات ذات الصلة

- `tests/test_no_auto_external_send.py`
- `tests/test_outreach_drafts.py`
- `tests/test_output_quality_gate.py`

## المصادقة

- **المسؤول**: المراجِعون + فريق الامتثال
- **المراجعة**: ربع سنوي
- **المراجع**: `AI_USAGE_POLICY_AR.md`، `HUMAN_APPROVAL_GATES.md`