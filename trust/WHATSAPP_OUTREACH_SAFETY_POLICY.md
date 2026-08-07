# WhatsApp Outreach Safety Policy

قواعد السلامة للتواصل عبر واتساب

## الغرض

ضمان أن كل رسالة واتساب خارجية تلتزم بسياسة Meta للأعمال وسياسات
موافقة PDPL، مع منع الإرسال البارد وغير المصرّح به.

## القواعد الإلزامية

### 1. الموافقة المسبقة (Opt-in)

- **لا واتساب بارد**: لا إرسال واتساب لأي جهة دون موافقة موثّقة
  مسبقة (opt-in).
- سجل الموافقة يجب أن يحتوي: المعرّف، التوقيت، القناة، نص
  الموافقة، نسخة السياسة.
- سحب الموافقة يُفعّل قائمة الإيقاف فوراً.
- الاختبار: `tests/test_whatsapp_requires_opt_in.py`.

### 2. قوالب معتمدة من Meta

- كل رسالة واتساب تسويقية يجب أن تستخدم قالباً معتمداً من Meta
  (template readiness).
- لا رسائل نصية حرّة للأغراض التسويقية.
- راجع `docs/ops/WHATSAPP_META_VERIFICATION.md`.

### 3. لا إرسال جماعي بارد

- ممنوع: "cold whatsapp"، "bulk whatsapp"، "whatsapp blast"،
  "mass whatsapp".
- الاختبار: `tests/test_no_cold_whatsapp.py`،
  `tests/test_v7_no_cold_whatsapp.py`.

### 4. فحص قائمة الإيقاف

- قبل أي إرسال، يجب فحص قائمة الإيقاف.
- الاختبار: `tests/test_suppression_blocks_all_channels.py`.

### 5. سجل الموافقة (Consent Record)

- `safe_send_gateway.enforce_consent_or_block` يتطلب
  `consent_record_id` غير فارغ لقناة واتساب.
- بدون سجل موافقة، يُرفع استثناء `SendBlocked` برمز
  `no_consent_record`.

### 6. موافقة بشرية قبل الإرسال

- لا إرسال تلقائي. كل رسالة تبدأ كمسودة بحالة `draft`.
- الإرسال يتطلب `approval_status == "approved"`.

### 7. ساعات النشاط

- لا إرسال خارج ساعات النشاط السعودية (21:00-08:00).

### 8. لا أتمتة غير مصرّح بها

- لا أتمتة واتساب باردة أو أدوات scraping لأرقام واتساب.
- راجع `NO_FAKE_CLAIMS_POLICY.md` و `governance_os/draft_gate.py`.

## المسؤوليات

| الدور | المسؤولية |
|---|---|
| منشئ المسودة | استخدام قالب معتمد، التأكد من وجود موافقة |
| المراجِع | فحص المحتوى، تأكيد الموافقة، منح/رفض الإرسال |
| النظام | تطبيق بوابات consent_record + approval + suppression |

## الاختبارات ذات الصلة

- `tests/test_whatsapp_requires_opt_in.py`
- `tests/test_no_cold_whatsapp.py`
- `tests/test_v7_no_cold_whatsapp.py`
- `tests/test_suppression_blocks_all_channels.py`
- `tests/test_whatsapp_safety_gates.py`
- `tests/test_whatsapp_safe_send_v14.py`

## المصادقة

- **المسؤول**: فريق الامتثال + مسؤول تكامل Meta
- **المراجعة**: ربع سنوي أو عند تغيير سياسة Meta
- **المراجع**: `docs/ops/WHATSAPP_META_VERIFICATION.md`،
  `docs/ops/OUTBOUND_PRIVACY_RUNBOOK.md`