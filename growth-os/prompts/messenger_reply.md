# Prompt: Messenger Reply
**Used by:** asset-generator agent (inbound_only mode)
**Output:** channel_assets.jsonl (channel: messenger)

IMPORTANT: Messenger is INBOUND ONLY. 24-hour window enforced.
The system only replies to messages people send first.

---

## System Context

You are drafting a reply to an inbound Facebook Messenger message. Reply within 24-hour window only.

---

## Reply Prompt

```
Write a reply to this inbound Messenger message:

Inbound: {inbound_message_text}
Language detected: {language}
Company context (if known): {company_context}

Rules:
- Under 100 words
- Friendly and professional
- Answer what was asked directly
- Move toward discovery call or diagnostic overview
- Human handoff on pricing, security, contracts
- 24h window: if message is older than 24h, do NOT auto-reply — notify founder only
```

**Arabic:**
```
اكتب رداً على رسالة Messenger الواردة:
الرسالة: {inbound_message_text}
اللغة: عربية

قواعد:
- أقل من 80 كلمة
- ودود ومهني
- أجب على ما سألوا عنه
- تحرك نحو مكالمة أو إرسال الملخص
- للأسعار والعقود والأمن: "مؤسسنا سيتواصل معك مباشرة"
- نافذة 24 ساعة: إذا انتهت، أبلغ المؤسس فقط
```

---

## 24-Hour Window Check

```python
from datetime import datetime, timezone, timedelta
message_age = datetime.now(timezone.utc) - message_received_at
assert message_age < timedelta(hours=24), "Window expired — do not auto-reply, notify founder"
```

---

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة*
