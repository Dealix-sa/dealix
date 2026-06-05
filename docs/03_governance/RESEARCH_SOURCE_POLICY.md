# Research Source Policy — سياسة مصادر البحث

> طبقة: Governance OS · يفرضها: `scripts/targeting_compliance_gate.py` + `data/targeting/blocked_sources.yml`

## الدور

تحدد ما يحق لـ **Dealix Market Intelligence & Targeting OS** أن يستخدمه كمصدر
دليل، وما يُرفض رفضًا قاطعًا. القاعدة: **كل ادعاء يحتاج دليلًا من مصدر مسموح**،
وأي شركة دليلها الوحيد من مصدر ممنوع تُرفض ولا تدخل قائمة الاستهداف.

## أ. مصادر عالية الثقة (مسموحة)

| المصدر | الاستخدام |
|---|---|
| الموقع الرسمي للشركة | تعريف، خدمات، تواصل، proof |
| صفحة الخدمات | تحديد الألم والعرض المناسب |
| صفحة case studies / العملاء | قوة أو ضعف الإثبات |
| صفحة الوظائف | إشارة نمو/توسع |
| صفحة الأخبار/blog | توقيت وintent |
| صفحة التواصل الرسمية | قناة رسمية فقط |
| LinkedIn يدويًا | **تحقق بشري فقط** — بدون أي automation |
| ملفات seed من المؤسس | أعلى أولوية |

## ب. مصادر عامة مسموحة (بحذر)

- Google Programmable Search JSON API أو بدائلها — discovery فقط، **provider قابل للاستبدال** (الخدمة مغلقة للعملاء الجدد ولها مسار انتقال حتى 2027؛ لا نعتمد عليها اعتمادًا دائمًا).
- Saudi Open Data — إشارات قطاعية عامة.
- أدلة الفعاليات والغرف والمعارض العامة — اكتشاف شركات نشطة.
- مواقع المناقصات/الأخبار العامة — إشارات توسع.

## ج. مصادر ممنوعة (Reject)

| المصدر | الحكم |
|---|---|
| scraping عميق / خلف login | ❌ |
| LinkedIn automation | ❌ |
| أرقام جوالات شخصية | ❌ |
| قواعد بيانات مسربة | ❌ |
| CAPTCHA bypass | ❌ |
| mass WhatsApp / mass email | ❌ |
| قوائم PII مشتراة | ❌ |

هذه المصادر مُرمّزة في [`data/targeting/blocked_sources.yml`](../../data/targeting/blocked_sources.yml)
ويفرضها `gate_company()` آليًا: أي `source_type` ممنوع أو دومين محظور ⇒ **reject**.

## القاعدة الذهبية

> نبحث بكثافة، نفلتر بصرامة، نرسل بقلة، ونوثّق كل ادعاء بدليل.

كل شركة تحتاج **دليلين مستقلين على الأقل** من مصادر مسموحة قبل أن تتأهل لأي مسودة.

## روابط

- [Robots & Terms Policy](ROBOTS_AND_TERMS_POLICY.md)
- [Outreach Approval Policy](OUTREACH_APPROVAL_POLICY.md)
- [No-Spam Policy](NO_SPAM_POLICY.md)
- دستور: [docs/00_constitution/NON_NEGOTIABLES.md](../00_constitution/NON_NEGOTIABLES.md)
