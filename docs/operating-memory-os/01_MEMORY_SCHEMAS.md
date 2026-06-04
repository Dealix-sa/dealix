# مخططات الذاكرة | Memory Schemas

> **AR:** يصف هذا المستند مخططات الذاكرة التشغيلية المعرّفة في `config/operating_memory_schemas.json`، وأداة التحقق `scripts/operating_memory_validate.py`. المخططات تضمن أن كل سجل قرار/عميل/سوق/إيراد يلتزم ببنية ثابتة قابلة للتدقيق قبل اعتماده.
>
> **EN:** This document describes the operating-memory schemas defined in `config/operating_memory_schemas.json`, and the validator `scripts/operating_memory_validate.py`. The schemas guarantee that every decision/client/market/revenue record conforms to a stable, auditable structure before it is committed.

## ملف المخططات | Schema File

`config/operating_memory_schemas.json` يحتوي على أربعة مخططات جذرية / contains four root schemas:

| المخطط Schema | المعرّف Type | الغرض Purpose |
|---|---|---|
| `decision_memory` | `decision` | بنية سجل القرار / Decision record structure |
| `client_memory` | `client` | بنية سجل العميل / Client record structure |
| `market_memory` | `market` | بنية سجل السوق / Market record structure |
| `revenue_memory` | `revenue` | بنية سجل الإيراد / Revenue record structure |

## الحقول المشتركة | Common Fields

كل سجل يشترك في الحقول التالية / Every record shares:

- `id` — معرّف فريد / unique identifier.
- `type` — أحد: decision | client | market | revenue.
- `created_at` / `updated_at` — طوابع زمنية ISO-8601.
- `status` — `draft` \| `approved` \| `archived`.
- `approved_by` — يبقى فارغًا حتى موافقة المؤسس / empty until founder approval.
- `source` — أصل السجل (manual / ai-draft).

## مخطط القرار | Decision Schema

- `decision`, `context`, `alternatives[]`, `rationale`, `outcome`, `review_date`.

## مخطط العميل | Client Schema

- `client_name`, `segment`, `need`, `relationship_stage`, `last_interaction`, `notes` (بدون بيانات حساسة / no sensitive data).

## مخطط السوق | Market Schema

- `sector`, `signal`, `hypothesis`, `confidence` (low/medium/high), `evidence_ref`.

## مخطط الإيراد | Revenue Schema

- `deal_stage`, `amount`, `currency`, `probability`, `verified` (bool), `verification_ref`.

## أداة التحقق | Validator

`scripts/operating_memory_validate.py` يقوم بـ / performs:

1. تحميل المخططات من `config/operating_memory_schemas.json`. / Load schemas.
2. التحقق من كل سجل مقابل مخطط نوعه. / Validate each record against its type schema.
3. رفض الحقول غير المعرّفة والقيم المفقودة. / Reject undefined fields and missing required values.
4. **فحص الأمان:** يرفض أي سجل يحتوي مفاتيح/أسرار أو طلب إرسال خارجي. / Safety check: rejects records containing secrets or any external-send request.
5. إخراج تقرير PASS/FAIL بدون تنفيذ أي فعل خارجي. / Emit PASS/FAIL report; no external action executed.

```bash
python scripts/operating_memory_validate.py --records data/operating_memory/
```

## قواعد الأمان | Safety Rules

- المُحقِّق لا يرسل ولا يقدّم ولا يطلق أي شيء — تحقق فقط. / Validator only validates; it never sends, submits, or launches.
- AI prepares, Founder approves, Manual action only, No external sending.
- لا تُخزَّن مفاتيح API أو أسرار في أي سجل. / No API keys or secrets stored in any record.
