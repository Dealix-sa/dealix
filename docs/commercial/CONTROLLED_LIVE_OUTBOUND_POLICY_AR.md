# سياسة الإرسال المباشر المُتحكَّم به (Controlled Live Outbound Policy)

> **هذا الإصدار لا يُفعّل الإرسال المباشر.** الواجهة مُصمَّمة للمستقبل، والوضع
> الافتراضي مغلق بالكامل (fail-closed).

## البوابات المطلوبة لأي إرسال حي

يجب أن تتحقق **كل** الشروط التالية مجتمعةً:

1. العلم العام مُفعّل: `EXTERNAL_SEND_ENABLED=true`.
2. الوضع: `OUTBOUND_MODE=controlled_live`.
3. علم القناة مُفعّل (`EMAIL_SEND_ENABLED` / `WHATSAPP_SEND_ENABLED` + `WHATSAPP_ALLOW_LIVE_SEND`).
4. القناة مسموحة تعاقدياً للعميل (`client_rules.allowed_channels`).
5. الحساب `verified` ولديه `source_url`.
6. العميل قابل للتواصل ولم يُلغِ الاشتراك.
7. واتساب: يوجد opt-in (التواصل البارد ممنوع منعاً باتاً).
8. البريد: يحتوي على إلغاء اشتراك (unsubscribe).
9. `message.status=approved` و`owner_decision=send` أو `book`.
10. اجتياز حدود المعدّل (rate limits).
11. اجتياز حارس الادعاءات (لا "مضمون"، لا ROI مضمون...).
12. كتابة سجل تدقيق (audit log).

أي إخفاق ⇒ **مسودة + سبب، دون إرسال.**

## الواجهة البرمجية

```python
from app.commercial.safety import (
    can_send_email, can_send_whatsapp,
    can_write_calendar, can_finalize_proposal,
)

decision = can_send_email(action, account, client_rules)
# SafetyDecision(allowed, reason, required_approvals, blocked_by, audit_level)
```

كل دالة ترجع `SafetyDecision`، والافتراضي دائماً **مرفوض** للإرسال الحي ما لم
تتحقق الأعلام والموافقات معاً.

## حارس الادعاءات (Claim Guard)

عبارات محظورة (أمثلة): `guarantee`, `risk-free`, `100%`, `نضمن`, `مضمون`،
`double your revenue`, `we promise`. أي رسالة تحتوي إحداها تُحجب عن الإرسال.
