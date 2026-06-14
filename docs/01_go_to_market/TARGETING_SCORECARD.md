# Targeting Scorecard — بطاقة تقييم الاستهداف — The Scoring Rubric

## دور هذه الوثيقة

تُحوّل "حدس المؤسس" إلى **رقم قابل للتدقيق**. كل مرشّح يُقيَّم على 100، وله بوّابة تأهّل واضحة. لا مرشّح يدخل القُمع بلا دليل.

> الرقم لا يستبدل المؤسس — يُرتّب له اليوم. التقييم بوّابة، لا قرار نهائي.

## أبعاد التقييم — Scoring Dimensions (مجموع = 100)

| البُعد — Dimension | الوزن — Weight | ما يقيس |
|---|---|---|
| ICP fit — ملاءمة العميل المثالي | 25 | القطاع، الحجم، النضج التشغيلي |
| Evidence of operating pain — دليل ألم تشغيلي | 25 | ألم مرئي موثّق بمصدر، لا مُفترَض |
| Decision speed — سرعة القرار | 15 | هل يوجد صاحب قرار واضح وسريع |
| Deal size potential — حجم الصفقة المحتمل | 15 | قدرة على الترقّي إلى Managed OS |
| Partnership potential — احتمال الشراكة | 10 | باب لإحالات أو شراكة قناة |
| Reachability without spam — إمكانية الوصول بلا إزعاج | 10 | قناة شرعية، علاقة أو مصدر علني |
| **المجموع** | **100** | |

## بوّابة التأهّل — Qualification Gate

مرشّح يصبح **Qualified** إذا:

- **score ≥ 80**، **أو**
- **warm intro** (تعريف دافئ من علاقة موثوقة).

أقل من 80 وبلا تعريف دافئ = يبقى في Research، لا يتقدّم. لا استثناءات بلا تسجيل سبب.

## الحقول لكل مرشّح — Data Fields per Candidate

| الحقل — Field | الوصف |
|---|---|
| `company` | اسم الشركة |
| `sector` | القطاع |
| `evidence_source` | مصدر الدليل العلني المسموح (إلزامي) |
| `pain_signal` | الألم التشغيلي الموثّق |
| `angle` | زاوية الاستهداف المبنية على الألم |
| `score` | التقييم 0–100 |
| `status` | Research / Qualified / Reviewed / Draft Ready |

## مثال محسوب — Worked Example

| Field | Value |
|---|---|
| `company` | معرض سيارات (قطاع تجزئة، مجهول الهوية) |
| `sector` | Automotive retail |
| `evidence_source` | موقع الشركة العلني + إعلان وظيفة "مسؤول متابعة عملاء" منشور |
| `pain_signal` | تأخّر متابعة العملاء المحتملين — دليل من إعلان التوظيف ومراجعات علنية |
| `angle` | "خريطة إيراد تكشف أين يتسرّب العميل المحتمل قبل الإغلاق" |
| `score` | 84 (ICP 22 + pain 24 + speed 12 + size 12 + partner 6 + reach 8) |
| `status` | Qualified → Draft Ready |

## قواعد لا-إزعاج / الدليل إلزامي — No-Spam / Evidence-Required Rules

- **لا مسودّة بلا `evidence_source`.** الدليل شرط دخول، لا تحسين لاحق.
- **الدليل من مصادر علنية مسموحة فقط** — لا scraping خلف تسجيل دخول، احترام `robots.txt` وشروط المصدر.
- **لا إرسال جماعي، لا واتساب بارد.** كل وصول شرعي ومُوافَق عليه.
- **التقييم لا يُلغي الموافقة البشرية** — score 100 لا يعني إرسالًا تلقائيًا.

## روابط مرجعية — Cross-links

- [MARKET_INTELLIGENCE_OS.md](MARKET_INTELLIGENCE_OS.md)
- [SALES_PLAYBOOK.md](SALES_PLAYBOOK.md)
- [../05_governance_os/APPROVAL_POLICY.md](../05_governance_os/APPROVAL_POLICY.md)

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
