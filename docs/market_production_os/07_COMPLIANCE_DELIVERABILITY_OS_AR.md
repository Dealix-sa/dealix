# Compliance & Deliverability OS — بوابة الامتثال والوصولية — Compliance & Deliverability OS

> الموضع في العمود الفقري: المكوّن السابع في طبقة *Market Production OS*.
> راجع [`00_MARKET_PRODUCTION_OS_MASTER_AR.md`](00_MARKET_PRODUCTION_OS_MASTER_AR.md) §7 (القواعد الصارمة).

هذه **البوابة الحاسمة** التي تقف بين المصنع (المكوّن 6) وبوابة موافقة المؤسس (المكوّن 8). كل مسودة
تمرّ بها قبل أن تُعرَض للاعتماد. تجمع البوابة بين **الجودة + الامتثال** من جهة، و**الوصولية
(deliverability)** من جهة أخرى. لا تمرّ مسودة فاشلة في أي فحص — تُردّ للمصنع أو تُعلَّم `fail`.

---

## 1. ماذا تُركّب البوابة (Reused Cores)

البوابة طبقة رقيقة تنسّق ثلاث أنوية موجودة، ولا تكرّر منطقها:

| النواة | المسار | الدور |
|---|---|---|
| فحص سياسة المسودة | `governance_os.policy_check_draft` | يرفض اللغة المحظورة (أتمتة LinkedIn، واتساب بارد، scraping…) |
| تدقيق سلامة الادعاء | `governance_os.audit_claim_safety` | يرفض الادعاءات بلا دليل أو وعود نتيجة |
| منع الهدر | `revenue_os.anti_waste.validate_pipeline_step` | يرفض المصدر المحظور وغياب Decision Passport |
| + فحوص الوصولية | (هذا المستند) | DNS + سمعة الدومين + suppression |

> أي مسودة لا تحمل `governance_decision` تُرفض فورًا — «لا مخرج بدون قرار حوكمة» (المرجع الرئيسي §3).

---

## 2. قائمة فحص DNS والوصولية (Deliverability Checklist)

قبل تفعيل أي إرسال على دومين، يجب اكتمال هذه القائمة (تُراجَع دوريًا، لا مرة واحدة):

| العنصر | المتطلّب | لماذا |
|---|---|---|
| `SPF` | سجل صالح يدرج مُرسِلي الدومين المعتمدين | يمنع انتحال المُرسِل |
| `DKIM` | توقيع مفاتيح صالح ومحدّث | يثبت سلامة الرسالة وأصلها |
| `DMARC` | سياسة منشورة (`p=quarantine`/`reject`) + تقارير | محاذاة SPF/DKIM + تقارير سمعة |
| Custom tracking domain | نطاق تتبّع خاص لا مشترك | يحمي السمعة من جيران سيّئين |
| Valid reply-to | عنوان رد حقيقي يُراقَب | احترام الرد البشري، لا صندوق مهجور |
| Unsubscribe endpoint | رابط/آلية إلغاء اشتراك تعمل فعليًا | شرط قانوني وتشغيلي |
| Suppression list | قائمة محظورين محدّثة ومطبّقة | لا تواصل مع من طلب التوقّف |
| Bounce handling | معالجة ارتداد آلية تُحدّث القائمة | تحمي معدّل الارتداد والسمعة |
| Google Postmaster Tools | مراقبة سمعة الدومين/IP لدى Gmail | إنذار مبكر قبل تدهور الوصول |

> هذه القائمة جزء من شرط `domain_health_ok` في بوابة الإرسال (المكوّن 8). نقص أي عنصر → الإرسال متوقّف.

---

## 3. القائمة المحظورة (Forbidden — تُرفض دائمًا)

هذه سلوكيات ممنوعة، وليست خيارات قابلة للتفعيل:

- قوائم بريد **مشتراة** أو مستأجرة أو مُسرَّبة.
- مواضيع **مضللة** لا تطابق المحتوى.
- استخدام `Re:`/`Fwd:` **زائفة** لإيهام علاقة سابقة.
- إرسال **بلا unsubscribe**.
- **تجاهل opt-out** أو إعادة التواصل بعد طلب التوقّف.
- الإرسال إلى **قائمة suppression**.
- **ادعاءات بلا دليل** أو وعود نتيجة/أرقام مبيعات.
- أتمتة LinkedIn، واتساب بارد، أو scraping يخالف الشروط.

أي مسودة تطابق واحدة من هذه → `compliance_status = "fail"` وتُحجَب عن بوابة الموافقة.

---

## 4. المعايير المرجعية (Standards — نثرًا)

نلتزم بهذه المعايير بوصفها قواعد تشغيلية، لا شعارات. الإشارة هنا نثرية موجزة، والتفصيل القانوني في
[`../commercial/MARKET_INTELLIGENCE_PDPL_LEGAL_REVIEW_AR.md`](../commercial/MARKET_INTELLIGENCE_PDPL_LEGAL_REVIEW_AR.md).

- **CAN-SPAM:** يمنع الترويسات والمواضيع المخادعة، ويُلزم بآلية إلغاء اشتراك واضحة، وباحترام طلب
  الإلغاء خلال **عشرة أيام عمل**. عمليًا: كل مسودة عندنا تحمل unsubscribe، وكل opt-out يُنفَّذ
  فورًا ويُضاف لقائمة suppression قبل أي إرسال لاحق.
- **DMARC:** سياسة يضبطها **مالك الدومين** في DNS فوق محاذاة SPF/DKIM، مع تقارير دورية تكشف
  محاولات الانتحال وصحة المحاذاة. عمليًا: ننشر سياسة DMARC ونراقب تقاريرها كجزء من صحة الدومين.
- **قائمة Suppression:** هي العناوين/الجهات التي **طلبت عدم التواصل** (إلغاء اشتراك، شكوى، ارتداد
  دائم). عمليًا: تُفحَص قبل كل إرسال، والإضافة إليها نهائية ولا تُلغى آليًا.
- **أساس PDPL:** كل تواصل يحتاج أساسًا قانونيًا معلنًا (مصلحة مشروعة/عقد/موافقة) موثّقًا في
  `data_os.SourcePassport` — راجع المراجعة القانونية الداخلية أعلاه.

> هذه إشارة تشغيلية موجزة، لا استشارة قانونية. أي نص في عقد أو موقع يمرّ بمحامٍ سعودي قبل النشر.

---

## 5. مقاييس مراجعة صحة الدومين (Domain Health Review)

تُراجَع هذه المقاييس دوريًا (يوميًا أثناء الـ warm-up، ثم أسبوعيًا)، وتغذّي قرار رفع/خفض سقف الإرسال:

| المقياس | العتبة الآمنة | الإجراء عند التجاوز |
|---|---|---|
| Bounce rate | منخفض ومستقر | تجميد الرفع + تنظيف القائمة |
| Spam complaint rate | **< 0.3%** | إيقاف الإرسال فورًا + مراجعة الاستهداف |
| Unsubscribe rate | منخفض | مراجعة الرسالة والتخصيص |
| Reply rate | إشارة صحّة إيجابية | يُستخدم في المراجعة الأسبوعية |
| Positive reply rate | المؤشّر الأهم للجودة | يقود اختيار العرض/القطاع |
| Provider warnings | صفر تحذيرات | أي تحذير → تجميد + فحص DNS |

> معدّل شكوى السبام **< 0.3%** خط أحمر: تجاوزه يوقف الإرسال على الدومين حتى المعالجة، بصرف النظر
> عن مرحلة التدرّج.

---

## 6. شرط الإرسال (يتكرر هنا للتأكيد)

البوابة تتحقّق من جاهزية شروط الإرسال، لكنها **لا ترسل**. الإرسال الفعلي حصري للمكوّن 8 بعد موافقة
المؤسس. الشروط الستة، **كلها معًا**:

```txt
send_allowed = (
  approval            AND
  unsubscribe_included AND
  domain_health_ok    AND
  suppression_check   AND
  personalization >= P1 AND
  risk_level in {low, medium}
)
```

غياب أي شرط → لا إرسال. (التفصيل في [`08_APPROVAL_QUEUE_AND_SENDING_RAMP_AR.md`](08_APPROVAL_QUEUE_AND_SENDING_RAMP_AR.md).)

---

## 7. مخرجات البوابة لكل مسودة

| الحقل | القيمة بعد البوابة |
|---|---|
| `compliance_status` | `pass` أو `fail` (مع سبب) |
| `risk_level` | مُعاد تقييمه: `low`/`medium`/`high` |
| `domain_health_ok` | `true`/`false` على مستوى الدومين |
| `suppression_check` | `true`/`false` على مستوى المستلِم |
| `governance_decision` | قرار الحوكمة المرجعي |

- المسودات `pass` فقط تُمرَّر لبوابة الموافقة، مرتّبة لاحقًا ضمن Top-50.
- المسودات `fail` تُعاد للمصنع مع السبب، أو تُؤرشَف إن كان العيب في المصدر/الجهة.
- `risk_level = high` يُعلَّم بوضوح في تقرير المؤسس ولا يدخل دفعة الإرسال المقترَحة تلقائيًا.

---

## 8. الربط مع الطبقات الأخرى

- المدخل: مسودات [`06_COLD_EMAIL_DRAFT_FACTORY_AR.md`](06_COLD_EMAIL_DRAFT_FACTORY_AR.md) بحالة `send_status=draft`.
- النواة: `governance_os.policy_check_draft` + `governance_os.audit_claim_safety` + `revenue_os.anti_waste.validate_pipeline_step`.
- المخرج: بوابة الموافقة وتدرّج الإرسال [`08_APPROVAL_QUEUE_AND_SENDING_RAMP_AR.md`](08_APPROVAL_QUEUE_AND_SENDING_RAMP_AR.md).
- الخصوصية: [`../commercial/MARKET_INTELLIGENCE_PDPL_LEGAL_REVIEW_AR.md`](../commercial/MARKET_INTELLIGENCE_PDPL_LEGAL_REVIEW_AR.md).
- العقيدة: المرجع الرئيسي §7 + اللاءات الإحدى عشرة §1.

---

## EN summary

`Compliance & Deliverability OS` is the seventh Market Production OS component — the decisive gate
between the draft factory and the founder approval queue. It is a thin layer that composes three
existing cores — `governance_os.policy_check_draft`, `governance_os.audit_claim_safety`, and
`revenue_os.anti_waste.validate_pipeline_step` — plus deliverability checks. The DNS/deliverability
checklist covers SPF, DKIM, DMARC, a custom tracking domain, a valid reply-to, an unsubscribe
endpoint, a suppression list, bounce handling, and Google Postmaster Tools. Forbidden behaviors —
purchased lists, misleading subjects, fake Re:/Fwd:, missing unsubscribe, ignoring opt-out,
sending to a suppression list, unevidenced claims, plus LinkedIn automation, cold WhatsApp, and
scraping — always fail. Standards cited in prose: CAN-SPAM (no deceptive headers, clear opt-out,
honored within ten business days), DMARC (a domain-owner DNS policy over SPF/DKIM alignment with
reporting), and the suppression list (addresses that asked not to be contacted). Domain-health
metrics — bounce, spam complaint **< 0.3%**, unsubscribe, reply, positive reply, and provider
warnings — feed the sending-ramp decision. The gate validates but never sends; the six-part send
condition (approval, unsubscribe_included, domain_health_ok, suppression_check, personalization
≥ P1, risk_level in {low, medium}) must hold in full.

> القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.
