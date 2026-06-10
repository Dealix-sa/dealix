# Market Intelligence OS — Targeting Engine (GTM) — استخبارات السوق — محرّك الاستهداف

This is the go-to-market view of the Dealix targeting engine: how a wide market becomes five strong, manual, evidence-based outreach sends. It is an intelligence system, not a spam system. Status: BETA. The operating-system one-pager lives at [`../02_operating_systems/MARKET_INTELLIGENCE_OS.md`](../02_operating_systems/MARKET_INTELLIGENCE_OS.md); this document stays operational and GTM-facing.

هذه هي رؤية الانطلاق إلى السوق لمحرّك الاستهداف في Dealix: كيف يتحوّل سوق واسع إلى خمس رسائل تواصل يدوية قوية مبنية على الأدلة. إنه نظام استخبارات لا نظام رسائل عشوائية. الحالة: BETA. صفحة النظام الواحدة في [`../02_operating_systems/MARKET_INTELLIGENCE_OS.md`](../02_operating_systems/MARKET_INTELLIGENCE_OS.md)، ويبقى هذا المستند تشغيلياً وموجّهاً للانطلاق.

---

## The funnel — القُمع

| Stage — المرحلة | Count — العدد | What happens — ماذا يحدث |
|---|---|---|
| Raw candidates — مرشّحون خام | 400 | Discovered from legitimate, terms-respecting sources |
| Scored targets — أهداف مُقيَّمة | 80 | Pass the scorecard cutoff |
| Founder shortlist — قائمة المؤسس | 20 | Founder confirms fit and a real decision-maker |
| Drafts — مسودات | 10 | One angle + one CTA each, evidence attached |
| Manual sends — إرسال يدوي | 5 | Founder-approved, sent by hand |

The ratio is deliberate. Each step removes noise, so the five messages that go out are the most relevant five, each carrying its own evidence. Volume is never the goal; relevance is.

النسبة مقصودة. كل خطوة تزيل الضجيج، فالرسائل الخمس التي تخرج هي الأكثر صلة، وكل منها يحمل دليله. الحجم ليس الهدف أبداً، بل الصلة.

---

## What makes a target qualified — ما الذي يجعل الهدف مؤهّلاً

A target is qualified only when all of these hold:

- **ICP fit** — a Saudi B2B service company matching the current ICP.
- **Evidence of pain** — a sourced signal of a real revenue or operations problem.
- **A reachable real decision-maker** — identifiable and reachable through a legitimate, public channel.
- **A budget signal** — observable indication the company can pay for a Sprint.
- **Timing** — a reason this is relevant now.

Each of these must be traceable to a source. No source, no qualification (non-negotiable #7). Detailed weights are in [`TARGETING_SCORECARD.md`](./TARGETING_SCORECARD.md).

يُعدّ الهدف مؤهّلاً فقط عند تحقّق كل ما يلي:

- **مطابقة الملف المثالي** — شركة خدمات سعودية بين الأعمال تطابق الملف الحالي.
- **دليل على الألم** — إشارة موثّقة إلى مشكلة إيراد أو تشغيل حقيقية.
- **صاحب قرار حقيقي يمكن الوصول إليه** — يمكن تحديده والوصول إليه عبر قناة عامة مشروعة.
- **إشارة ميزانية** — مؤشّر ملحوظ على قدرة الشركة على دفع قيمة سبرنت.
- **التوقيت** — سبب يجعل هذا مناسباً الآن.

كل عنصر يجب أن يكون متتبّعاً إلى مصدره. بلا مصدر، لا تأهيل (المبدأ رقم 7). الأوزان التفصيلية في [`TARGETING_SCORECARD.md`](./TARGETING_SCORECARD.md).

---

## Evidence requirement per target — متطلّب الدليل لكل هدف

Every target row must carry at least one cited evidence item before it can be scored. Evidence is a public, lawful reference — a company website, a public registry, a published announcement, a public job posting — recorded with its source so any claim can be checked later. Un-sourced assertions never enter the pipeline (non-negotiable #4).

كل صف هدف يجب أن يحمل عنصر دليل مُسنَد واحداً على الأقل قبل أن يُقيَّم. الدليل مرجع عام مشروع — موقع الشركة، سجل عام، إعلان منشور، إعلان وظيفة عام — يُسجَّل مع مصدره ليُمكن التحقّق من أي ادعاء لاحقاً. الادعاءات بلا مصدر لا تدخل خط الإنتاج أبداً (المبدأ رقم 4).

---

## Source policy — سياسة المصادر

- **Respect robots.txt and source terms.** If a source disallows automated access, it is not used that way.
- **No scraping behind login** (non-negotiable #1). Private or gated content is out of scope.
- **No LinkedIn or WhatsApp automation** (non-negotiables #2, #3). Channels are used by hand, within their own terms.
- **Public, lawful sources only.** Preference for first-party and official registry data.
- **No PII in logs** (non-negotiable #6). Records hold what is needed to act, not sensitive personal identifiers.

- **احترام robots.txt وشروط المصدر.** إن منع المصدر الوصول الآلي، لا يُستخدم بهذه الطريقة.
- **لا استخراج خلف تسجيل الدخول** (المبدأ رقم 1). المحتوى الخاص أو المحجوب خارج النطاق.
- **لا أتمتة لينكدإن أو واتساب** (المبدآن 2 و3). تُستخدم القنوات يدوياً ضمن شروطها.
- **مصادر عامة مشروعة فقط.** تفضيل بيانات الطرف الأول والسجلات الرسمية.
- **لا بيانات شخصية في السجلات** (المبدأ رقم 6). تحفظ السجلات ما يلزم للتصرّف، لا المعرّفات الشخصية الحسّاسة.

---

## Outputs — المخرجات

The engine produces a founder-reviewed `prospects.csv`. Its shape is described here for transparency; the data is gathered through legitimate research, not scraped:

| Column — العمود | Meaning — المعنى |
|---|---|
| `company` | Company name — اسم الشركة |
| `sector` | Sector / ICP segment — القطاع |
| `evidence_url` | Source link for at least one cited signal — رابط مصدر إشارة واحدة على الأقل |
| `pain_signal` | The sourced problem observed — المشكلة الموثّقة الملحوظة |
| `decision_maker_role` | Role only, no personal contact PII — الدور فقط، بلا بيانات اتصال شخصية |
| `legitimate_channel` | Public channel to reach out by hand — قناة عامة للتواصل اليدوي |
| `score` | Scorecard total — مجموع بطاقة التقييم |
| `stage` | raw / scored / shortlist — خام / مُقيَّم / مختصر |

The CSV feeds the founder shortlist; the founder, not the system, decides who is contacted, and contact is always manual and approved.

ينتج المحرّك ملف `prospects.csv` مُراجَعاً من المؤسس. شكله موصوف هنا للشفافية؛ والبيانات مجموعة عبر بحث مشروع لا عبر استخراج. يغذّي الملف قائمة المؤسس المختصرة؛ والمؤسس — لا النظام — يقرّر من يُتواصَل معه، والتواصل دائماً يدوي ومعتمَد.

---

Cross-links: [`COMMAND_SPRINT_OFFER.md`](./COMMAND_SPRINT_OFFER.md) · [`TARGETING_SCORECARD.md`](./TARGETING_SCORECARD.md) · [`SALES_PLAYBOOK.md`](./SALES_PLAYBOOK.md) · [`../00_platform_truth/MODULE_STATUS_MAP.md`](../00_platform_truth/MODULE_STATUS_MAP.md)

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
