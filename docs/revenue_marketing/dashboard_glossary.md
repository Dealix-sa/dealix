## قاموس مقاييس لوحة التحكم — Dashboard Glossary (AR)

كل مقياس على لوحة Revenue Marketing Dashboard له تعريف واحد شفّاف. لا "مقاييس ذكية" بلا معادلة. لا مقياس يُعرض بدون قيمة سيّئة معروفة وخطوة علاج مُحدَّدة. هذا القاموس مرجعي ومُلزم — أي إضافة مقياس جديد تمرّ بمراجعة.

### الجدول الكامل

| المقياس (EN) | الاسم العربي | التعريف | المعادلة / المصدر | لماذا يهمّ | قيمة سيّئة | علاج |
|------------|--------------|---------|-------------------|-------------|------------|------|
| `top_campaigns_by_revenue` | أعلى الحملات بالإيراد | ترتيب الحملات من الأعلى إيراداً للأدنى خلال نافذة زمنية | `SUM(revenue) GROUP BY campaign_id ORDER BY DESC` | يكشف الحملات التي تستحق التوسيع وتلك المرشّحة للإلغاء | حملة واحدة تجمع > 70% من الإيراد (تركّز خطر) | تنويع المحفظة، اختبار حملتين جديدتين |
| `cost_per_lead` (CPL) | تكلفة الـ Lead | تكلفة الإنتاج / عدد الـ leads المؤهّلة | `total_cost / qualified_leads_count` | يقيس كفاءة قناة الجذب | CPL > 3x المتوسط القطاعي لقطاع B2B السعودي | مراجعة القناة، تشديد معايير التأهيل |
| `money_quality_score` (MQS) | درجة جودة الإيراد | درجة موزونة على إيراد محقّق + احتفاظ + هامش + توسيع | معادلة موزونة في `dealix/revenue_marketing/scoring.py` | يميّز إيراداً صحياً من إيراد هشّ | MQS < 50 على 100 | مراجعة العقود قصيرة الأمد، تعزيز الاحتفاظ |
| `attribution_chain` | سلسلة الإحالة | تتبّع كل صفقة من أول لمسة إلى الإغلاق، بمعرّفات المحتوى | `events` table + first-touch / last-touch / multi-touch | يربط المحتوى بالإيراد فعلياً | > 30% من الصفقات بلا lineage موثَّق | تشديد تتبّع UTM، إغلاق قنوات بلا قياس |
| `lead_to_deal_rate` | معدّل تحويل Lead → صفقة | عدد الصفقات / عدد الـ leads المؤهّلة | `deals_count / qualified_leads_count` | يقيس صحة عملية المبيعات | < 5% لقمع B2B Saudi | مراجعة عملية المبيعات، تدريب فريق، تعديل ICP |
| `pilot_to_core_rate` | معدّل تحويل Pilot → Core | عدد عملاء Core الذين بدأوا بـ Pilot / إجمالي Pilot | `core_from_pilot / total_pilots` | يقيس نجاح سلّم العروض | < 20% | مراجعة تجربة Pilot، تعزيز handover |
| `monthly_recurring_revenue` (MRR) | الإيراد الشهري المتكرّر | إجمالي الإيراد الشهري من اشتراكات نشطة | `SUM(active_subscriptions * monthly_price)` | المؤشر الأساسي لصحة الشركة | انخفاض شهري > 5% بلا تفسير | مراجعة churn، استدعاء عملاء "في خطر" |
| `churn_rate` | معدّل التسرّب | عملاء مغادرون / إجمالي عملاء بداية الشهر | `churned / start_count` | يكشف عيوب التسليم | > 8% شهرياً | مراجعة سبب التسرّب، تحسين onboarding |
| `expansion_rate` | معدّل التوسيع | عملاء وسّعوا اشتراكهم / إجمالي عملاء | `expanded / total` | يقيس قدرة التسليم على إنتاج قيمة إضافية | < 10% سنوياً | إضافة Offer Expansion، تدريب Account Manager |
| `partner_sourced_revenue` | إيراد الشركاء | إيراد العملاء النهائيين الذين جلبهم الشركاء | `SUM(revenue WHERE source = partner)` | يقيس نضج قناة الشركاء | < 20% من الإيراد بعد 12 شهر | مراجعة Partner Kit، تجنيد شركاء أكثر |
| `evidence_pack_coverage` | تغطية حزمة الأدلة | الصفقات التي لها سجل أدلة كامل / كل الصفقات | `with_evidence / total_deals` | يقيس التزام الحوكمة الداخلية | < 80% | إضافة validation قبل الإغلاق |
| `fit_score_avg` | متوسط درجة الـ Fit | متوسط Fit Score للفرص المُسلَّمة | `AVG(fit_score) GROUP BY pilot_id` | يكشف انجراف جودة الاستهداف | < 65 | إعادة تدريب الـ scoring weights |
| `time_to_pilot_delivery` | وقت تسليم الـ Pilot | أيام بين الدفع وتسليم الـ 10 فرص | `delivery_date - payment_date` | يقيس انضباط التسليم | > 9 أيام | فحص عمليات Production، إعادة ترتيب أولويات |
| `kill_decisions_per_quarter` | قرارات الإلغاء/الربع | عدد الحملات/العروض التي أُلغيت | `COUNT(killed) WHERE quarter = X` | يقيس صحة قرارات Scale/Kill | = 0 (تشير لعدم تطبيق القاعدة) | فرض مراجعة شهرية صارمة |
| `vanity_signals_blocked` | إشارات الزينة المحجوبة | عدد المحاولات لاحتساب مقياس زينة وحده | `COUNT(vanity_block_events)` | يقيس انضباط Anti-vanity | كل إشارة محجوبة تُسجَّل وتُراجَع | تدريب الفريق على القاعدة |
| `consent_status_named_pct` | نسبة الحالات المُسمّاة بإذن | حالات بإذن خطّي / كل الحالات | `named / total_cases` | يقيس مصداقية القصص | < 20% (يدلّ على قصص "آمنة" بلا قصص مُسمّاة) | حملة جمع consent من عملاء راضين |

### قواعد عرض المقاييس

- كل مقياس يُعرض مع: قيمته الحالية + خط الأساس + هدف الربع + اتجاه آخر 4 أسابيع.
- لا مقياس يُعرض وحده بلا "بجانبه" مقياس تحويل ≥ 1 (راجع `anti_vanity_rules.md`).
- التحديث: لوحة التحكم تُحدَّث يومياً عند منتصف الليل، تقرير ربعي شامل أوّل يوم من كل ربع.

---

## Dashboard Glossary (EN)

Every metric on the Revenue Marketing Dashboard has one transparent definition. No "smart metrics" without a formula. No metric shown without a known bad value and a defined remediation step. This glossary is binding — any new metric goes through review.

### Full Table

| Metric (EN) | Arabic Name | Definition | Formula / Source | Why It Matters | Bad Value | Remediation |
|-------------|-------------|------------|-------------------|----------------|-----------|-------------|
| `top_campaigns_by_revenue` | أعلى الحملات بالإيراد | Campaigns ranked by revenue within a window | `SUM(revenue) GROUP BY campaign_id ORDER BY DESC` | Reveals campaigns to scale and candidates to kill | One campaign captures > 70% of revenue (concentration risk) | Diversify portfolio, test two new campaigns |
| `cost_per_lead` (CPL) | تكلفة الـ Lead | Production cost / qualified leads | `total_cost / qualified_leads_count` | Measures channel acquisition efficiency | CPL > 3x Saudi B2B sector average | Channel review, tighter qualification |
| `money_quality_score` (MQS) | درجة جودة الإيراد | Weighted score on realized revenue + retention + margin + expansion | Weighted formula in `dealix/revenue_marketing/scoring.py` | Distinguishes healthy revenue from fragile revenue | MQS < 50 / 100 | Review short contracts, strengthen retention |
| `attribution_chain` | سلسلة الإحالة | Track each deal from first touch to close, with content IDs | `events` table + first/last/multi-touch | Ties content to actual revenue | > 30% of deals without documented lineage | Tighten UTM tracking, close untracked channels |
| `lead_to_deal_rate` | معدّل تحويل Lead → صفقة | Deals / qualified leads | `deals_count / qualified_leads_count` | Measures sales process health | < 5% for Saudi B2B funnel | Sales process review, team training, ICP adjustment |
| `pilot_to_core_rate` | معدّل تحويل Pilot → Core | Core customers starting from Pilot / total Pilots | `core_from_pilot / total_pilots` | Measures offer-ladder success | < 20% | Review pilot experience, strengthen handover |
| `monthly_recurring_revenue` (MRR) | الإيراد الشهري المتكرّر | Monthly revenue from active subscriptions | `SUM(active_subscriptions * monthly_price)` | Core company health signal | Monthly drop > 5% without explanation | Review churn, call at-risk customers |
| `churn_rate` | معدّل التسرّب | Customers lost / start-of-month customers | `churned / start_count` | Reveals delivery defects | > 8% monthly | Investigate churn cause, improve onboarding |
| `expansion_rate` | معدّل التوسيع | Customers who expanded / total customers | `expanded / total` | Measures delivery's ability to create extra value | < 10% annually | Add expansion offer, train Account Manager |
| `partner_sourced_revenue` | إيراد الشركاء | Revenue from partner-sourced end-customers | `SUM(revenue WHERE source = partner)` | Measures partner channel maturity | < 20% of revenue after 12 months | Review Partner Kit, recruit more partners |
| `evidence_pack_coverage` | تغطية حزمة الأدلة | Deals with a full evidence ledger / all deals | `with_evidence / total_deals` | Measures internal governance discipline | < 80% | Add validation before close |
| `fit_score_avg` | متوسط درجة الـ Fit | Average Fit Score on delivered opportunities | `AVG(fit_score) GROUP BY pilot_id` | Reveals targeting quality drift | < 65 | Retrain scoring weights |
| `time_to_pilot_delivery` | وقت تسليم الـ Pilot | Days between payment and 10-opportunity delivery | `delivery_date - payment_date` | Measures delivery discipline | > 9 days | Inspect production ops, re-prioritize |
| `kill_decisions_per_quarter` | قرارات الإلغاء/الربع | Campaigns/offers killed in the quarter | `COUNT(killed) WHERE quarter = X` | Health of Scale/Kill discipline | = 0 (signals rule isn't being applied) | Enforce strict monthly review |
| `vanity_signals_blocked` | إشارات الزينة المحجوبة | Attempts to count a vanity metric alone | `COUNT(vanity_block_events)` | Anti-vanity discipline | Every blocked signal is logged and reviewed | Team training on the rule |
| `consent_status_named_pct` | نسبة الحالات المُسمّاة بإذن | Cases with written consent / all cases | `named / total_cases` | Story credibility | < 20% (suggests "safe" cases without named ones) | Consent collection campaign with happy customers |

### Display Rules

- Every metric shows: current value + baseline + quarter target + last-4-week trend.
- No metric is displayed alone without a paired downstream conversion ≥ 1 (see `anti_vanity_rules.md`).
- Refresh: dashboard updates daily at midnight; a comprehensive quarterly report runs on day 1 of every quarter.

---

**Disclosure / إفصاح:** Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.

Cross-links: `docs/revenue_marketing/anti_vanity_rules.md`, `docs/revenue_marketing/case_study_template.md`, `dealix/revenue_marketing/scoring.py` (engineer-owned).
