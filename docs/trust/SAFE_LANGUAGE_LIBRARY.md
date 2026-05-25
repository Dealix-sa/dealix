# Safe Language Library — مكتبة العبارات الآمنة

## Purpose
Provide approved replacement phrases for every banned phrase listed in `docs/trust/NO_OVERCLAIM_POLICY.md`. Operators consult this file when the scanner flags a hit.

## Owner
Founder.

## Inputs
- Banned phrase list.
- Author drafts that hit the scanner.

## Outputs
- Approved replacements per category.
- Worked examples (before / after).

## Rules (numbered)
1. Every banned phrase has at least one approved replacement.
2. Replacements name what Dealix delivers, not what the buyer will do.
3. Replacements are bilingual; AR and EN entries are kept in parallel.
4. New replacements require A2 approval; new categories require A3.
5. Operators who improvise their own replacement file a one-line note in `docs/learning/MESSAGE_PERFORMANCE.md`.

## Metrics
- Number of times each replacement is used per month.
- Improvised replacements per quarter (target less than 5).
- Phrases retired per quarter.

## Cadence
Quarterly review.

## Evidence (paths)
- `docs/trust/registers/safe_language_usage.md`

## Verifier
Founder.

## Runtime Command
`make trust.safe_language.suggest TEXT=<file>` proposes replacements for flagged phrases.

## Replacement table

| Banned (EN) | Approved (EN) | Banned (AR) | Approved (AR) |
|---|---|---|---|
| guaranteed revenue | evidenced opportunities | نضمن إيرادات | فرص مُثبتة بأدلة |
| guaranteed sales | evidenced opportunities | نضمن مبيعات | فرص مُثبتة بأدلة |
| guaranteed results | documented outputs | نضمن نتائج | مخرجات موثّقة |
| 100% accuracy | validated against schema X with failure modes Y listed | دقة 100٪ | مُتحقَّق عبر المخطط X مع توثيق حالات الإخفاق Y |
| AI-powered | uses model X for task Y (named) | مدعوم بالذكاء الاصطناعي | يستخدم نموذج X لمهمة Y |
| transform your business | name the specific change | نُحوّل أعمالك | حدّد التغيير المعني |
| supercharge | name the specific lift, with a baseline | (none used) | (الأفضل تجنّبها) |
| revolutionary | new (and cite the prior approach) | ثوري | جديد (مع الإشارة للنهج السابق) |
| best-in-class | best on benchmark X dated Y | الأفضل في فئته | الأفضل على معيار X بتاريخ Y |
| industry-leading | leading on metric X as of date Y | الرائد في المجال | الرائد في المقياس X اعتبارًا من Y |
| guaranteed ROI | observed ROI range from prior sprints (with sample size) | نضمن العائد | نطاق عائد مُلاحظ من السبرنتات السابقة (مع حجم العينة) |
| X% conversion rate (promised) | observed reply rate range was X to Y in N cases | معدل تحويل X٪ (موعود) | تراوحت معدلات الرد بين X و Y في N حالات |
| we ensure | we deliver (name artifact) | نضمن | نُسلّم (اذكر المنتج) |
| fail-proof | designed with failure modes documented | لا يخفق | مُصمَّم مع توثيق حالات الإخفاق |
| risk-free | risks named and bounded in the SOW | بدون مخاطر | المخاطر مذكورة ومحدودة في عقد العمل |

## Worked examples

**Before:** "Our AI-powered platform guarantees revenue uplift for Saudi B2B companies."
**After:** "Our 7-day Revenue Sprint delivers an evidence pack with scored leads, message variants, and source citations. The client owns sending and outcomes."

**Before:** "نضمن لكم زيادة المبيعات بنسبة 30٪ خلال شهر."
**After:** "نُسلّم خلال 7 أيام حزمة أدلة تتضمن قائمة فرص مُقيَّمة ومتغيرات رسائل ومصادر موثَّقة. القرار بالإرسال والنتائج النهائية مسؤولية العميل."

**Before:** "Industry-leading conversion through revolutionary AI."
**After:** "Sector-specific outreach packs with source-cited evidence. Methodology documented at `docs/delivery/revenue_sprint/REVENUE_SPRINT_FACTORY.md`."

## Operating substance
The Safe Language Library is the practical companion to the no-overclaim policy. The policy says what is forbidden; this file says what to write instead. Without the library, scanner hits become friction; with it, they become a 60-second swap.

The pattern is consistent. Banned phrases are vague and unverifiable; approved phrases are concrete and verifiable. The replacement always points to a method, a metric, or a deliverable that someone outside Dealix could check.

Operators who find themselves writing a phrase that does not match any entry in the library are encouraged to write the literal capability instead. "This system reads public registers and flags companies that filed in the last 60 days" is always stronger copy than any marketing phrase it might replace.

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
