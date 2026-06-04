# Manual Events Ledger — سجل الأحداث اليدوية

## الغرض (AR)
يصف هذا المستند مخطط ملف `data/revenue_manual_events.example.jsonl`، وهو سجل بصيغة JSON Lines يدوّن فيه المؤسس **يدويًا** كل حدث إيرادي حدث فعلًا. السجل هو مصدر الحقيقة الوحيد للوحة المؤشرات وقواعد خط الأنابيب. **تسجيل يدوي فقط — لا إرسال ولا أتمتة خارجية.**

## Purpose (EN)
This document describes the schema of `data/revenue_manual_events.example.jsonl`, a JSON Lines ledger where the founder **manually** records every revenue event that actually occurred. The ledger is the single source of truth for the dashboard and pipeline rules. **Manual recording only — no sending and no external automation.**

## المخطط / Schema

| الحقل / Field | النوع / Type | الوصف / Description |
|---|---|---|
| event_id | string | معرّف فريد للحدث / Unique event identifier |
| created_at | string (ISO 8601) | وقت التسجيل / Timestamp of recording |
| event_type | enum | نوع الحدث (انظر أدناه) / Event type (see below) |
| company | string | اسم الشركة / Company name |
| vertical | string | القطاع / Vertical |
| source_draft_id | string | معرّف المسودة المصدر / Source draft id |
| channel | string | القناة (التواصل تم يدويًا) / Channel (contact was manual) |
| amount_sar | number | المبلغ بالريال إن وُجد / Amount in SAR if any |
| stage_before | enum | المرحلة قبل الحدث / Stage before |
| stage_after | enum | المرحلة بعد الحدث / Stage after |
| notes | string | ملاحظات / Notes |
| founder_initials | string | الأحرف الأولى للمؤسس (إقرار يدوي) / Founder initials (manual attestation) |

## أنواع الأحداث المسموحة / Allowed event_type
- `manual_send_recorded` — تسجيل إرسال يدوي / a manual send was recorded
- `reply_positive` — رد إيجابي / positive reply
- `reply_negative` — رد سلبي / negative reply
- `discovery_booked` — حجز مكالمة اكتشاف / discovery call booked
- `diagnostic_sold` — بيع تشخيص / diagnostic sold
- `diagnostic_delivered` — تسليم تشخيص / diagnostic delivered
- `pilot_proposed` — عرض تجربة / pilot proposed
- `pilot_sold` — بيع تجربة / pilot sold
- `retainer_started` — بدء عقد شهري / retainer started
- `lost` — فقدان الصفقة / deal lost
- `suppressed` — استبعاد (عدم التواصل) / suppressed (do-not-contact)

## قواعد التسجيل / Recording Rules
- كل سطر حدث واحد بصيغة JSON صالحة.
- `manual_send_recorded` يعني أن المؤسس أرسل بنفسه؛ النظام لم يرسل.
- `founder_initials` إلزامي كإقرار يدوي.
- لا تُسجّل أحداثًا لم تحدث (لا جذب وهمي).

One JSON object per line. `manual_send_recorded` means the founder sent it personally. `founder_initials` is a required manual attestation. Never record events that did not happen (no fake traction).

## السلامة / Safety
الملف سجل توثيقي فقط؛ قراءته لا تُطلق أي إرسال أو كشط أو أتمتة خارجية.
The file is a documentation ledger only; reading it never triggers any sending, scraping, or external automation.
