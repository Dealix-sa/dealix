# Market Intelligence OS — Targeting and research system — نظام استخبارات السوق

## Purpose — الغرض

Market Intelligence OS researches sectors, identifies candidate companies, and narrows a broad market into a short, defensible list of accounts worth pursuing. It runs a staged funnel — 400 candidates to 80 to 20 to 10 to 5 — where each stage applies explicit, recorded criteria so the shortlist can be defended to anyone who asks why a company is on it. AI explores public-context signals and analyzes fit and recommends ranking; deterministic workflows apply the scoring rules; the founder reviews and approves the final shortlist. The system never scrapes, never automates outreach, and never invents facts about a company. It produces company intelligence that feeds Revenue OS and Command OS.

نظام استخبارات السوق يبحث القطاعات، ويحدّد الشركات المرشّحة، ويضيّق سوقاً واسعة إلى قائمة قصيرة قابلة للدفاع عنها من الحسابات الجديرة بالمتابعة. يدير قمعاً متدرّجاً — 400 مرشّح إلى 80 إلى 20 إلى 10 إلى 5 — حيث تطبّق كل مرحلة معايير صريحة مسجّلة بحيث يمكن الدفاع عن القائمة أمام أي سائل عن سبب وجود شركة فيها. يستكشف الذكاء الاصطناعي الإشارات العامة ويحلّل الملاءمة ويوصي بالترتيب؛ وتطبّق المسارات الحتمية قواعد التقييم؛ ويراجع المؤسس القائمة النهائية ويعتمدها. لا يجمع النظام البيانات بالكشط، ولا يؤتمت التواصل، ولا يختلق حقائق عن شركة. ينتج استخبارات الشركة التي تغذّي نظام الإيراد ونظام القيادة.

## Status — الحالة

Market Intelligence OS | BETA | Research → score → shortlist pipeline, founder-reviewed

نظام استخبارات السوق | BETA | مسار البحث ← التقييم ← القائمة المختصرة، بمراجعة المؤسس

## Inputs — المدخلات

- Sector and ICP definition from go-to-market docs — تعريف القطاع والعميل المثالي من وثائق الذهاب إلى السوق
- Publicly available company context (no scraping) — السياق العام المتاح عن الشركات (بلا كشط)
- Scoring criteria and disqualifiers — معايير التقييم وأسباب الاستبعاد

## Outputs — المخرجات

- Funnel record: 400 → 80 → 20 → 10 → 5 with reasons — سجل القمع: 400 ← 80 ← 20 ← 10 ← 5 مع الأسباب
- Company intelligence sheet per shortlisted account — ورقة استخبارات الشركة لكل حساب مختصر
- Targeting shortlist handed to Revenue OS — قائمة الاستهداف المسلّمة لنظام الإيراد

## Guardrails — الضوابط

- No scraping (1): only manually gathered, sourced public context — لا كشط للبيانات
- No fake or un-sourced claims (4): every company fact cites a source — لا ادعاءات مزيّفة أو بلا مصدر
- No cold WhatsApp / LinkedIn automation (2, 3): research informs manual, approved outreach only — لا أتمتة تواصل بارد على واتساب أو لينكدإن
- No source-less answers (7): scores trace to recorded criteria — لا إجابات بلا مصدر

## Cross-links — روابط

- [`../00_platform_truth/MODULE_STATUS_MAP.md`](../00_platform_truth/MODULE_STATUS_MAP.md)
- GTM sibling: [`../01_go_to_market/MARKET_INTELLIGENCE_OS.md`](../01_go_to_market/MARKET_INTELLIGENCE_OS.md)
- [`REVENUE_OS.md`](./REVENUE_OS.md) · [`COMMAND_OS.md`](./COMMAND_OS.md) · [`GOVERNANCE_OS.md`](./GOVERNANCE_OS.md)

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
