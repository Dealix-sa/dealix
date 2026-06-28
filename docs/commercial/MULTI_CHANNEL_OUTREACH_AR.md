# التواصل متعدد القنوات (Multi-Channel Outreach)

عقل واحد يدير عدة قنوات. لكل قناة محوّل (adapter) يبني الحمولة الدقيقة ويرفق
قرار الأمان — **بدون أي إرسال شبكي**.

## القنوات والقواعد

| القناة | القاعدة |
|--------|---------|
| `whatsapp` | رسائل تفاعلية، ≤3 أزرار، opt-in إلزامي، التواصل البارد ممنوع |
| `email` | يجب أن يحوي إلغاء اشتراك (List-Unsubscribe + سطر STOP/إيقاف) |
| `linkedin_manual` | يدوي فقط — نُنتج نصاً للنسخ + مهمة للمشغّل؛ الأتمتة ممنوعة (A3) |
| `phone` | مهمة يدوية فقط (نقاط حديث) |

## الواجهة

```python
from app.commercial import channels
payload = channels.prepare_for_channel(
    "email", conversation_id="c1", account_id="a1",
    draft={"body_ar": "...", "body_en": "..."}, account=account,
)
# payload.safety = SafetyDecision.to_dict(); payload.send_status ∈ {draft, blocked, approved}
```

## مكتب الإيميل (Inbox)

`email_desk` يستوعب سلسلة بريد (thread)، يصنّف آخر رسالة واردة، ويصيغ رداً
بسلسلة (Re:) مع تذييل إلغاء اشتراك إلزامي. لا يتصل بصندوق بريد حي في هذا
الإصدار — يستوعب الرسائل المُزوّدة فقط، والإرسال يبقى مُبوَّباً.

## محرّك التفاعل الحيّ

`engagement_engine.run_engagement(...)` يختار القناة الأنسب لكل حساب، يفتح/يقدّم
المحادثة، يجهّز الحمولات، ويُنتج خطة إجراءات مرتّبة بالأولوية لغرفة القيادة
(`reports/commercial/engagement/latest.{json,md}`).

> كل المخرجات مسودات. `safe_to_send_now=false` افتراضياً على كل القنوات.
