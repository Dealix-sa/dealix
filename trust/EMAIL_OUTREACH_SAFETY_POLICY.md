# Email Outreach Safety Policy

قواعد السلامة للتواصل عبر البريد الإلكتروني

## الغرض

ضمان أن كل إيميل خارجي يلتزم بقواعد السلامة والخصوصية والامتثال،
مع منع الإرسال التلقائي وحماية المستلمين من المحتوى المضلِّل.

## القواعد الإلزامية

### 1. آلية إلغاء الاشتراك (Unsubscribe)

- **كل إيميل تسويقي** يجب أن يحتوي على آلية واضحة لإلغاء الاشتراك.
- الطرق المقبولة: رابط unsubscribe، تعليمات نصية باللغة العربية
  ("لإلغاء الاشتراك ردّ بإيقاف")، رأس بريد `List-Unsubscribe`.
- الاختبار: `tests/test_email_requires_unsubscribe.py` يؤكد وجود
  آلية إلغاء في كل مسودة جاهزة للإرسال.

### 2. فحص قائمة الإيقاف (Suppression)

- قبل أي إرسال، يجب فحص وجهة الإرسال ضد قائمة الإيقاف.
- قائمة الإيقاف تشمل: منسحبون، مرتدون (bounces)، شكاوى،
  طلبات صريحة بالتوقف.
- الاختبار: `tests/test_suppression_blocks_all_channels.py`.
- لا يمكن تجاوز قائمة الإيقاف بأي ظرف.

### 3. لا مواضيع مضلِّلة

- لا استخدام `Re:` أو `Fwd:` أو `FW:` في موضوع إيميل بارد
  لمحاكاة رد على رسالة سابقة.
- الاختبار: `tests/test_outbound_safety_gates.py::TestOutboundNoFakeReplySubject`.

### 4. لا ادعاءات مضمونة

- لا "نتائج مضمونة"، "عائد مضمون"، "نضمن لك مبيعات"، "مضمون 100%".
- الاختبار: `tests/test_no_fake_claims.py` و
  `tests/test_v7_no_guaranteed_claims.py`.

### 5. موافقة بشرية قبل الإرسال

- لا إرسال تلقائي. كل إيميل يبدأ كمسودة بحالة `draft`.
- الإرسال يتطلب `approval_status == "approved"`.
- التنفيذ: `safe_send_gateway.enforce_consent_or_block`.

### 6. ساعات النشاط

- لا إرسال خارج ساعات النشاط السعودية (21:00-08:00).
- التنفيذ: `outreach_window.py`.

### 7. الأساس القانوني

- الإيميل التسويقي البارد يتطلّب أساساً قانونياً واضحاً (موافقة
  أو مصلحة مشروعة موثّقة).
- راجع `governance_os/lawful_basis.py`.

## المسؤوليات

| الدور | المسؤولية |
|---|---|
| منشئ المسودة | توليد محتوى متوافق، لا ادعاءات مضمونة، آلية إلغاء |
| المراجِع | فحص المحتوى، تأكيد التوافق، منح/رفض الموافقة |
| النظام | تطبيق البوابات، منع الإرسال بدون موافقة، فحص الإيقاف |

## الاختبارات ذات الصلة

- `tests/test_email_requires_unsubscribe.py`
- `tests/test_suppression_blocks_all_channels.py`
- `tests/test_no_auto_external_send.py`
- `tests/test_outbound_safety_gates.py`
- `tests/test_outreach_window_enforcement.py`

## المصادقة

- **المسؤول**: فريق الامتثال
- **المراجعة**: ربع سنوي
- **المراجع**: `docs/ops/EMAIL_DELIVERABILITY.md`،
  `docs/ops/OUTBOUND_PRIVACY_RUNBOOK.md`