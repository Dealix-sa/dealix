# Digital Sales Room — غرفة عميل Dealix

**البديل المجاني في المستودع:** مجلد منظم + [`hub.html`](hub.html) محلي (بدون منصة SaaS خارجية).

**البديل المدفوع لاحقاً:** Dock / GetAccept / Trumpet — نفس هيكل [`INDEX.yaml`](INDEX.yaml).

## متى تُنشئ غرفة

بعد **أول اجتماع مؤهل** (Discovery أو Demo) — لا قبل جمع الحاجة.

## هيكل المجلد لكل عميل

```
docs/marketing-system/digital-sales-room/clients/{slug}/
  INDEX.yaml          # نسخة من القالب + تعبئة
  live-deck.pdf       # من live-deck-b2b-ar
  leave-behind.pdf
  appendix-technical.pdf
  roi-link.html       # نسخة أو رابط لحاسبة ROI
  MAP.md              # من MAP_TEMPLATE
  recording-notes.md  # ملخص الاجتماع (داخلي)
```

## قواعد الحوكمة

- لا تضع credentials أو بيانات شخصية خام في Git
- استخدم `{slug}` مجهّل (مثلاً `acme-2026-05`) — لا أسماء كاملة في المستودع العام
- كل outreach في الغرفة = **مسودات** فقط

## MAP

بعد كل اجتماع: حدّث [`MAP_TEMPLATE.md`](MAP_TEMPLATE.md) وشارك رابط `hub.html?client=slug` محلياً أو PDF.

## فهرس الأصول العامة

انظر [`INDEX.yaml`](INDEX.yaml) للقائمة المعيارية.
