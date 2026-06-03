# سياسة إمكانية التوصيل البريدي — هوية النطاق وصحة الإرسال
# Email Deliverability Policy — Domain Identity and Sending Health

**الجمهور:** المؤسس + مشغّل البنية التحتية  
**المرجع التقني:** `auto_client_acquisition/email/deliverability_check.py`  
**الوثائق ذات الصلة:** [COLD_EMAIL_COMPLIANCE_AR.md](COLD_EMAIL_COMPLIANCE_AR.md) · [SENDING_RAMP_PLAN_AR.md](SENDING_RAMP_PLAN_AR.md) · [docs/commercial/FOUNDER_PDPL_COMPLIANCE_PASS_AR.md](../commercial/FOUNDER_PDPL_COMPLIANCE_PASS_AR.md)

---

## ١. مبدأ جوهري

المسوّدة مسموح بها دائماً — 250 مسوّدة يومياً بدون قيود.  
الإرسال الفعلي ممنوع حتى تجتاز النطاق جميع بوابات الصحة أدناه.

**Draft is always allowed — up to 250 drafts/day.  
Live send is blocked until domain health gates are fully passed.**

---

## ٢. استراتيجية النطاق والنطاق الفرعي

### النطاق الأساسي مقابل نطاق الإرسال

| النوع | الغرض | المثال |
|---|---|---|
| نطاق العلامة التجارية | الموقع الرئيسي — لا يُستخدم للإرسال البارد | dealix.me |
| نطاق الإرسال المخصص | البريد الخارج فقط | mail.dealix.me أو outreach.dealix.me |
| نطاق التتبع المخصص | روابط التتبع وإلغاء الاشتراك | track.dealix.me |

**القاعدة الصارمة:** لا تُرسل بريداً بارداً من نطاق العلامة التجارية الرئيسي.  
إذا اكتسب نطاق الإرسال سمعة سيئة، يبقى dealix.me نظيفاً.

**Hard rule:** Never send cold outreach from the primary brand domain.  
Sending-domain reputation damage must not contaminate the brand domain.

---

## ٣. متطلبات سجلات DNS

### ٣.١ SPF — مطلوب لجميع المرسلين

```
v=spf1 include:_spf.google.com ~all
```

- يجب أن يبدأ بـ `v=spf1`
- يجب أن يتضمن آلية `include:` أو `ip4:` أو `ip6:` صالحة
- تحذير: لا تستخدم `+all` — يجعل السجل غير آمن تماماً
- المصدر: RFC 7208

### ٣.٢ DKIM — مطلوب للمرسلين بالجملة ومُوصى به للجميع

```
v=DKIM1; k=rsa; p=<مفتاح_عام>
```

- السجل على: `selector._domainkey.mail.dealix.me`
- يجب أن يتضمن `v=DKIM1` و`p=<مفتاح>`
- انسخ المفتاح من Google Admin Console أو مزوّد البريد الإلكتروني
- المصدر: RFC 6376

### ٣.٣ DMARC — مطلوب للمرسلين بالجملة ومُوصى به للجميع

```
v=DMARC1; p=quarantine; rua=mailto:dmarc@mail.dealix.me
```

- السجل على: `_dmarc.mail.dealix.me`
- `p=none` وضع مراقبة فقط — غير كافٍ للإرسال بالجملة
- `p=quarantine` الحد الأدنى الموصى به
- المصدر: RFC 7489

### ٣.٤ نطاق التتبع المخصص

- رابط إلغاء الاشتراك يجب أن يظهر من `track.dealix.me` وليس نطاقاً خارجياً
- يُضاف `List-Unsubscribe` و`List-Unsubscribe-Post` كترويسات في كل رسالة تسويقية
- يُعاد التحقق من صحة الرابط قبل كل دُفعة إرسال

### ٣.٥ Reply-To — صحة العنوان

- `reply_to` في `email_account` يجب أن يكون بريداً صالحاً ومُراقَباً
- لا يجوز أن يكون `noreply@` في البريد البارد — الرد اليدوي مطلوب
- انظر: [REPLY_HANDLING_OS_AR.md](REPLY_HANDLING_OS_AR.md)

---

## ٤. جدول عتبات صحة النطاق

| المقياس | مستوى آمن | تحذير | توقف إلزامي |
|---|---|---|---|
| معدل الارتداد (Bounce Rate) | أقل من 2% | 2% – 5% | أكثر من 5% |
| معدل الشكاوى البريدية (Spam Complaint) | أقل من 0.1% | 0.1% – 0.3% | أكثر من 0.3% |
| معدل إلغاء الاشتراك (Unsubscribe Rate) | أقل من 0.5% | 0.5% – 1% | أكثر من 1% |
| معدل الرد الإيجابي | أكثر من 2% | 0.5% – 2% | أقل من 0.5% مع ارتفاع باقي المقاييس |
| حالة SPF | صالح | غير مُهيَّأ | غائب أو خاطئ |
| حالة DKIM | صالح | غير مُهيَّأ | غائب أو خاطئ |
| حالة DMARC | صالح | `p=none` | غائب |
| حالة نطاق التتبع | صالح | لا يُراقَب | غائب أو مكسور |
| تحذيرات Gmail Postmaster | لا توجد | ملاحظات | تحذير نشط |

---

## ٥. حالات `overall_status` في `deliverability_check.py`

| الحالة | المعنى | الإرسال الفعلي مسموح؟ |
|---|---|---|
| `ready_for_marketing` | SPF + DKIM + DMARC + إلغاء اشتراك — كامل | نعم، بعد موافقة المؤسس |
| `ready_for_transactional` | SPF فقط — حجم منخفض | رسائل معاملاتية فقط |
| `needs_dkim` | SPF صالح، DKIM غائب | لا |
| `needs_dmarc` | SPF + DKIM صالحان، DMARC غائب | لا للإرسال بالجملة |
| `founder_action_needed` | SPF غائب أو خاطئ | لا — إجراء فوري مطلوب |
| `blocked_marketing` | DNS جاهز لكن لا توجد ترويسة إلغاء اشتراك | لا للبريد التسويقي |

---

## ٦. قائمة التحقق قبل الإرسال — Pre-Send Checklist

يجب اجتياز **جميع** البنود قبل إرسال أي دُفعة خارج بيئة المسوّدات.

| # | البند | المرجع |
|---|---|---|
| 1 | SPF صالح على نطاق الإرسال | `deliverability_check.py → _check_spf()` |
| 2 | DKIM صالح على نطاق الإرسال | `deliverability_check.py → _check_dkim()` |
| 3 | DMARC صالح على نطاق الإرسال (ليس `p=none`) | `deliverability_check.py → _check_dmarc()` |
| 4 | نطاق التتبع المخصص نشط ومختبر | فحص يدوي — انقر رابط تجريبياً |
| 5 | ترويسة `List-Unsubscribe` + `List-Unsubscribe-Post` مُضافة | `compliance.py → append_opt_out_line()` |
| 6 | `reply_to` صالح ومُراقَب | `email_account.reply_to` — فحص يدوي |
| 7 | العنوان البريدي الفعلي (physical address) موجود في تذييل الرسالة | فحص نص يدوي |
| 8 | قائمة الاستثناء (Suppression List) نشطة ومُفعَّلة | `compliance.py → suppression_emails / suppression_domains` |
| 9 | معالجة الارتداد مُفعَّلة (Bounce Handling) | إعداد Google Postmaster أو مزوّد البريد |
| 10 | مراقبة معدل الشكاوى نشطة | Google Postmaster Tools أو مزوّد مكافئ |

---

## ٧. معالجة الارتداد (Bounce Handling)

- **الارتداد الصلب (Hard Bounce):** أضف العنوان فوراً إلى قائمة الاستثناء بنوع `bounce`
- **الارتداد الناعم (Soft Bounce):** راقب؛ إذا تكرّر 3 مرات → استثنِه
- **ارتداد أكثر من 5% في دُفعة واحدة:** أوقف الإرسال فوراً وراجع قائمة الاستهداف
- كل ارتداد صلب يُوقف إرسال `compliance.py` لأن `bounced_before=True` تُعيد `allowed=False`

---

## ٨. مراقبة الشكاوى

- **هدف Gmail للمرسلين بالجملة:** أقل من 0.10% (المصدر: إرشادات Gmail للمرسلين بالجملة 2024)
- **الحد الأقصى المقبول:** 0.30% — تجاوزه يعني إيقاف الإرسال وإعادة المراجعة
- **أداة المراقبة:** Google Postmaster Tools (مجاني) — سجّل نطاقك وتتبع يومياً

---

## ٩. الحقول المرتبطة في `email_account`

```
email_account {
  domain            -- نطاق الإرسال (مثال: mail.dealix.me)
  spf               -- حالة SPF: valid | invalid | missing
  dkim              -- حالة DKIM: valid | invalid | missing
  dmarc             -- حالة DMARC: valid | p=none | missing
  tracking_domain   -- النطاق المخصص للتتبع (مثال: track.dealix.me)
  reply_to          -- بريد الرد المُراقَب
  warmup_stage      -- مرحلة الإحماء: 0 | 1 | 2 | 3 | 4
  daily_cap         -- الحد اليومي المسموح به حسب المرحلة
  health_status     -- الحالة الإجمالية: healthy | warning | paused | blocked
}
```

---

## EN Mirror — Email Deliverability Policy

**Audience:** Founder and infrastructure operator  
**Technical reference:** `auto_client_acquisition/email/deliverability_check.py`

### Core Principle

Up to 250 drafts/day are always permitted. Live sending is blocked until all domain health gates pass.

### Domain Strategy

Never cold-send from the primary brand domain. Use a dedicated sending subdomain (`mail.dealix.me`) and a separate custom tracking domain (`track.dealix.me`).

### DNS Requirements

- **SPF** (RFC 7208): required for all senders — must start `v=spf1` with at least one valid mechanism
- **DKIM** (RFC 6376): required for bulk senders — `v=DKIM1; k=rsa; p=<public_key>`
- **DMARC** (RFC 7489): required for bulk senders — `p=quarantine` minimum; `p=none` is monitor-only and insufficient
- **List-Unsubscribe + List-Unsubscribe-Post headers**: required on every marketing email per Google bulk-sender guidance (2024)

### Pre-Send Checklist

All 10 items in Section 6 must pass before any batch is released. The `deliverability_check.py` module returns `founder_action_needed` when SPF is absent — callers must hold at `draft_only` until resolved.

### Health Thresholds

Bounce > 5%, spam complaint > 0.3%, or any provider warning triggers an immediate sending pause. See the thresholds table in Section 4.

### Bounce Handling

Hard bounces → suppress immediately. Soft bounces → suppress after three occurrences. A single batch bounce spike above 5% stops all subsequent sends.

---

القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value
