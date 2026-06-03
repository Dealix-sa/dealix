# 11 — إنتاج المحتوى — Content Production OS

> الموقع في الطبقة: المكوّن رقم 12 من *Market Production OS*. قناة جذب واردة (inbound)، لا قناة دفع بارد.
> العمود الفقري: [`00_MARKET_PRODUCTION_OS_MASTER_AR.md`](00_MARKET_PRODUCTION_OS_MASTER_AR.md).

هذا المستند يحدّد مصنع المحتوى اليومي والأسبوعي لصوت المؤسس. كل قطعة محتوى **تُسوَّد للمراجعة**، ولا
يُنشَر أي شيء تلقائيًا — النشر (بما فيه منشورات LinkedIn) إجراء خارجي يتطلب موافقة المؤسس. المحتوى وسيلة
جذب تبني الثقة وتولّد ردودًا واردة تتغذّى منها بقية الطبقة، وليس بديلًا عن العمل المُحوكَم.

> القاعدة الأساسية: **كل قطعة تُسوَّد، لا تُنشَر تلقائيًا.** الإيقاع الثابت يخدم
> [`docs/content/LINKEDIN_CADENCE_PLAN.md`](../content/LINKEDIN_CADENCE_PLAN.md) (3 منشورات/أسبوع، 3 مسارات).

---

## 0. المبدأ الحاكم لطبقة المحتوى

- كل قطعة محتوى تربط ست عناصر إلزامية: **قطاع + ألم + سير عمل + إثبات + عرض + دعوة (CTA).**
- بلا أسماء عملاء، بلا أرقام غير مُتحقَّقة. الأرقام مسموحة فقط Client-Confirmed، وإلا فهي "نمط آمن".
- بلا ضمان نتائج، بلا emojis، بلا اسم نموذج، بلا ادعاء بلا مصدر.
- النشر إجراء خارجي = موافقة المؤسس على كل منشور قبل النشر.

---

## 1. الإنتاج اليومي (4 قطع تُسوَّد يوميًا)

| # | النوع | الغرض | الزاوية |
|---|---|---|---|
| 1 | رؤية المؤسس (founder insight) | صوت قيادي حازم | درس/موقف من بناء عمليات مُحوكَمة |
| 2 | منشور ألم قطاعي (sector-pain) | يلامس وجع محدّد | ألم متكرّر في قطاع مستهدف + كيف يُحوكَم حلّه |
| 3 | منشور إثبات/تعلّم (proof/learning) | يُظهر آلة الحوكمة | جواز مصدر، درجة جودة بيانات، قرار حوكمة (بلا PII) |
| 4 | منشور بأسلوب دراسة حالة قصيرة (case-style) | نتيجة آمنة | نمط قطاعي مجهّل، أرقام Client-Confirmed فقط |

كل قطعة يومية تُختَم بإخلاء مسؤولية القيمة، وتُمرَّر على اللاءات قبل دخول طابور الموافقة.

---

## 2. الإنتاج الأسبوعي (5 قطع أعمق)

| # | النوع | الغرض |
|---|---|---|
| 1 | منشور LinkedIn طويل | طرح فكرة حاكمة بعمق (مثال: لماذا نرفض اختصارًا) |
| 2 | سكربت كاروسيل (carousel script) | تفكيك مفهوم في شرائح متسلسلة |
| 3 | مسودة دراسة حالة (case-study draft) | نمط آمن مفصّل، يُوسم "افتراضي/آمن" إن لا عميل مُسمّى |
| 4 | شرح منتج (product explainer) | كيف تعمل طبقة من الطبقات (Proof Pack، Reply Handling…) |
| 5 | درس المؤسس (founder lesson) | احتكاك علني → أصل قابل لإعادة الاستخدام |

المنشور الطويل والكاروسيل يخدمان مسارات الأسبوع في
[`LINKEDIN_CADENCE_PLAN.md`](../content/LINKEDIN_CADENCE_PLAN.md)، ونموذج الصوت في
[`LINKEDIN_POST_001.md`](../content/LINKEDIN_POST_001.md). لا تُكرّر خطة الإيقاع — وسّعها.

---

## 3. ربط العناصر الستة (إلزامي لكل قطعة)

| العنصر | السؤال الذي يجيب عنه | المصدر |
|---|---|---|
| قطاع | لمن هذه القطعة؟ | `seeds/sectors.yaml` · `docs/sector-reports/` |
| ألم | أي وجع محدّد تلامس؟ | الـ playbooks القطاعية |
| سير عمل | أي مسار يُحوكِم الحل؟ | طبقات OS (`06`–`10`) |
| إثبات | ما الدليل/النمط الآمن؟ | حزمة الإثبات · `value_ledger` (Client-Confirmed) |
| عرض | إلى أي درجة يقود؟ | السلّم الخماسي ([§5](00_MARKET_PRODUCTION_OS_MASTER_AR.md)) |
| دعوة (CTA) | ما الخطوة التالية؟ | "تشخيص" / رد واردة → [`09`](09_REPLY_HANDLING_OS_AR.md) |

قطعة بلا أحد العناصر الستة = **تُرفض في المراجعة** وتُعاد صياغتها. الدعوة تقود دائمًا إلى **رد وارد**
يُعالَج في [`09_REPLY_HANDLING_OS_AR.md`](09_REPLY_HANDLING_OS_AR.md) — لا إلى تواصل بارد.

---

## 4. خط الإنتاج (Pipeline)

| الخطوة | المخرج | البوابة |
|---|---|---|
| توليد | 4 قطع يومية / 5 أسبوعية (`status=draft`) | تلقائي |
| فحص الصوت | مطابقة نبرة المؤسس + اللاءات | تلقائي + بشري |
| فحص الادعاء | كل رقم له مصدر؛ بلا ضمان؛ بلا PII | `governance_os.audit_claim_safety` |
| طابور الموافقة | المؤسس يعتمد ما يُنشَر | موافقة المؤسس |
| النشر | يدوي بعد الاعتماد | المؤسس فقط |
| القياس | ردود واردة محوّلة (لا متابعون) | تقرير GTM |

---

## 5. إعادة الاستخدام (Reuse)

- `auto_client_acquisition/gtm_os/content_calendar.py` — تقويم المحتوى والإيقاع.
- `dealix/marketing_factory/` — توليد الحزم: `weekly_pack.py`، `content_calendar.seed.yaml`،
  `utm.py`، `store.py`.
- التوثيق القائم: [`docs/content/`](../content/) — خطة الإيقاع ونماذج المنشورات.

> أعد الاستخدام قبل أن تكتب: مصنع المحتوى والتقويم موجودان. هذا المستند = **سياسة الإنتاج والربط بالعناصر الستة**.

---

## 6. القياس (يُغذّي التقرير اليومي/الأسبوعي)

عدد القطع المُسوَّدة يوميًا، القطع التي اجتازت فحص الجودة، القطع المعتمدة للنشر، والردود الواردة المحوّلة
إلى تشخيص. **لا تُقاس المتابعات (vanity).** التفاصيل في
[`14_GTM_METRICS_AND_LEARNING_AR.md`](14_GTM_METRICS_AND_LEARNING_AR.md): أفضل قطاع/عرض/عنوان/CTA يُشتقّ
جزئيًا من أداء المحتوى.

---

## 7. اللاءات المطبَّقة هنا

- لا نشر تلقائي. النشر إجراء خارجي بموافقة المؤسس.
- لا أتمتة LinkedIn، ولا scraping، ولا أي تواصل بارد عبر المحتوى.
- لا أسماء عملاء بلا إذن نشر موقّع. لا أرقام غير مُتحقَّقة. لا ضمان نتائج.
- دراسة الحالة بلا عميل مُسمّى تُوسَم "افتراضي/آمن (case-safe)".

---

## EN summary

Content Production OS is component #12: an inbound trust channel, not a cold-push channel. Daily output
is four drafted pieces (one founder insight, one sector-pain post, one proof/learning post, one short
case-style post). Weekly output is five deeper pieces (one long LinkedIn post, one carousel script, one
case-study draft, one product explainer, one founder lesson). Every piece must bind six mandatory
elements: sector + pain + workflow + proof + offer + CTA; a piece missing any element is rejected in
review and rewritten. The CTA always leads to an inbound reply handled in `09_REPLY_HANDLING_OS_AR.md`,
never to cold outreach. All content is drafted for founder approval; nothing is auto-posted, and
publishing (including LinkedIn) is an external action that requires founder sign-off. No client names
without signed publish permission, no unverified numbers (Client-Confirmed only, else "case-safe"), no
guaranteed outcomes, no emojis, no model name. The layer reuses `gtm_os/content_calendar.py`,
`dealix/marketing_factory/`, and the existing `docs/content/` cadence (3 posts/week, 3 lanes) rather
than duplicating it. Measurement counts inbound replies that convert, not follower vanity. Core rule
holds: 250 drafts/day, 0 auto-sends.

---

القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.
