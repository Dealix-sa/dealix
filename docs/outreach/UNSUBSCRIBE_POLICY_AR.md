# سياسة إلغاء الاشتراك وقائمة الاستثناء
# Unsubscribe and Suppression Policy

**الجمهور:** المؤسس + مشغّل مسار البريد  
**المراجع التقنية:** `auto_client_acquisition/email/compliance.py` · `auto_client_acquisition/safe_send_gateway/middleware.py`  
**الوثائق ذات الصلة:** [COLD_EMAIL_COMPLIANCE_AR.md](COLD_EMAIL_COMPLIANCE_AR.md) · [EMAIL_DELIVERABILITY_POLICY_AR.md](EMAIL_DELIVERABILITY_POLICY_AR.md) · [REPLY_HANDLING_OS_AR.md](REPLY_HANDLING_OS_AR.md)

---

## ١. المبدأ الجوهري

**إلغاء الاشتراك يُنفَّذ فوراً وبصفة دائمة.**  
لا استثناءات. لا «نرى الأمر لاحقاً». لا «ننتظر نهاية الحملة».  
أي رسالة ترسل بعد طلب إلغاء الاشتراك هي انتهاك مباشر لـ CAN-SPAM و PDPL.

**Unsubscribe is immediate and permanent.**  
No exceptions. No "we'll process it later." Any message sent after an opt-out request is a direct CAN-SPAM and PDPL violation.

---

## ٢. آلية إلغاء الاشتراك بنقرة واحدة — One-Click Unsubscribe

### ٢.١ ترويسات HTTP المطلوبة (Gmail 2024+)

يجب أن تتضمّن كل رسالة تسويقية ترويستَين:

```
List-Unsubscribe: <https://track.dealix.me/unsubscribe?uid={{uid}}&token={{token}}>
List-Unsubscribe-Post: List-Unsubscribe=One-Click
```

- الترويسة الأولى: رابط GET يتيح إلغاء الاشتراك عبر تطبيق البريد مباشرة
- الترويسة الثانية: تتيح إلغاء الاشتراك بنقرة واحدة (POST) بدون فتح الرسالة في المتصفح
- هذا مطلوب من Google لأي مرسل يُرسل أكثر من 5000 رسالة/يوم (المصدر: إرشادات Gmail للمرسلين بالجملة 2024)
- **موصى به لجميع الرسائل التسويقية بصرف النظر عن الحجم**

### ٢.٢ نص إلغاء الاشتراك في جسم الرسالة

`compliance.py → append_opt_out_line()` يضيف نص إلغاء الاشتراك تلقائياً إذا غاب:

```
— لإلغاء الاشتراك، ردّ بـ STOP أو OPT OUT.
  To unsubscribe, reply STOP.
```

لا يُرسَل أي بريد خارجي بدون هذا النص أو رابط إلغاء اشتراك واضح.

### ٢.٣ كيف يظهر رابط إلغاء الاشتراك في المسوّدات

- المسوّدات تُولَّد مع رابط إلغاء اشتراك حقيقي (وليس placeholder) قبل عرضها على المؤسس
- الرابط يُشير إلى `track.dealix.me/unsubscribe?uid=...` مع token مشفّر
- المؤسس يتحقق من صحة الرابط كجزء من قائمة التحقق قبل الإرسال ([EMAIL_DELIVERABILITY_POLICY_AR.md](EMAIL_DELIVERABILITY_POLICY_AR.md))
- رابط مكسور أو غائب → يمنع الإرسال تلقائياً

---

## ٣. مسار إلغاء الاشتراك — Opt-Out Workflow

```
المستلم يطلب إلغاء الاشتراك (رابط أو رد STOP أو OPT OUT أو إيقاف أو إلغاء)
        ↓
reply_classifier.py يُصنّف الرد فوراً كـ "unsubscribe"
        ↓
الإضافة الفورية إلى suppression list بـ type=email، reason=unsubscribe
        ↓
compliance.py يُعيد allowed=False لأي رسالة لاحقة (contact_opt_out=True)
        ↓
safe_send_gateway/middleware.py يرفع SendBlocked(reason_code="opted_out")
        ↓
رد إقرار يُرسَل فوراً: "تم إيقاف التواصل. لن أتواصل مرة ثانية."
        ↓
تسجيل في سجل المراجعة (audit log) مع طابع زمني
```

**ملاحظة:** رد الإقرار (acknowledgment) مسموح بإرساله تلقائياً لأن `reply_classifier.py` يضبط `auto_send_allowed=True` لفئة `unsubscribe`. هذا الاستثناء الوحيد للإرسال التلقائي بدون موافقة إضافية.

---

## ٤. مخطط قائمة الاستثناء — Suppression Record

حقول كل سجل في قائمة الاستثناء:

```
suppression {
  value      -- البريد الإلكتروني أو النطاق أو اسم الشركة المُستثنى
  type       -- email | domain | company
  reason     -- unsubscribe | bounce | complaint | do_not_contact | manual
  added_at   -- طابع زمني ISO 8601
}
```

### حالات `reason`

| السبب | المصدر | دائم؟ |
|---|---|---|
| `unsubscribe` | طلب صريح من المستلم | نعم — لا يُحذف أبداً |
| `bounce` | ارتداد صلب أو ارتداد ناعم متكرر | نعم — يُراجع فقط بتصريح مؤسس |
| `complaint` | بلاغ spam من المستلم | نعم — لا يُحذف أبداً |
| `do_not_contact` | قرار مؤسس صريح | نعم — يُعدَّل بقرار مؤسس فقط |
| `manual` | إضافة يدوية من المؤسس | يُحدَّد عند الإضافة |

### حالات `type`

| النوع | ما يُستثنى | مثال |
|---|---|---|
| `email` | عنوان بريد محدد | `john.doe@acme.com` |
| `domain` | جميع عناوين نطاق | `acme.com` → يمنع `*@acme.com` |
| `company` | جميع جهات اتصال شركة | سجل CRM بـ `company_id` |

---

## ٥. الاحتفاظ بقائمة الاستثناء — Retention

- **`reason=unsubscribe` أو `complaint`:** لا حذف أبداً — يُحتفظ بها إلى أجل غير مسمّى
- **`reason=bounce`:** يُحتفظ بها للمدة التشغيلية؛ مراجعة دورية كل 6 أشهر إذا كان الارتداد ناعماً
- **`reason=manual` أو `do_not_contact`:** يُحتفظ بها حتى قرار مؤسس صريح بالإزالة
- **PDPL:** طلب حذف البيانات يعني حذف السجل من CRM — **لكن** إدخال قائمة الاستثناء يبقى لأغراض الامتثال (منع الاتصال المستقبلي)

---

## ٦. مراجعة إلغاءات الاشتراك — Opt-Out Audit

| المراجعة | التكرار | المسؤول |
|---|---|---|
| مراجعة إضافات اليوم إلى قائمة الاستثناء | يومياً — في لوحة تحكم المؤسس الصباحية | المؤسس |
| التحقق من أن جميع حالات `unsubscribe` أُضيفت بشكل صحيح | قبل كل دُفعة | مشغّل مسار البريد |
| تقرير شهري: حجم قائمة الاستثناء + معدل النمو | شهرياً | المؤسس |
| فحص سلامة قائمة الاستثناء (هل تعمل البوابة؟) | أسبوعياً | اختبار يدوي أو آلي |

للتفاصيل عن قائمة انتظار الردود: [REPLY_HANDLING_OS_AR.md](REPLY_HANDLING_OS_AR.md)

---

## ٧. عمليات قائمة الاستثناء في الكود

`compliance.py → check_outreach()` تتحقق من ثلاثة مستويات:

```python
# 1. تحقق من العنوان المباشر
if to_email.lower() in suppression_emails:
    reasons.append("email_suppressed")

# 2. تحقق من النطاق
domain = to_email.split("@", 1)[1].lower()
if domain in suppression_domains:
    reasons.append("domain_suppressed")

# 3. تحقق من حالة opt-out في CRM
if contact_opt_out:
    reasons.append("contact_opt_out_true")
```

أي سبب من هذه الثلاثة يُعيد `allowed=False` — لا إرسال.

---

## EN Mirror — Unsubscribe and Suppression Policy

**Audience:** Founder and outbound pipeline operators

### Core Principle

An unsubscribe request, however received — one-click link, `List-Unsubscribe` header activation, reply containing STOP / OPT OUT / إيقاف — triggers immediate and permanent suppression. There is no grace period.

### One-Click Unsubscribe

Every marketing email carries two headers per Google's 2024 bulk-sender requirements:
- `List-Unsubscribe`: a URL pointing to `track.dealix.me/unsubscribe`
- `List-Unsubscribe-Post: List-Unsubscribe=One-Click`

`compliance.py → append_opt_out_line()` appends an in-body opt-out line if the text is absent. A missing or broken unsubscribe link blocks the send.

### Suppression Record Fields

Each suppression record contains: `value`, `type` (email | domain | company), `reason` (unsubscribe | bounce | complaint | do_not_contact | manual), `added_at`.

`unsubscribe` and `complaint` records are never deleted.  
`bounce` records are retained operationally; reviewed every 6 months.

### Opt-Out Workflow

Reply classified as `unsubscribe` → immediate suppression → `compliance.py` returns `allowed=False` → `safe_send_gateway` raises `SendBlocked(reason_code="opted_out")` → acknowledgment reply sent → audit log entry created.

### CAN-SPAM SLA

Maximum 10 business days to honor opt-out requests (legal requirement). Operational target: immediate — before any subsequent message is sent.

---

القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value
