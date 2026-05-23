# Sales Scripts

Sales scripts are bilingual conversation aids for the human seller. They are not autocomplete. Every sentence in every script must be defensible against the no-guarantee rule.

**Source of truth:** `$PRIVATE_OPS/sales_scripts.csv`
**Owner:** Founder + Revenue Lead
**Trust gate:** A1 — script updates are reviewed monthly.

## Four scripts

| Script | Audience | Length | Output |
|--------|----------|--------|--------|
| Discovery | Cold-warm | 30 minutes | Discovery brief |
| Qualification | Discovery completed | 20 minutes | Go / no-go decision |
| Close | Proposal sent | 30 minutes | Decision and date |
| No-guarantee response | Any | 1-2 minutes | Reframe |

## Discovery script (excerpt)

EN: "We're a Revenue Operating System for Saudi B2B teams. We don't promise revenue; we build the factory that makes revenue measurable. Before we discuss any package, I'd like to understand three things: your current revenue motion, the friction point you'd most like solved, and the data you already have."

AR: "نحن نظام تشغيل للإيرادات لفِرَق B2B في السعودية. لا نَعِد بإيرادات؛ نبني المصنع الذي يجعل الإيرادات قابلة للقياس. قبل أن نناقش أي باقة، أودّ أن أفهم ثلاثة أمور: حركة الإيرادات الحالية لديكم، نقطة الاحتكاك الأكثر إلحاحًا، والبيانات المتوفرة لديكم."

## Qualification script (excerpt)

The qualifying questions:

1. Who is the economic buyer and have they agreed to a 30-minute call?
2. What is the budget range for the next quarter?
3. What is the current revenue process map?
4. What is the explicit success criterion for the first engagement?
5. What is your timeline?
6. Who would be impacted by trust or data-handling concerns?

A "no" on the economic buyer question is a polite pause, not a force-through. Force-through is a documented pattern that erodes trust.

## Close script (excerpt)

EN: "We've sent the proposal. It includes scope, exclusions, deliverables, timeline, and price. There are three open questions I'd like to align on: are the deliverables right, is the timeline workable, and is the price within range? If yes to all three, we sign today. If any are no, we adjust on this call."

AR: "أرسلنا المقترح. يتضمن النطاق، الاستثناءات، المخرجات، الجدول الزمني، والسعر. هناك ثلاثة أسئلة مفتوحة أودّ التوافق عليها: هل المخرجات صحيحة، هل الجدول الزمني عملي، وهل السعر ضمن النطاق؟ إذا كانت الإجابة نعم على الثلاثة، نوقّع اليوم. إذا كان أيٌّ منها لا، نُعدّل في هذه المكالمة."

## No-guarantee response script

When a prospect asks "how much revenue will we make":

EN: "We don't promise revenue. We promise a factory whose throughput you can measure. Based on case-safe patterns, prospects with your profile typically see an increase in qualified conversations in the first sprint. The exact number depends on your data, your team, and your market. We'll show you the case-safe patterns; we won't show you a fabricated forecast."

AR: "لا نَعِد بإيرادات. نَعِد بمصنع يمكنكم قياس إنتاجيته. استنادًا إلى أنماط آمنة من حالات سابقة، يشهد العملاء بمواصفاتكم عادةً زيادة في المحادثات المؤهَّلة خلال السبرنت الأول. الرقم الفعلي يعتمد على بياناتكم وفريقكم وسوقكم. سنُريكم الأنماط؛ لن نُريكم توقعًا مُختلَقًا."

## Failure modes

- **Script drift:** a seller invents numbers under pressure. Detection: call recording review. Recovery: re-train, log in `$PRIVATE_OPS/sales_coaching_log.csv`.
- **Skipped qualification:** a proposal is sent without qualification complete. Detection: factory state. Recovery: roll back to qualification stage.
- **No-guarantee bypass:** a script is amended to imply a guarantee. Detection: monthly script audit. Recovery: revert; founder review.

## Recovery path

If scripts diverge from the published versions in source control, the founder freezes new prospect calls until alignment.

## Metrics

- Calls per script per week.
- Qualification pass rate.
- Close rate by script version (estimated).
- No-guarantee incidents per quarter (target: 0).

## Disclaimer

Scripts are aids, not promises. Dealix does not guarantee revenue. Estimated value is not Verified value.
