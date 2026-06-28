# نظام Dealix التجاري للنمو — الإصدار الثاني (Commercial Growth OS v2)

## ما هو؟

نظام تشغيل تجاري متصل — وليس مجرد روبوت محادثة ولا ملاحظات CRM ولا مسودات
واتساب فقط. النظام يخطّط، يجمع العملاء المحتملين من مصادر مسموحة، يؤهّل
الحسابات، يجهّز الرسائل، يقترح الردود والتفاوض ضمن حدود معتمدة، ينشئ خيارات
حجز، يجهّز ملخصات العروض، يتابع، يحدّث خط الأنابيب (Pipeline)، يسلّم للتنفيذ،
ويُنتج تقرير غرفة قيادة (Command Room) كدليل.

> **القاعدة الذهبية:** الوضع الافتراضي آمن. لا إرسال خارجي، لا كتابة تقويم، لا
> تسعير نهائي بدون موافقة بشرية صريحة.

## التدفق الأساسي

```
عميل محتمل / حساب
  → التحقق من المصدر (source_url إلزامي)
  → تقييم المطابقة ICP
  → تأهيل / استبعاد
  → بطاقة نمو (Growth Card)
  → التوصية بالقناة
  → مسودة تواصل
  → مكتب الرد الذكي / التفاوض
  → مكتب الحجز
  → مصنع العروض (Proposal Factory)
  → محرك المتابعة
  → تحديث خط الأنابيب
  → تسليم التنفيذ
  → حزمة الإثبات (Proof Pack)
  → التجديد / البيع الإضافي
```

## الحركات التجارية المدعومة (10)

1. التنقيب عن المبيعات (Sales prospecting)
2. تواصل الشراكات (Partnership outreach)
3. دفع العروض (Proposal push)
4. إحياء العملاء القدامى (Revival)
5. البيع الإضافي (Upsell)
6. الاحتفاظ (Retention)
7. الإحالة (Referral)
8. التجديد (Renewal)
9. توسعة نجاح العميل (Customer success expansion)
10. مراقبة السوق/الحساب (Market/account watch)

## الوحدات البرمجية

| الوحدة | الغرض |
|--------|-------|
| `app/commercial/schemas.py` | نماذج البيانات المُوثّقة |
| `app/commercial/safety.py` | عقيدة الأمان والبوابات (fail-closed) |
| `app/commercial/icp_scoring.py` | تقييم المطابقة |
| `app/commercial/lead_sourcing.py` | جمع وتحقق العملاء المحتملين |
| `app/commercial/growth_cards.py` | بناء بطاقات النمو |
| `app/commercial/reply_classifier.py` | تصنيف الردود |
| `app/commercial/negotiation_desk.py` | مسودات التفاوض ضمن الحدود |
| `app/commercial/booking_desk.py` | خيارات الحجز (بدون كتابة تقويم) |
| `app/commercial/proposal_factory.py` | ملخصات العروض (بموافقة) |
| `app/commercial/followup_engine.py` | مهام المتابعة D1/D3/D7 |
| `app/commercial/pipeline.py` | آلة حالة خط الأنابيب |
| `app/commercial/delivery_handoff.py` | تسليم التنفيذ |
| `app/commercial/proof_pack.py` | حزمة الإثبات |
| `app/commercial/command_snapshot.py` | لقطة غرفة القيادة |
| `app/commercial/orchestrator.py` | المنسّق الكامل |

## التشغيل

```bash
python scripts/commercial/run_commercial_growth_os.py    # أو: make commercial-growth-os
python scripts/commercial/verify_commercial_growth_os.py # أو: make commercial-growth-verify
```

المخرجات:

- `reports/commercial/growth_os/latest.json`
- `reports/commercial/growth_os/latest.md`

## ما لا يفعله النظام أبداً

- لا يرسل واتساب/بريد/رسائل بدون موافقة.
- لا يكتب في التقويم افتراضياً.
- لا يحدّد سعراً نهائياً ولا يمنح خصماً ولا يقبل شروطاً قانونية.
- لا يخترع عملاء أو شهادات أو نتائج (ROI) أو دراسات حالة.
- لا يَعِد بنتائج مضمونة.
- لا يجمع من مصادر محظورة.
