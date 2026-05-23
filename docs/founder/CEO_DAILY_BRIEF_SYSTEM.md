# CEO Daily Brief System — Dealix

## الدور — Role

تقرير يومي يكتبه النظام للمؤسس قبل بدء العمل. الهدف: تحويل آلاف الأحداث إلى **قرار واحد لليوم**.

## المخرج — Output

ملف Markdown ثنائي اللغة:

```
<private_ops>/founder/ceo_daily_brief.md
```

## الأقسام — Sections

1. **Top CEO Action** — الـ action رقم 1 لليوم.
2. **Revenue Bottleneck** — أين توقف الكاش؟
3. **Trust Risks** — مخاطر ثقة مفتوحة بحاجة قرار.
4. **Worker Failures** — أي agents/workers فشلت في آخر 24 ساعة.
5. **Launch Blockers** — blockers من `<private_ops>/launch/blockers.csv`.
6. **Payment Follow-Ups** — فواتير معلقة + اقتراح follow-up.
7. **Approved Work Ready** — عناصر اعتُمدت ولم تُنشر بعد.
8. **Decisions Needed** — قرارات بحاجة المؤسس فقط.
9. **What To Ignore Today** — قائمة "لا تفعل" حتى لا يتشتت.

## القواعد — Rules

- يُولَّد فقط من بيانات حقيقية تحت `<private_ops>/`.
- لا يحتوي وعد دخل أو ضمان نتيجة.
- لا يكشف أي secret.
- إذا لم تُمرَّر `PRIVATE_OPS` يطبع تحذير + ينتج template فارغ.
- اللغة: عربي رئيسي + ملخص إنجليزي قصير.

## التوليد — Generation

```bash
make ceo-daily-brief PRIVATE_OPS=/opt/dealix-ops-private
```

النظام الفعلي:
- `scripts/generate_ceo_daily_brief.py`

## الملكية — Ownership

- Owner: Founder.
- Backup: Sales lead.
- Cadence: يومي قبل 09:00.
