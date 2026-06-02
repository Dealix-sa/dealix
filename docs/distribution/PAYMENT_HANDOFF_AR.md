# Dealix Payment Handoff — تسليم الدفع

`dealix/distribution/payments.py` · CLI: `scripts/generate_payment_handoff.py` ·
Make: `make payment-handoffs`

> القاعدة الحاسمة: **النظام لا يُنشئ ولا يرسل رابط دفع ولا يسحب بطاقة.** ينتج
> *مسودة تعليمات* للمؤسس ليُصدر رابط Moyasar أو فاتورة يدوية بنفسه.

## المنطق
- يُنشئ handoff فقط من **عروض معتمدة** (`status == approved`) — dedupe لكل عرض.
- المبلغ يُشتق من العرض في الكتالوج (`price_sar.typical` أو `min`).
- يبدأ `draft_pending_approval` مع `approval_required = true`.

## البنية
يطابق `schemas/payment_handoff.schema.json`:
```
id, proposal_id, company, amount_sar, currency="SAR",
payment_provider ∈ {moyasar, manual_invoice},
approval_required=true, status, notes, created_at
```

## التكامل مع Moyasar
روابط الدفع تُدار في `dealix/payments/` (sandbox افتراضيًا؛ الوضع الحي يتطلب ضبط
متغيّر البيئة الحي + المفتاح الحي يدويًا). هذه الطبقة **لا** تلمس مفاتيح الدفع ولا
تُنشئ روابط — تكتفي بمسودة المبلغ والمزوّد المقترح.

## الموافقة
```python
from dealix.distribution.payments import approve_handoff
approve_handoff(handoff_id)   # ثم يُصدر المؤسس الرابط/الفاتورة يدويًا
```
