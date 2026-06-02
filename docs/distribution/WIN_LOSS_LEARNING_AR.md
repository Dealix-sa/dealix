# Dealix Win/Loss Learning — تعلّم الربح والخسارة

`dealix/distribution/win_loss.py` · CLI: `scripts/win_loss_learning.py` ·
Make: `make win-loss`

> كل خسارة لازم تعلّم النظام. الملخّصات **عدّ خالص** لما سُجِّل — لا بيانات مخترعة.

## التسجيل
```bash
python scripts/win_loss_learning.py --record \
  --company "Acme" --outcome lost --reason price \
  --sector clinics --channel email --lesson "ابدأ بـ Diagnostic أصغر"
```
`outcome ∈ {won, lost, no_response, nurture}`. يطابق `schemas/win_loss.schema.json`.

## الملخّص الأسبوعي
- توزيع النتائج (won/lost/no_response/nurture).
- حسب القطاع والقناة وأهم الأسباب.
- `win_rate_pct` و`lessons`.
- **next_changes** مقترحة آليًا من أنماط الأسباب:
  - سعر متكرر → قدّم Diagnostic أصغر كنقطة دخول.
  - ضعف ثقة → ابدأ بـ Proof Pack ومرجع.
  - توقيت → nurture بدل الإغلاق المبكر.
  - لا ألم واضح → أعد تأهيل القطاع/الحساب.

## المخرجات
- `reports/distribution/WIN_LOSS_LEARNING.md`.
- يدخل ضمن `distribution-metrics` و`distribution-weekly`.
