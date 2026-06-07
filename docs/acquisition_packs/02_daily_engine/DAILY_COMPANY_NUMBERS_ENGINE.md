# Daily Company Numbers Engine — محرك أرقام الشركات اليومي

محرك يومي ضمن حزم اكتساب العملاء (Client Acquisition Packs). الهدف التشغيلي واحد: تحويل سوق غير منظَّم إلى قائمة شركات مؤهَّلة بأرقام قابلة للمراجعة، مع مسودة مخصَّصة لكل شركة تنتظر موافقة بشرية قبل أي إرسال. لا انطباعات ولا أرقام مضمونة — فقط أرقام مُسجَّلة قابلة للتدقيق.

روابط ذات صلة: [../04_marketer_enablement/MARKETER_FIELD_MANUAL.md](../04_marketer_enablement/MARKETER_FIELD_MANUAL.md) · [../05_outreach/OUTREACH_SCRIPTS.md](../05_outreach/OUTREACH_SCRIPTS.md) · [../03_offers/OFFER_PACKAGES.md](../03_offers/OFFER_PACKAGES.md) · [../10_compliance/COMPLIANCE_PACK.md](../10_compliance/COMPLIANCE_PACK.md) · [../07_operating_cadence/DAILY_OPERATING_CADENCE.md](../07_operating_cadence/DAILY_OPERATING_CADENCE.md) · المرجع التجاري: [../../commercial/DEALIX_REVOPS_PACKAGES_AR.md](../../commercial/DEALIX_REVOPS_PACKAGES_AR.md) · الامتثال: [../../commercial/FOUNDER_PDPL_COMPLIANCE_PASS_AR.md](../../commercial/FOUNDER_PDPL_COMPLIANCE_PASS_AR.md)

---

## الغرض

تشغيل قطاع واحد كل يوم بنظام ثابت: نبحث عن الشركات من مصادر عامة مسموح بها، نُقيّمها بمنطق واحد، نحدد فجوة الإيراد لكل شركة، ونُجهّز مسودة مخصَّصة لكل شركة مؤهَّلة. الناتج اليومي أرقام ثابتة تُسجَّل في القوالب لا انطباعات شخصية. كل قيمة سعرية مذكورة تقديرية وليست متحقَّقة، وأي رقم تحويل أو إغلاق يُعرض كنمط آمن للحالة لا كوعد. تركيز المحرك على الانضباط: نفس الخطوات، نفس الأعمدة، نفس معايير التأهيل كل يوم، حتى تصبح المقارنة بين القطاعات عادلة وقابلة للقياس.

## ما هو المحرك — وما ليس هو

هو: بحث يدوي منظَّم من مصادر عامة مسموح بها، تقييم بمنطق ثابت قابل للتكرار، وإعداد مسودة لكل شركة تُحال إلى مراجعة بشرية قبل أي تواصل خارجي.

ليس هو: ليس كشطاً (scraping) لأي موقع أو منصة، وليس قوائم مشتراة، وليس إرسالاً بارداً أو جماعياً أو مؤتمتاً. لا أتمتة واتساب، لا أتمتة لينكدإن، لا إرسال مجمَّع. الكشط والقوائم المشتراة ممنوعة صراحةً وفق `source_registry` / `forbidden_sources`. أي مصدر غير مُدرَج في سجل المصادر المسموح بها لا يُستخدَم، وإن وُجد صف بمصدر غير مسموح يُحذَف الصف.

## المدخلات (أنواع المصادر المسموح بها فقط)

- السجلات التجارية العامة والإعلانات الرسمية المنشورة.
- الإعلانات العامة للشركات: توسّع، فرع جديد، إعلان توظيف منشور، جولة تمويل معلَنة، عقد عام.
- إشارات السوق التي يزوّدنا بها المؤسس مباشرةً.

كل صف يحمل `source_type` يوثّق المصدر العام الذي خرجت منه الشركة، و`consent_basis` = `legitimate_interest_b2b`. نخزّن جهة اتصال أعمال فقط (دور وظيفي وقناة عمل عامة)، بلا أي بيانات شخصية: لا بريد شخصي، لا رقم جوال شخصي، لا هوية وطنية، لا أسماء أفراد في الأمثلة. الأمثلة تستخدم نائباً مثل «Example Trading Co».

## التدفّق اليومي (الهدف المعياري)

قطاع واحد/اليوم بالأرقام: ~50 شركة تُحلَّل ← ~15 مؤهَّلة ← ~10 مسودات مخصَّصة تُجهَّز ← تقرير نهاية اليوم. النسب أهداف تشغيلية لا ضمانات، وتُعدَّل حسب نضج القطاع.

1. اختيار القطاع والمنطقة لليوم وتثبيتهما في عمود `sector` و`region`.
2. سرد الشركات من المصادر المسموح بها فقط، صف واحد لكل شركة.
3. تقييم كل شركة وتسجيلها في `company_scoring_template.csv` مع `fit_score` و`intent_score` و`total_score`.
4. تحديد المؤهَّلين، صياغة `gap_identified` و`pain_hypothesis` و`recommended_offer`، وإعداد مسودة لكل مؤهَّل.
5. تسليم المسودات لصندوق الموافقات، ثم تسجيل الأرقام اليومية في `daily_numbers_template.csv`.

## نموذج التقييم

المعادلة الأساسية: `total_score = fit_score + intent_score`. الرقمان يُسجَّلان لكل شركة حتى يكون التأهيل قابلاً للمراجعة لا حدسياً.

- `fit_score`: مدى ملاءمة الشركة لعرضنا — الحجم (`size_band`)، القطاع، المنطقة، ومدى وضوح الحاجة المتوقَّعة.
- `intent_score`: قوة إشارة «لماذا الآن» — كلما كان الحدث العام أحدث وأوضح ارتفعت القيمة.
- `why_now_signal`: حدث عام حديث يدل على حركة في الشركة (فرع جديد، توسّع، إعلان توظيف، عقد جديد). بلا إشارة واضحة يصعب التأهيل.
- `gap_identified`: الفجوة التشغيلية في الإيراد كما نقرؤها من الإشارات العامة (مثال: لا خط أنابيب منظَّم، متابعة يدوية بطيئة، عملاء محتملون يضيعون بلا تتبّع). الفجوة هي ما يربط الشركة بالعرض المناسب.
- `pain_hypothesis`: فرضية الألم — قراءة مبدئية تُختبَر في التواصل، لا تُعرض كحقيقة.

## كيف تصبح الشركة عميلاً مؤهَّلاً

`status` تنتقل عبر مسار واحد: `new → qualified → contacted → replied → meeting → proposal → won/lost`. الشركة تنتقل من `new` إلى `qualified` عندما تجتمع أربعة شروط: `total_score` كافٍ مقارنةً بحد القطاع، `why_now_signal` واضح وحديث، `gap_identified` ملموس وقابل للوصف، و`recommended_offer` مناسب من حزمة العروض. التأهيل قرار مُعلَّل يُسجَّل في `notes`، لا انطباع.

## التسليم لمسودات التواصل

كل مسودة لشركة مؤهَّلة تُكتب مخصَّصة (الفجوة + العرض المقترح) وتذهب لصندوق الموافقات. لا إرسال خارجي دون موافقة بشرية صريحة — `NO_LIVE_SEND` قاعدة ثابتة. ما يُوافَق عليه يُرسَل يدوياً، ويُسجَّل في `messages_sent_approved` ضمن أرقام اليوم. السكربتات المعتمدة في [../05_outreach/OUTREACH_SCRIPTS.md](../05_outreach/OUTREACH_SCRIPTS.md)، والعروض في [../03_offers/OFFER_PACKAGES.md](../03_offers/OFFER_PACKAGES.md).

## أين تُسجَّل الأرقام

- صف لكل شركة: [../09_dashboards/company_scoring_template.csv](../09_dashboards/company_scoring_template.csv).
- المؤهَّلون ينتقلون إلى [../09_dashboards/pipeline_template.csv](../09_dashboards/pipeline_template.csv).
- الإجماليات اليومية في [../09_dashboards/daily_numbers_template.csv](../09_dashboards/daily_numbers_template.csv).

أعمدة `company_scoring_template.csv`: `company_name, sector, region, size_band, source_type, why_now_signal, pain_hypothesis, fit_score, intent_score, total_score, recommended_offer, gap_identified, consent_basis, owner, status, next_action, next_action_date, notes`.

---

# Daily Company Numbers Engine

A daily engine inside the Client Acquisition Packs. One operating goal: turn an unstructured market into a list of qualified companies with reviewable numbers, plus one tailored draft per company awaiting human approval before any send. No impressions, no guaranteed figures — only recorded, auditable numbers.

Related: [../04_marketer_enablement/MARKETER_FIELD_MANUAL.md](../04_marketer_enablement/MARKETER_FIELD_MANUAL.md) · [../05_outreach/OUTREACH_SCRIPTS.md](../05_outreach/OUTREACH_SCRIPTS.md) · [../03_offers/OFFER_PACKAGES.md](../03_offers/OFFER_PACKAGES.md) · [../10_compliance/COMPLIANCE_PACK.md](../10_compliance/COMPLIANCE_PACK.md) · [../07_operating_cadence/DAILY_OPERATING_CADENCE.md](../07_operating_cadence/DAILY_OPERATING_CADENCE.md) · Commercial reference: [../../commercial/DEALIX_REVOPS_PACKAGES_AR.md](../../commercial/DEALIX_REVOPS_PACKAGES_AR.md) · Compliance: [../../commercial/FOUNDER_PDPL_COMPLIANCE_PASS_AR.md](../../commercial/FOUNDER_PDPL_COMPLIANCE_PASS_AR.md)

---

## Purpose

Run one sector per day on a fixed system: source companies from allowed public sources, score them with one logic, identify the revenue gap per company, and prepare a tailored draft for each qualified company. The daily output is a fixed set of numbers recorded in the templates, not personal impressions. Every price value stated is estimated, not verified; any conversion or close figure is presented as a case-safe pattern, not a promise. The engine's focus is discipline: the same steps, the same columns, and the same qualification criteria every day, so that comparing sectors stays fair and measurable.

## What it is — and what it is NOT

It is: structured manual research from allowed public sources, scoring with fixed and repeatable logic, and a per-company draft routed to human review before any external contact.

It is NOT: scraping of any site or platform, purchased lists, or cold, bulk, or automated outreach. No WhatsApp automation, no LinkedIn automation, no bulk sending. Scraping and purchased lists are explicitly forbidden per `source_registry` / `forbidden_sources`. Any source not listed in the allowed source registry is not used, and if a row carries a disallowed source, the row is removed.

## Inputs (allowed source types only)

- Public business registries and published official announcements.
- Public company announcements: expansion, new branch, published hiring notice, announced funding round, public contract.
- Market signals supplied directly by the founder.

Each row carries a `source_type` documenting the public source the company came from, and `consent_basis` = `legitimate_interest_b2b`. We store a business contact only (a job role and a public business channel), with no personal data: no personal email, no personal mobile number, no national ID, no individual names in examples. Examples use a placeholder such as "Example Trading Co".

## The daily flow (canonical target)

One sector/day, by the numbers: ~50 companies analyzed → ~15 qualified → ~10 tailored drafts prepared → end-of-day report. The ratios are operating targets, not guarantees, and they adjust with sector maturity.

1. Select the day's sector and region and fix them in the `sector` and `region` columns.
2. List companies from allowed sources only, one row per company.
3. Score each company and record it in `company_scoring_template.csv` with `fit_score`, `intent_score`, and `total_score`.
4. Identify the qualified set, write `gap_identified`, `pain_hypothesis`, and `recommended_offer`, and prepare a draft for each.
5. Hand drafts to the approval inbox, then log the day's totals in `daily_numbers_template.csv`.

## Scoring model

Core formula: `total_score = fit_score + intent_score`. Both numbers are recorded per company so qualification stays reviewable, not intuitive.

- `fit_score`: how well the company fits our offer — size (`size_band`), sector, region, and how clear the expected need is.
- `intent_score`: strength of the "why now" signal — the more recent and clear the public event, the higher the value.
- `why_now_signal`: a recent public event showing movement (new branch, expansion, published hiring notice, new contract). Without a clear signal, qualification is hard.
- `gap_identified`: the operating revenue gap as read from public signals (e.g. no structured pipeline, slow manual follow-up, prospects lost without tracking). The gap is what links the company to the right offer.
- `pain_hypothesis`: a working hypothesis tested during outreach, never presented as fact.

## How a company becomes a qualified lead

`status` moves along one path: `new → qualified → contacted → replied → meeting → proposal → won/lost`. A company moves from `new` to `qualified` when four conditions meet: a sufficient `total_score` against the sector threshold, a clear and recent `why_now_signal`, a concrete and describable `gap_identified`, and a fitting `recommended_offer` from the offer set. Qualification is a reasoned decision recorded in `notes`, not an impression.

## Handoff to outreach drafts

Every draft for a qualified company is written tailored (the gap + the proposed offer) and routed to the approval inbox. No external send without explicit human approval — `NO_LIVE_SEND` is a fixed rule. What is approved is sent manually and logged in `messages_sent_approved` within the day's numbers. Approved scripts live in [../05_outreach/OUTREACH_SCRIPTS.md](../05_outreach/OUTREACH_SCRIPTS.md), and offers in [../03_offers/OFFER_PACKAGES.md](../03_offers/OFFER_PACKAGES.md).

## Where the numbers are recorded

- One row per company: [../09_dashboards/company_scoring_template.csv](../09_dashboards/company_scoring_template.csv).
- Qualified companies move to [../09_dashboards/pipeline_template.csv](../09_dashboards/pipeline_template.csv).
- Daily totals in [../09_dashboards/daily_numbers_template.csv](../09_dashboards/daily_numbers_template.csv).

`company_scoring_template.csv` columns: `company_name, sector, region, size_band, source_type, why_now_signal, pain_hypothesis, fit_score, intent_score, total_score, recommended_offer, gap_identified, consent_basis, owner, status, next_action, next_action_date, notes`.

Example placeholder: "Example Trading Co", `consent_basis = legitimate_interest_b2b`, business contact only.

> القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value
