# سياسة الامتثال للبريد الإلكتروني البارد
# Cold Email Compliance Policy

**الجمهور:** المؤسس + أي شخص يُشغّل مسار البريد الخارج  
**المراجع التقنية:** `auto_client_acquisition/email/compliance.py` · `auto_client_acquisition/channel_policy_gateway/email.py` · `auto_client_acquisition/safe_send_gateway/doctrine.py`  
**الوثائق ذات الصلة:** [EMAIL_DELIVERABILITY_POLICY_AR.md](EMAIL_DELIVERABILITY_POLICY_AR.md) · [UNSUBSCRIBE_POLICY_AR.md](UNSUBSCRIBE_POLICY_AR.md) · [docs/commercial/FOUNDER_PDPL_COMPLIANCE_PASS_AR.md](../commercial/FOUNDER_PDPL_COMPLIANCE_PASS_AR.md)

> **تحذير قانوني:** هذه الوثيقة ملخّص تشغيلي. ليست استشارة قانونية. استشر محامياً قبل أي ادعاء «امتثال كامل».

---

## ١. الإطار التنظيمي المُطبَّق

يعمل Dealix في السوق السعودي ويستهدف شركات مسجّلة. ثلاثة أطر تنظيمية تؤثر على البريد الخارج:

| الإطار | النطاق | ما يفرضه تشغيلياً |
|---|---|---|
| إرشادات Gmail للمرسلين بالجملة (2024) | أي مرسل إلى مستلمين Gmail | SPF + DKIM + DMARC + إلغاء اشتراك بنقرة واحدة + معدل شكاوى أقل من 0.3% |
| CAN-SPAM | الرسائل التجارية للمستلمين في الولايات المتحدة | لا عناوين مضلّلة، لا موضوعات خادعة، عنوان بريدي فعلي، احترام طلبات إلغاء الاشتراك خلال 10 أيام عمل |
| PDPL السعودي | معالجة بيانات الأشخاص السعوديين | أساس قانوني، تقليل البيانات، حذف البيانات عند الطلب، لا قوائم مشتراة |

---

## ٢. القواعد الصارمة — Hard Rules

هذه القواعد غير قابلة للتفاوض ومُنفَّذة برمجياً في `compliance.py` و`doctrine.py`:

- **250 مسوّدة/يوم مسموح** — بدون قيود
- **250 إرسالاً فعلياً/يوم غير مسموح** حتى تجتاز: صحة النطاق + إلغاء الاشتراك + قائمة الاستثناء + خطة الإحماء — انظر [SENDING_RAMP_PLAN_AR.md](SENDING_RAMP_PLAN_AR.md)
- لا قوائم مشتراة أو مجمَّعة (harvested lists) بأي شكل
- لا موضوعات مضلّلة أو خادعة في أي رسالة
- لا استخدام `Re:` أو `Fwd:` مزيّف في موضوع البريد البارد
- احترم طلبات إلغاء الاشتراك خلال 10 أيام عمل كحد أقصى (فوري كهدف تشغيلي)
- موافقة المؤسس مطلوبة قبل أي إرسال خارجي — لا إرسال تلقائي بدون موافقة
- لا أتمتة WhatsApp الباردة — مسوّدات فقط مع موافقة
- لا أتمتة LinkedIn — مسوّدات فقط
- لا scraping أو جمع ويب غير مصرّح
- لا وعود بمبيعات مضمونة — «فرص مُثبتة بأدلة» فقط

---

## ٣. ما يجعل موضوع البريد مضلّلاً

| محظور | مقبول |
|---|---|
| `Re: اجتماعنا الأخير` (بدون اجتماع سابق) | `استعلام: نظام رد الـ leads` |
| `Fwd: توصية من طارق` (بدون توصية فعلية) | `كيف يرد فريقكم على leads الموقع؟` |
| `فزت بجائزة / حصلت على خصم` (إذا لم يكن صحيحاً) | `عرض Pilot 7 أيام لوكالات الرياض` |
| `تأكيد موعدنا` (بدون موعد محجوز) | `طلب اجتماع قصير — 15 دقيقة` |
| أي موضوع يوحي بعلاقة سابقة غير موجودة | أي موضوع يصف الرسالة بدقة |

**القاعدة الاختبارية:** هل سيشعر المستلم بالخداع عند فتح الرسالة؟ إذا كان الجواب نعم — الموضوع محظور.

---

## ٤. هوية المرسل المطلوبة

كل رسالة خارجية يجب أن تتضمّن:

- **الاسم الكامل للشركة:** Dealix أو الاسم التجاري المسجّل
- **العنوان البريدي الفعلي (Physical Address):** مطلوب بموجب CAN-SPAM — أضفه في تذييل كل رسالة
- **عنوان بريد إلكتروني صالح:** لا `noreply@` في البريد البارد
- **رابط إلغاء اشتراك واضح:** في جسم الرسالة وكترويسة `List-Unsubscribe`

```
تذييل إلزامي (مثال):
Dealix — [عنوانكم الفعلي، الرياض، المملكة العربية السعودية]
لإلغاء الاشتراك: [رابط] أو ردّ بـ STOP
To unsubscribe: [link] or reply STOP
```

---

## ٥. إجراء احترام إلغاء الاشتراك — Opt-Out SLA

| الخطوة | المهلة |
|---|---|
| استلام طلب إلغاء الاشتراك (رابط أو رد STOP) | فوري (لحظة استلام الرد) |
| إضافة إلى قائمة الاستثناء في النظام | فوري — `compliance.py` يمنع الإرسال عند `contact_opt_out=True` |
| وقف جميع الرسائل المجدولة لهذا المستلم | خلال دقائق من الإضافة |
| الحد الأقصى المسموح قانونياً (CAN-SPAM) | 10 أيام عمل |
| **هدفنا التشغيلي** | **فوري — قبل أي رسالة تالية** |

للتفاصيل الكاملة: [UNSUBSCRIBE_POLICY_AR.md](UNSUBSCRIBE_POLICY_AR.md)

---

## ٦. الممارسات المحظورة — Banned Practices

المحظورات التالية مُنفَّذة في `doctrine.py → enforce_doctrine_non_negotiables()`:

- **scraping:** جمع بيانات ويب غير مصرّح — محظور تماماً
- **أتمتة WhatsApp الباردة:** إرسال جماعي بارد عبر WhatsApp — محظور؛ مسوّدات فقط مع موافقة
- **أتمتة LinkedIn:** أي أتمتة خارجية عبر LinkedIn — محظور
- **تواصل جماعي بدون حوكمة:** bulk outreach بدون موافقة وبوابات الحوكمة — محظور
- **وعود مبيعات مضمونة:** لا «نضمن مبيعات» أو أرقام تحويل كحقائق — «فرص مُثبتة بأدلة» فقط
- **قوائم مشتراة:** لا استخدام قوائم بريد إلكتروني تجارية مشتراة أو مُجمَّعة
- **إرسال خارجي بدون موافقة:** أي إرسال على اسم العميل يتطلب موافقته الصريحة

---

## ٧. حالات `compliance_status`

يُرجع `compliance.py → check_outreach()` `ComplianceCheck` بـ `allowed: bool`. ترجمتها إلى حالات التشغيل:

| الحالة | المعنى | الإجراء |
|---|---|---|
| `pass` | `allowed=True`، لا أسباب حظر | متاح للإدراج في طابور موافقة المؤسس |
| `needs_fix` | `requires_human_review=True` مع ملاحظات | يظهر للمؤسس مع تفاصيل المراجعة |
| `blocked` | `allowed=False`، قائمة `blocked_reasons` مملوءة | لا يُرسل — يُسجَّل سبب الحظر ويُعلَم المؤسس |

أسباب الحظر الممكنة من `compliance.py`:

- `contact_opt_out_true` — المستلم ألغى الاشتراك
- `email_suppressed` — العنوان في قائمة الاستثناء
- `domain_suppressed` — النطاق في قائمة استثناء النطاقات
- `bounced_before` — سبق ارتداد هذا العنوان
- `risk_score_too_high` — درجة المخاطرة أعلى من 50
- `allowed_use_missing` — لا أساس قانوني مُسجَّل
- `daily_limit_hit` — وصل حد الإرسال اليومي
- `batch_size_hit` — وصل حد حجم الدُّفعة
- `batch_cooldown` — فترة الانتظار بين الدُّفعات لم تنتهِ

---

## ٨. PDPL — النقاط التشغيلية

- **الأساس القانوني:** يجب أن يكون لكل جهة استهداف أساس قانوني مُوثَّق في حقل `allowed_use`
- **تقليل البيانات:** لا تجمع أكثر من: اسم الشركة، المسمّى الوظيفي، بريد العمل، القطاع
- **حذف البيانات:** طلب الحذف → استثناء من جميع القوائم + حذف من CRM خلال 30 يوم
- **لا قوائم مشتراة:** أي قائمة مشتراة تعني غياب الأساس القانوني — محظورة تلقائياً
- **تخزين البيانات:** يُحفظ في Postgres مُقيَّد بصلاحيات — لا إرسال لجهات خارجية

للتفاصيل: [docs/commercial/FOUNDER_PDPL_COMPLIANCE_PASS_AR.md](../commercial/FOUNDER_PDPL_COMPLIANCE_PASS_AR.md)

---

## EN Mirror — Cold Email Compliance Policy

**Audience:** Founder and outbound pipeline operators  
**Hard rules enforced in code:** `compliance.py`, `doctrine.py`

### Applicable Frameworks (Operational Summary — Not Legal Advice)

- **Gmail bulk-sender guidance (2024):** SPF + DKIM for all senders; SPF + DKIM + DMARC for bulk senders; one-click `List-Unsubscribe` on every marketing email; spam-complaint rate below 0.3% (target: below 0.1%)
- **CAN-SPAM:** No false or misleading headers or subject lines; clear opt-out mechanism honored within 10 business days; valid physical postal address in every message; no harvested lists
- **PDPL-aware:** Lawful basis required for each target; data minimization; right to erasure honored within 30 days; no purchased lists

### Hard Rules

- 250 drafts/day always permitted
- 250 live sends/day NOT permitted until domain health + unsubscribe + suppression + ramp gates all pass
- No purchased lists; no misleading subjects; no fake Re:/Fwd:; honor opt-outs; founder approval before any send; no cold WhatsApp/LinkedIn automation; no scraping

### Subject Line Test

A subject is misleading if the recipient would feel deceived upon opening. Using `Re:` or `Fwd:` to imply a prior conversation that did not happen is a CAN-SPAM violation and is banned in this system.

### Compliance Status

`compliance.py` returns `allowed=True` (pass), `requires_human_review=True` (needs_fix), or `allowed=False` with `blocked_reasons` (blocked). Blocked records are never sent; they are logged and surfaced to the founder queue.

---

القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value
