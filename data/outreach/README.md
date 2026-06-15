# Dealix Outreach Kit — محرّك الاستهداف اليومي

نظام يجهّز لك إيميلات إقناع جاهزة لشركات سعودية حقيقية — **أنت تراجع وترسل**. لا شيء يُرسل تلقائيًا (سياسة المراجعة البشرية، محمية باختبار `tests/test_no_auto_send.py`).

## الملفات
| الملف | الدور |
|------|------|
| `sector_pitches.json` | نصوص الإقناع لكل قطاع سعودي (ألم → حل Dealix → دعوة)، ثنائية اللغة |
| `saudi_target_intake.template.csv` | قالب تملأه بشركاتك الحقيقية |
| `saudi_target_intake.csv` | ملفك الحقيقي (تنشئه أنت — gitignored، لا يُرفع) |

## كيف تشغّله (3 خطوات)
```bash
# 1) انسخ القالب
cp data/outreach/saudi_target_intake.template.csv data/outreach/saudi_target_intake.csv

# 2) عدّل الملف وحط شركات حقيقية (الاسم، القطاع، إيميل مؤكد، سبب الاستهداف)

# 3) ولّد الإيميلات الجاهزة
make outreach          # أو: python3 scripts/dealix_outreach_kit.py
```
الناتج في `reports/outreach/<التاريخ>/` — إيميل جاهز لكل شركة + `_DIGEST.md` للمراجعة.

## القطاعات المدعومة
`real_estate` · `clinic` · `logistics` · `training` · `marketing_agency` · `b2b_services`

## قواعد لا تُكسر
- **لا تخترع إيميلات.** ضع فقط عناوين مؤكدة لشركات تعرفها أو بحثت عنها.
- الألم يُكتب كـ **فرضية/سؤال**، لا كحقيقة مؤكدة عن الشركة.
- بدون ادعاءات أرقام عائد، بدون شهادات وهمية، بدون ضغط.
- الإرسال **يدوي منك** دائمًا.
