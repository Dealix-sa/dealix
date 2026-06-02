# Dealix Draft Quality Policy — سياسة بوابة الجودة

`dealix/distribution/quality.py` · CLI: `scripts/check_draft_quality.py` ·
Make: `make draft-quality` (تفشل بـ exit code 1 إن وُجد خلل).

## فحوص حاسمة (خطأ → المسودة تفشل البوابة)
- لا عبارة ادعاء/مبالغة ممنوعة (نضمن / مضمون / إرسال جماعي …).
- `policy == draft_only_no_auto_send`.
- `status` ضمن الحالات المعروفة.
- `evidence_level` عدد صحيح صالح 0–5.
- وجود CTA واحد واضح (سطر `CTA:` أو سؤال `؟`).
- وجود نص عربي ضمن حدود طول معقولة (60–2000 حرف).
- اجتياز مخطط `schemas/draft.schema.json`.

## تنبيهات (تظهر، لا تُفشِل)
- أكثر من 3 أسئلة (`؟`) — كثرة طلبات.
- وجود رابط خام (الروابط يضيفها المؤسس عند الإرسال اليدوي).

## المخرجات
- تقرير `reports/distribution/DRAFT_QUALITY_GATE.md`.
- اختياريًا تُكتب نتيجة الجودة داخل كل draft (`persist`).
- `distribution-day` يجعل الـ verdict = FAIL إذا فشلت أي مسودة.

## التحقق
```python
from dealix.distribution.quality import check_draft
res = check_draft(some_draft)
res["passed"], res["errors"]
```
