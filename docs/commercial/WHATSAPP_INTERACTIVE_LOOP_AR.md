# حلقة واتساب التفاعلية (WhatsApp Interactive Loop)

حلقة محادثة واتساب بأزرار رد تفاعلية (≤3 أزرار، العنوان ≤20 حرفاً)، تبني
الحمولات الدقيقة، تحلّل أحداث الـ webhook، وتدفع المحادثة خطوة بخطوة — **بدون
أي إرسال HTTP**.

## بناء حمولة الأزرار

```python
from app.commercial.whatsapp_loop import build_interactive_payload
body = build_interactive_payload("النص", buttons)   # شكل WhatsApp interactive/button
```

يفرض الحد الأقصى 3 أزرار وطول العنوان ≤20 حرفاً تلقائياً.

## تحليل الـ Webhook

`parse_webhook(event)` يقبل الشكل المبسّط أو شكل Cloud API المتداخل، ويُخرج:
`{from, text, button_id, button_intent}`. ضغط الزر يُربط بنية المحادثة عبر
بيانات الأزرار في آخر دور صادر.

## الحلقة

```python
from app.commercial import whatsapp_loop as wl
conv, opener = wl.start(account)                 # افتتاحية بأزرار (مسودة)
nxt = wl.step(conv, webhook_event, account=account)  # خطوة واحدة لكل حدث وارد
```

## الإرسال المُبوَّب (مستقبلي)

`GatedWhatsAppSender` يمثّل واجهة الإرسال الحي المستقبلية. في هذا الإصدار:
- `transmitted=False` دائماً (لا يوجد ناقل HTTP موصول).
- يرفض ما لم تجتَز كل بوابات الأمان (تتطلب opt-in؛ التواصل البارد ممنوع).

> الهدف: تجربة محادثة حيّة حقيقية (افتتاح → أزرار → حجز → تفاوض → رد)، مع بقاء
> كل شيء مسودة حتى الموافقة وتفعيل البوابات.
