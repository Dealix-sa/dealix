# محرّك المحادثة (Conversation Engine)

محرّك متعدد الأدوار بآلة حالة (state machine) يدير محادثة واحدة عبر أي قناة،
ويعتمد على العقل التجاري لاختيار الخطوة التالية. لا يرسل شيئاً.

## المراحل (Stages)

```
opener → qualifying → value → objection → negotiation → booking → proposal
       → closing → won / lost / nurture / opted_out
```

- الدخول إلى `won` / `lost` / `proposal` **مقيّد بموافقة** — لا يُقلب تلقائياً.
- `opted_out` مرحلة نهائية: يتوقف كل تواصل فوراً.

## التدفق

```python
from app.commercial.conversation import start_conversation, handle_inbound

conv, opener_payload = start_conversation(account, motion="sales_prospecting", channel="whatsapp")
# المستخدم يضغط زراً أو يرد نصاً:
next_payload = handle_inbound(conv, "السعر غالي", account=account)   # → negotiation
```

- كل دور (turn) يُسجَّل: الاتجاه (inbound/outbound)، النية، المرحلة قبل/بعد،
  `is_draft=True` للمخرجات، و`reasoning` (سبب القرار).
- قناة واتساب تُرفق أزراراً تفاعلية (≤3) حسب المرحلة؛ الإيميل بلا أزرار.

## السلامة

- كل حمولة (`OutboundPayload`) تحمل `requires_approval=True` و`SafetyDecision`.
- `send_status` يبقى `draft` أو `blocked` افتراضياً.
- حارس الادعاءات يمنع أي عبارة "مضمونة" في النص.
