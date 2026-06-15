# دليل غرفة القيادة (Command Room)

## الغرض

غرفة القيادة هي لوحة تحكم offline تُبنى يوميًا من ledgers/ وتعرض:

- عدد الفرص والجاهزين للتواصل
- مسودات اليوم والإيميلات المرسلة يدويًا
- الردود والاجتماعات والعروض
- الصفقات المربحة/الخاسرة
- توقع الإيرادات
- توزيع القطاعات وأنماط الألم
- الإجراءات التالية والحواجز

## ملفات المصدر

- `ledgers/prospects.csv` — الفرص
- `ledgers/deals_pipeline.csv` — الأنابيب
- `ledgers/reply_log.csv` — الردود
- `ledgers/outreach_log.csv` — الإيميلات المرسلة
- `outbox/YYYY-MM-DD/` — المسودات المولدة

## التشغيل

```bash
make command-room
```

الناتج: `reports/command_room/index.html`

افتح الملف في المتصفح محليًا. لا يحتاج سيرفر.

## الدلالي اليومي

1. صباحًا: شغّل `make company-day`.
2. افتح `reports/command_room/index.html`.
3. راجع العدد الجاهز للتواصل.
4. راجع المسودات في `outbox/YYYY-MM-DD/`.
5. بعد الإرسال اليدوي: سجّل في `ledgers/outreach_log.csv`.
6. مساءً: حدّث `ledgers/deals_pipeline.csv` و`reply_log.csv`.
