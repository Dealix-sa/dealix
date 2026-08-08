# Controlled Live Activation Runbook — دليل تفعيل الإرسال المباشر

> **الحالة**: جاهز للتفعيل | **التاريخ**: 2026-08-08
>
> هذا المستند يوثق خطوات تفعيل الإرسال المباشر المحكوم في بيئة Railway.
> التفعيل يتم على مرحلتين: البريد الإلكتروني أولاً، ثم واتساب بعد التحقق.

## المتطلبات الأساسية

قبل التفعيل، تأكد من:

- [x] CI أخضر على main
- [x] Docker build ناجح
- [x] نظام Company Intelligence يعمل (8 محركات)
- [x] Policy gate مُطبّق (`app/outbound/policy_gate.py`)
- [x] بوابات الأمان: suppression list, consent, rate limiting
- [x] الادعاءات المحظورة: guaranteed ROI, مضمون, testimonials
- [x] Unsubscribe wording enforced
- [x] Contact verification required
- [x] Message approval required
- [ ] Railway billing paid and service connected
- [ ] PostgreSQL database attached
- [ ] `/healthz` returns 200

## المرحلة 1 — تفعيل البريد الإلكتروني

### متغيرات Railway المطلوبة

```env
# Master switches
EXTERNAL_SEND_ENABLED=true
OUTBOUND_MODE=controlled_live

# Email channel
EMAIL_SEND_ENABLED=true

# Keep other channels disabled initially
WHATSAPP_SEND_ENABLED=false
WHATSAPP_ALLOW_LIVE_SEND=false
SMS_SEND_ENABLED=false

# Safety gates (must remain true)
OUTBOUND_REQUIRE_APPROVAL=true
OUTBOUND_REQUIRE_VERIFIED_TARGET=true
OUTBOUND_REQUIRE_SOURCE_URL=true
OUTBOUND_REQUIRE_OPT_OUT=true
OUTBOUND_BLOCK_FAKE_CLAIMS=true
OUTBOUND_BLOCK_GUARANTEED_ROI=true
```

### التحقق بعد التفعيل

```bash
# 1. Health check
curl -fsS https://api.dealix.me/healthz

# 2. Safety status — يجب أن يظهر email_send_enabled=true
curl -fsS https://api.dealix.me/api/status | python3 -m json.tool

# المتوقع:
# {
#   "external_send_enabled": true,
#   "outbound_mode": "controlled_live",
#   "email_send_enabled": true,
#   "whatsapp_send_enabled": false,
#   "sms_send_enabled": false,
#   "safe_to_send": false  ← يبقى false لأن كل رسالة تحتاج approval
# }
```

### بوابات الحماية التي تبقى فعالة

حتى مع `EXTERNAL_SEND_ENABLED=true`، كل رسالة يجب أن تمر عبر:

1. **`message.status = approved`** — المؤسس يوافق على كل رسالة
2. **`contact.verification_status = approved_to_send`** — جهة الاتصال مُتحقق منها
3. **`contact.email_opt_out ≠ true`** — لم يطلب الإيقاف
4. **`source_url` موجود** — مصدر البيانات مُوثّق
5. **Unsubscribe wording** — نص إلغاء الاشتراك موجود
6. **No blocked claims** — لا ادعاءات محظورة
7. **Consent recorded** — الموافقة مُسجّلة
8. **Rate limits** — حدود الإرسال مُحترمة
9. **Suppression list** — قائمة الحظر مُفعّلة

## المرحلة 2 — تفعيل واتساب (بعد نجاح البريد)

### متغيرات إضافية

```env
WHATSAPP_SEND_ENABLED=true
WHATSAPP_ALLOW_LIVE_SEND=true
WHATSAPP_SEND_MODE=template_only

# WhatsApp Cloud API credentials
WHATSAPP_PHONE_NUMBER_ID=<from Meta Business>
WHATSAPP_ACCESS_TOKEN=<from Meta Business>
WHATSAPP_APP_SECRET=<from Meta Business>
```

### بوابات واتساب الإضافية

1. **`WHATSAPP_SEND_MODE = template_only`** — فقط قوالب مُعتمدة من Meta
2. **`contact.whatsapp_opt_in = true`** — موافقة صريحة مطلوبة
3. **`contact.whatsapp_opt_out ≠ true`** — لم يطلب الإيقاف
4. **`message.template_name` موجود** — اسم القالب مطلوب
5. **STOP / إيقاف / إلغاء** — يُحترم فوراً

## المرحلة 3 — SMS (اختياري)

```env
SMS_SEND_ENABLED=true
```

## إيقاف الطوارئ

في أي وقت، يمكن إيقاف الإرسال فوراً:

```env
EXTERNAL_SEND_ENABLED=false
# أو
OUTBOUND_MODE=draft_only
```

أو تحديداً لقناة واحدة:

```env
EMAIL_SEND_ENABLED=false
WHATSAPP_SEND_ENABLED=false
SMS_SEND_ENABLED=false
```

## ما لا يتغير أبداً

- ❌ لا إرسال جماعي بدون موافقة
- ❌ لا واتساب بدون opt-in صريح
- ❌ لا ادعاءات مضمونة
- ❌ لا بيانات مزيفة أو شهادات وهمية
- ❌ لا إرسال بدون مصدر بيانات مُوثّق
- ❌ لا تجاوز لقوائم الحظر
