# 14 — مقاييس GTM والتعلّم — GTM Metrics & Learning

> الموقع في الطبقة: المكوّن رقم 18 من *Market Production OS* (حلقة المقاييس والتعلّم) + تعيين تبويبات
> *Founder GTM Control Room*. العمود الفقري: [`00_MARKET_PRODUCTION_OS_MASTER_AR.md`](00_MARKET_PRODUCTION_OS_MASTER_AR.md).

هذا المستند يحدّد ما نقيسه يوميًا وأسبوعيًا، وكيف يتحوّل القياس إلى تعلّم وتجارب الأسبوع القادم. الأرقام
**أهداف داخلية قابلة للمعايرة، وليست وعودًا للعميل**، تمامًا كما في
[`NORTH_STAR_METRICS_AR.md`](../commercial/NORTH_STAR_METRICS_AR.md). المقاييس تُصدَر من تقرير GTM
اليومي/الأسبوعي، وتُقرأ في غرفة تحكّم المؤسس، ولا تُستخدم لتبرير أي إرسال تلقائي.

> القاعدة الأساسية: **نقيس لنتعلّم ونحسّن الجودة، لا لنزيد الإرسال بلا حوكمة.** 250 مسودة/يوم، صفر إرسال تلقائي.

---

## 0. المبدأ الحاكم لطبقة القياس

- لا رقم بلا مصدر. لا ادعاء إيراد بلا دفع مؤكَّد (`payment_confirmed`).
- لا قياس متابعين أو أرقام مظهرية (vanity). نقيس التحويل الوارد والجودة.
- لا PII في المقاييس — أرقام مجمّعة وأنماط فقط.
- ارتفاع `unsubscribe`/`angry`/`bounce` = إشارة لمراجعة الاستهداف، لا لرفع سقف الإرسال.

---

## 1. المقاييس اليومية (Daily Metrics)

تُصدَر في **تقرير GTM اليومي** (المخرج الإلزامي السابع، انظر [العمود الفقري §6](00_MARKET_PRODUCTION_OS_MASTER_AR.md)):

| # | المقياس | التعريف | الطبقة المصدر |
|---|---|---|---|
| 1 | drafts_generated | إجمالي المسودات المُولَّدة (هدف 250) | Draft Factory (`06`) |
| 2 | drafts_quality_passed | اجتازت بوابة الجودة والامتثال | Quality Gate (`07`) |
| 3 | drafts_approved | اعتمدها المؤسس للإرسال | Approval Queue (`08`) |
| 4 | emails_sent | أُرسلت فعليًا (ضمن سقف الأسبوع) | Sending Ramp (`08`) |
| 5 | bounces | فشل تسليم (hard/soft) | Reply Handling (`09`) |
| 6 | unsubscribes | طلبات إزالة (كبح فوري) | Reply Handling (`09`) |
| 7 | replies | إجمالي الردود الواردة | Reply Handling (`09`) |
| 8 | positive_replies | ردود مُصنَّفة `positive` | Reply Handling (`09`) |
| 9 | meetings_booked | اجتماعات/جلسات اكتشاف مُجدوَلة | WhatsApp Post-Reply (`10`) |
| 10 | proposals_requested | طلبات عرض/تسعير | Reply Handling (`09`) |
| 11 | job_signals_found | إشارات وظيفية/شراء مكتشَفة | Signal Detection (`05`) |
| 12 | content_posts_drafted | قطع محتوى مُسوَّدة | Content (`11`) |
| 13 | partner_prospects_found | شركاء محتملون مكتشَفون | Partnerships (`13`) |

> القمع اليومي: drafts_generated → quality_passed → approved → sent → replies → positive_replies →
> meetings_booked → proposals_requested. كل انتقال يُظهر فقدًا، والفقد يُقرأ كتعلّم لا كفشل.

---

## 2. المراجعة الأسبوعية (Weekly Review)

تُصدَر في **التقرير الأسبوعي** وتُغذّي تجارب الأسبوع القادم:

| البُعد | السؤال | الاستخدام |
|---|---|---|
| best_sector | أي قطاع أعطى أعلى positive_replies؟ | يوجّه استهداف الأسبوع القادم |
| best_offer | أي درجة من السلّم حقّقت أعلى تحويل؟ | يوجّه بطاقة العرض |
| best_subject_line | أي عنوان حقّق أعلى ردود؟ | يُعاد استخدامه/يُختبر |
| best_cta | أي دعوة حقّقت أعلى تفاعل وارد؟ | يوحّد CTA المحتوى والبريد |
| best_signal_source | أي مصدر إشارة جلب أفضل الفرص؟ | يُضاعف الجهد عليه |
| worst_bounce_source | أي مصدر أعطى أعلى bounce؟ | يُكبَح/يُراجَع، لا يُرسَل له |
| pipeline_value | قيمة الأنبوب التقديرية | تقديري، بلا ادعاء إيراد |
| lessons | ماذا تعلّمنا (نجاح/احتكاك)؟ | يدخل سجل الأصول |
| next_week_experiments | ماذا نختبر الأسبوع القادم؟ | تجربة واحدة لكل بُعد |

> هذه الأبعاد تطابق المراجعة الأسبوعية في [العمود الفقري §6](00_MARKET_PRODUCTION_OS_MASTER_AR.md):
> أفضل قطاع · أفضل عرض · أفضل subject · أفضل CTA · أفضل مصدر إشارة · أسوأ مصدر bounce · تجارب الأسبوع القادم.

---

## 3. الربط بمقاييس North Star

هذه المقاييس **تشغيلية يومية** وتتغذّى منها محاور North Star الأعمق دون تكرارها:

| محور North Star | المقياس اليومي/الأسبوعي المغذّي | المرجع |
|---|---|---|
| Revenue (تحويل Sprint→Retainer) | proposals_requested · pipeline_value | [`NORTH_STAR_METRICS_AR.md`](../commercial/NORTH_STAR_METRICS_AR.md) |
| Customer (زمن الرد المسودّة) | replies · positive_replies | المرجع نفسه |
| Governance (موافقات مسجّلة) | drafts_approved (100% من المُرسَل) | المرجع نفسه |
| Governance (حوادث PII) | 0 دائمًا | المرجع نفسه |
| Sales (معدل الإغلاق) | proposals_requested → مدفوعات | المرجع نفسه |

> أعد الاستخدام قبل أن تكتب: North Star هو مصدر الحقيقة للأهداف طويلة المدى. هذا المستند = **المقاييس
> التشغيلية اليومية التي تُغذّيه**.

---

## 4. مصدر الإصدار وإعادة الاستخدام (Reuse)

- التقرير اليومي/الأسبوعي يُصدَر من `auto_client_acquisition/market_production_os/report.py`
  (Daily/Weekly GTM report) — قيد البناء من قِبل المؤسس.
- حلقة التعلّم الأسبوعية تعيد استخدام `auto_client_acquisition/revenue_os/learning_weekly.py`.
- العرض في غرفة تحكّم المؤسس عبر الواجهات الموجودة `/[locale]/ops/founder` و `/ops/marketing` و
  `/ops/approvals` — **لا واجهة جديدة**، فقط تعيين تبويبات (المكوّن 17).
- مصدر مقاييس الفئات: [`09_REPLY_HANDLING_OS_AR.md`](09_REPLY_HANDLING_OS_AR.md) ·
  [`11_CONTENT_PRODUCTION_OS_AR.md`](11_CONTENT_PRODUCTION_OS_AR.md) ·
  [`13_PARTNERSHIPS_OS_AR.md`](13_PARTNERSHIPS_OS_AR.md).

---

## 5. حلقة التعلّم (Learning Loop)

```txt
قياس يومي (report.py)
→ مراجعة أسبوعية (best/worst لكل بُعد)
→ درس مُسجَّل (يدخل سجل الأصول)
→ تجربة واحدة لكل بُعد للأسبوع القادم
→ قياس أثر التجربة الأسبوع التالي
```

التجارب تغيّر **الجودة والاستهداف والرسالة** — لا ترفع سقف الإرسال بلا صحة دومين. أي تحسّن مظهري على
حساب الثقة يُرفض في المراجعة.

---

## 6. اللاءات المطبَّقة هنا

- لا رقم بلا مصدر. لا ادعاء إيراد بلا دفع مؤكَّد. لا قياس vanity.
- لا PII في المقاييس — أرقام مجمّعة وأنماط فقط.
- لا استخدام المقاييس لتبرير إرسال تلقائي. القاعدة ثابتة: 250 مسودة/يوم، صفر إرسال تلقائي.

---

## EN summary

GTM Metrics & Learning is component #18 plus the Founder GTM Control Room tab mapping. Daily metrics
(emitted by `market_production_os/report.py`, the Daily/Weekly GTM report under construction) are:
drafts generated, drafts quality-passed, drafts approved, emails sent, bounces, unsubscribes, replies,
positive replies, meetings booked, proposals requested, job signals found, content posts drafted, and
partner prospects found — forming a daily funnel read as learning, not failure. The weekly review
surfaces best sector, best offer, best subject line, best CTA, best signal source, worst bounce source,
pipeline value (estimated, never a revenue claim), lessons (logged into the capital ledger), and one
next-week experiment per dimension. These operational metrics feed the deeper North Star axes
(`NORTH_STAR_METRICS_AR.md`) without duplicating them, and are displayed in the existing `/ops/*`
control-room screens — no new UI, only tab mapping. The learning loop reuses
`revenue_os/learning_weekly.py`. Numbers are calibratable internal targets, not customer promises: no
number without a source, no revenue claim without payment confirmed, no vanity metrics, no PII
(aggregated patterns only). Metrics are never used to justify automated sending; rising
unsubscribe/angry/bounce signals trigger targeting review, not a higher send cap. Core rule holds: 250
drafts/day, 0 auto-sends.

---

القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.
