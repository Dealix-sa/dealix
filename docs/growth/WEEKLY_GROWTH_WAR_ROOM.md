# Weekly Growth War Room — Dealix

## الدور — Role

غرفة قرار أسبوعية تجيب على ثلاثة أسئلة فقط: **ماذا نضاعف؟ ماذا نصلح؟ ماذا نقتل؟**

## المخرج — Output

```
<private_ops>/founder/weekly_growth_review.md
```

## الأقسام — Sections

1. **What moved** — ما الذي تحرك أسبوعياً (paid, meetings, samples).
2. **What stalled** — ما الذي توقف رغم النشاط.
3. **Best sector** — قطاع أفضل تقدم.
4. **Worst sector** — قطاع لم يُحرز أي تقدم.
5. **Best channel** — قناة جلبت أعلى تحويل.
6. **Best message** — رسالة لقيت أعلى reply rate.
7. **Objections** — الاعتراضات الـ 3 الأشيع.
8. **Experiments** — تجارب اكتملت دورتها وقابلة للقرار.
9. **Kill / Fix / Scale** — قرارات الأسبوع.
10. **Next week operating targets** — هدف واحد قابل للقياس.

## القواعد — Rules

- لا قرار Scale بدون 2 weeks of evidence على الأقل.
- لا قرار Kill بدون hypothesis مكتوبة سابقًا في `learning/`.
- كل قرار يُسجَّل في `<private_ops>/learning/decisions.csv`.
- الجلسة لا تتجاوز 60 دقيقة.

## التوليد — Generation

```bash
make weekly-growth-review PRIVATE_OPS=/opt/dealix-ops-private
```

- Script: `scripts/generate_weekly_growth_review.py`.

## الملكية — Ownership

- Owner: Founder.
- Backup: Sales lead.
- Cadence: كل اثنين 09:00.
