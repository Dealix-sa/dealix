# Kill / Fix / Scale Decision System — Dealix

## الدور — Role

إطار قرار صريح لكل حملة / قناة / رسالة / قطاع.

## المعايير — Criteria

### Scale

- ≥ 1 paid customer من نفس المسار في ≤ 30 يوم.
- ≥ 20% reply rate على رسائل معتمدة.
- Trust risks تحت السيطرة (no high open).
- قابلية تكرار واضحة (sample + proposal + payment).

### Fix

- إشارة موجبة لكن لم تكتمل دورة الكاش.
- Reply rate موجب لكن objections متكررة → تعديل offer/message.
- Trust risk قابل للحل في ≤ أسبوع.

### Kill

- صفر كاش بعد 2 أسابيع نشاط حقيقي.
- ≥3 رفض متتالٍ لنفس الـ proposal.
- اعتراض غير قابل للحل (regulatory / fit).
- Trust risk عالٍ غير قابل للسيطرة.

## النموذج — Decision row

| Field | Value |
| --- | --- |
| `decision_id` | KFS-YYYYMMDD-<n> |
| `subject` | campaign / channel / message / sector |
| `decision` | scale / fix / kill |
| `evidence` | refs إلى `learning/*.csv` |
| `owner` | founder |
| `effective_from` | YYYY-MM-DD |
| `review_in_days` | 14 |

تُكتب في `<private_ops>/learning/decisions.csv`.

## القواعد — Rules

- لا قرار Scale بدون paid customer (لا "Scale بناءً على impressions").
- Kill لا يُلغى في نفس الأسبوع — على الأقل أسبوع cool-off.
- Fix له deadline واضح — إن فشل، تتحول لـ Kill.

## الملكية — Ownership

- Owner: Founder.
- Auditor: Sales lead.
