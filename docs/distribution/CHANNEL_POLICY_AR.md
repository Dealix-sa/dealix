# Dealix Channel Policy — سياسة القنوات

القاعدة: **كل قناة لها مستوى أتمتة مسموح. الصياغة الآلية في
`data/distribution/channel_policy.yaml` ويُطابقها اختبار مع
`dealix/distribution/doctrine.py`.**

> الصياغة الأم لكل القنوات: التوليد (draft) مسموح دائمًا — الإرسال الخارجي يدوي
> بعد موافقة. لا أتمتة إرسال خارجي في أي قناة.

## Email
- **مسموح:** توليد draft · حفظ draft · إرسال يدوي بعد الموافقة.
- **ممنوع:** إرسال تلقائي بدون موافقة · دفعات جماعية · ادعاءات مضمونة.

## WhatsApp
- **مسموح:** توليد رسالة · نسخ/إرسال يدوي · تذكير للمؤسس.
- **ممنوع:** cold WhatsApp automation · إرسال جماعي · ربط agent يرسل بدون موافقة.

## LinkedIn
- **مسموح:** كتابة draft · نسخ/إرسال يدوي.
- **ممنوع:** LinkedIn automation · scraping · mass connect.

## Phone
- **مسموح:** call script · ملاحظات discovery · متابعة الاعتراضات.
- **ممنوع:** اتصال آلي بدون موافقة.

## Proposals / Payments
- **مسموح:** proposal draft · proof pack · مسودة تسليم دفع.
- **ممنوع:** التزام تعاقدي بدون موافقة · إنشاء/إرسال رابط دفع تلقائيًا.

## لماذا هذا مهم
عند ربط أتمتة خارجية (مثل n8n أو GitHub Actions) بصلاحيات إرسال مباشرة، قد تتحول
إلى سطح هجوم أو مصدر إزعاج. لذلك: استخدم الأتمتة كـ workflow حتمي بصلاحيات مضبوطة
(intake، تذكير، مزامنة) — وليست agent حرًّا يرسل نيابة عنك.

## التحقق
```python
from dealix.distribution.doctrine import channel_allows
channel_allows("email", "manual_send_after_approval")   # True
channel_allows("whatsapp", "cold_whatsapp_automation")  # False (deny يفوز)
```
