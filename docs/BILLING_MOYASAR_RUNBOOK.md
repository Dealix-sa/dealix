# الفوترة — Moyasar (Dealix)

## مصدر الحقيقة

- `auto_client_acquisition/service_catalog/registry.py` يحفظ كتالوج العروض الداخلي.
- `api/routers/pricing.py` يفرض بوابات العرض العام وCheckout وMoyasar.
- قرار العرض والسعر الأول يتتبعه GitHub issue #917.

## الوضع الآمن الافتراضي

- `GET /api/v1/pricing/plans` يعيد قائمة فارغة وحالة `founder_approval_required`.
- `POST /api/v1/checkout` يعيد `503 checkout_not_founder_approved`.
- `pilot_1sar` ليس ضمن `ALLOWED_PLANS` ولا يمكن تشغيله في Production.
- لا مفتاح سري في المستودع، والمبالغ الداخلية بالهللة (SAR × 100).

## تفعيل سعر عام بعد اعتماد المؤسس فقط

يتطلب العاملان معًا:

- `DEALIX_PUBLIC_PRICING_ENABLED=true`
- `DEALIX_PUBLIC_PLAN_IDS=<canonical_id,...>`

أي معرف غير موجود أو `pilot_1sar` يُرفض تلقائيًا. يجب ألا تُضبط هذه القيم حتى تتطابق صفحة الهبوط والعرض والضريبة والفاتورة وCheckout ويُسجل قرار #917.

## تفعيل Checkout بعد اعتماد المؤسس فقط

- `DEALIX_CHECKOUT_ENABLED=true`
- يبقى المسار محميًا بـ `X-API-Key`.
- نفّذ اختبار Moyasar sandbox ثم الضريبة والفاتورة والاسترداد قبل أي دفعة حقيقية.

## اختبار 1 ريال

يحتاج في بيئة غير إنتاجية فقط:

- `DEALIX_CHECKOUT_ENABLED=true`
- `DEALIX_ENABLE_1SAR_CHECKOUT=true`
- `APP_ENV` لا يساوي `production`

حتى مع هذه القيم، يمنع الكود خطة 1 ريال إذا كانت البيئة Production.

## Webhook

- `POST /api/v1/webhooks/moyasar` يعتمد توقيع Moyasar ويستخدم idempotency.
- لا يُعتبر النظام جاهزًا للبيع لمجرد نجاح Webhook؛ قرار العرض، الخصوصية، ZATCA، والاسترداد بوابات مستقلة.
