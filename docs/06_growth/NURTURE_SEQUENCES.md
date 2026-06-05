# Nurture Sequences — Dealix Self-Growth OS

كل lead يدخل لازم يأخذ تسلسل تربية. التسلسلات **drafts** فقط — **لا رسالة
تُرسل تلقائيًا**، ولا cold WhatsApp، ولا LinkedIn automation. كل رسالة لها
**CTA واحد**.

> المصدر الحي: [`data/growth/nurture_sequences.json`](../../data/growth/nurture_sequences.json).
> التوليد: `python3 scripts/growth/generate_nurture_sequence.py`
> → [`reports/growth/NURTURE_SEQUENCES.md`](../../reports/growth/NURTURE_SEQUENCES.md).

---

## Sequence 7 أيام (للجاهزين — score < 70)

| اليوم | الموضوع | CTA |
|---:|---|---|
| 0 | النتيجة + الـ Score | اطّلع على نتيجتك الكاملة |
| 1 | أكبر نقطة تسرب | افهم كيف نعالجها |
| 2 | Sample Command Pack | شاهد نموذج Command Pack |
| 3 | عندكم CRM؟ لماذا لا يكفي | ابدأ تشخيص Dealix |
| 4 | قصة case-safe | ابدأ تشخيص Dealix |
| 5 | دعوة تشخيص | احجز التشخيص |
| 7 | تذكير أخير (3 sprints فقط) | ابدأ Command Sprint |

## Sequence 30 يوم (غير الجاهزين — score 40–69)

| اليوم | الموضوع | CTA |
|---:|---|---|
| 0 | النتيجة + أين تبدأ | اطّلع على نتيجتك |
| 7 | insight الأسبوع: operating rhythm | اقرأ المقال |
| 10 | قالب Next Action Board | حمّل القالب |
| 14 | دعوة لينة | احجز التشخيص |
| 21 | تقرير قطاعي | اقرأ التقرير |
| 28 | مثال case-safe + دعوة | احجز التشخيص |

---

## التوجيه حسب الـ Score

```
Score ≥ 70 → Diagnostic booking مباشر
Score 40–69 → nurture 30 يوم → diagnostic later
Score < 40 → nurture 7 أيام (تثبيت الألم) → diagnostic
```

---

## الحوكمة

- كل رسالة تمرّ على **موافقة المؤسس قبل الإرسال** (non-negotiable #8).
- لا cold WhatsApp (#2)، لا LinkedIn automation (#3).
- لا لغة إيراد مضمون (#5)، لا fake proof (#4).
- القيمة التقديرية ليست قيمة مُتحقَّقة / *Estimated value is not Verified value*.
- كل رسالة = **CTA واحد**.

---

## كيف نضيف/نعدّل تسلسلًا

عدّل `data/growth/nurture_sequences.json` (slug, name_ar, trigger, audience,
channel, messages[day/subject_ar/intent/cta]) ثم شغّل المولّد للتحقق.
