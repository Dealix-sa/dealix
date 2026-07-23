# Dealix Commercial Channel Control Plane

## الهدف

هذه الطبقة تحول Commercial Growth OS من ذكاء وتحليل إلى Action Queue قابل للتنفيذ المنضبط.

النظام يجهز:

- WhatsApp interactive payloads بأزرار.
- Email drafts مع opt-out.
- LinkedIn manual tasks بدون auto-DM.
- Phone call tasks.
- Website form tasks.
- Partner referral drafts.
- Human approval cards.
- Audit events.

## القاعدة

لا يوجد live send افتراضيًا. كل شيء يبدأ كـ draft أو manual task أو approval card.

## Human-in-loop

كل action له بطاقة موافقة:

- اعتماد
- تعديل
- تخطي

## القنوات

| القناة | الوضع |
|---|---|
| WhatsApp | payload تفاعلي، يحتاج opt-in |
| Email | draft فقط، يشمل opt-out |
| LinkedIn | manual-assisted فقط |
| Phone | call task |
| Website form | manual form task |
| Partner referral | شراكة draft |

## التشغيل

```bash
python scripts/commercial/run_channel_control_plane.py
python scripts/commercial/verify_channel_control_plane.py
python -m pytest -q tests/test_commercial_channel_control_plane.py
```

## المخرجات

```text
reports/commercial/channel_control/latest.json
reports/commercial/channel_control/latest.md
```
