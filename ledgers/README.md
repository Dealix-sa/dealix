# Dealix Founder Ledgers — سجلات المؤسس

> طبقة خفيفة وإضافية فوق نظام Dealix الحالي. مكان واحد يكتب فيه المؤسس **القرارات والوقائع** بصيغة منظّمة قابلة للتحقق — وليست بديلاً عن مصدر الحقيقة التشغيلي.

A lightweight, **additive** layer on top of the existing Dealix system. One place
for the founder to record structured, verifiable facts — not a replacement for the
operational source of truth.

## القاعدة الذهبية / Golden rule

**لا تختلق أي رقم.** `prospects.json` و `deals.json` تبدأ فارغة عمدًا. لا يكتب فيها إلا
المؤسس ببيانات حقيقية، تمامًا مثل قاعدة AGENTS.md: *"never invent CRM numbers in automation."*

**Never fabricate data.** `prospects.json` and `deals.json` ship empty on purpose.
Only the founder fills them with real figures — mirroring the AGENTS.md rule
*"never invent CRM numbers in automation."*

## الملفات / Files

| Ledger | Purpose | Source of truth it complements |
| --- | --- | --- |
| `prospects.json` | خط أنابيب الفرص (شركة/قطاع/مرحلة/الخطوة القادمة) | CRM + `auto_client_acquisition/` revenue memory event store |
| `deals.json` | الصفقات وقيمها بالريال (يكتبها المؤسس فقط) | CRM / HubSpot |
| `experiments.json` | حلقة التعلّم: فرضية واحدة + مقياس واحد لكل تجربة | `GET /api/v1/revenue-os/learning/weekly-template` |
| `risks.json` | سجل المخاطر (تجاري/منتج/أمن/امتثال/تشغيل) | `SECURITY.md`, `docs/SECURITY_RUNBOOK.md` |

كل سجل بياناته في `*.json`، وعقده (schema) في `*.schema.json` (JSON Schema draft 2020-12).

## الحماية / How it is guarded

- **Structural validator (no deps):** `python scripts/check_ledgers.py` → يطبع `DEALIX_LEDGERS_VERDICT=PASS|FAIL`.
- **CI guard:** `tests/test_ledgers_schema.py` يُجمَع تلقائيًا في بوابة `pytest --cov` الحالية — أي انحراف (JSON مكسور، حقل ناقص، enum غير صالح، id مكرر) يصبّغ CI أحمر. **بدون تعديل أي workflow.**

> الهوية خفيفة عمدًا (PDPL): سجّل **دور** جهة الاتصال (مثل "مدير تسويق") لا الأسماء/الجوالات/الإيميلات الشخصية — تلك تبقى في الـ CRM.
> Identity-light by design (PDPL): store the contact **role**, not personal names/phones/emails — those stay in the CRM.

## إضافة سطر / Add a row

1. انسخ بنية سجل من `*.schema.json` (راجع `$defs`).
2. استخدم مُعرّفًا بالنمط `PRO-0001` / `DEAL-0001` / `EXP-0001` / `RISK-0001`.
3. شغّل `python scripts/check_ledgers.py` قبل الـ commit.

See also: [`docs/FOUNDER_OS_INDEX.md`](../docs/FOUNDER_OS_INDEX.md) ·
[`docs/CLOUD_CODE_COMMAND_CENTER.md`](../docs/CLOUD_CODE_COMMAND_CENTER.md)
