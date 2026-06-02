# نظام التواصل الإعلامي — Press Outreach OS

**جزء من:** Dealix Market Production OS — انظر docs/market_os/MARKET_PRODUCTION_OS_AR.md
**المالك:** المؤسس (سامي)
**يبني على:** docs/BRAND_PRESS_KIT.md — لا يكرّره. الـ Press Kit يملك السِيَر والقوالب والـ 10 جهات؛ هذا الملف يملك **التشغيل**: متى نتواصل، بأي ترتيب، وكيف نقيس.
**آخر تحديث:** 2026-06-02

---

## الغرض

تحويل التغطية الإعلامية من حدث عشوائي إلى **نظام مُحفَّز بالإثبات**. لا نتواصل مع جهة إعلامية لأن «الوقت مناسب» — نتواصل لأن **معلَماً حقيقياً تحقّق** ويستحق الرواية. القاعدة الحاكمة: لا يُعلَن شيء قبل أن يصبح صحيحاً (انظر docs/press/PROOF_MILESTONES_AR.md).

## المحفّزات (Triggers)

كل محفّز هو حدث **قابل للتحقّق** يفتح حملة تواصل واحدة. لا حملة بدون محفّز.

| المحفّز | الشرط القابل للتحقّق | الزاوية الأساسية |
|--------|----------------------|------------------|
| أول 3 تجارب مدفوعة | 3 عملاء بحالة `payment_confirmed` | مؤسس سعودي، منتج جاهز، أول شركاء تأسيس |
| أول حزمة إثبات (Proof Pack) | حزمة 14 قسماً مُسلَّمة وموقَّع على نشرها | منهجية الإثبات الموثّق لشركة B2B سعودية |
| 10 عملاء مدفوعين | 10 عملاء بحالة `payment_confirmed` | نموّ بصفر cold outreach، امتثال PDPL |
| أول تجديد شريك | شريك واحد جدّد العقد بعد دورة كاملة | نموذج الشراكة المستدام، لا حصص مشتراة |
| معلَم امتثال سعودي | تسجيل/مراجعة منظِّم مكتملة وموثّقة | الامتثال كميزة معمارية لا إعداد اختياري |
| دراسة حالة | دراسة مُجهَّلة الهوية مُعتمَدة (انظر case-studies) | نمط نتائج آمن قانونياً، لا أسماء عملاء |

> أي محفّز يتطلّب موافقة المؤسس على «أنه صحيح الآن» قبل فتح الحملة. الادّعاء قبل التحقّق ممنوع.

## قاعدة الثلاثة (مأخوذة من الـ Press Kit)

الـ Press Kit يحدّد القاعدة؛ هنا نفصّل تشغيلها لكل حملة:

1. **اختر 3 جهات فقط** من الـ 10 (انظر docs/press/MEDIA_TARGETS_AR.md). لا إرسال للعشرة دفعة واحدة.
2. **اكتب طرحاً مخصّصاً لكل جهة** (≈80 كلمة)، موجَّهاً لصحفي مُسمّى لا لبريد التحرير العام، وبزاوية الجهة لا زاوية عامة.
3. **انتظر 7 أيام** قبل أي متابعة. متابعة واحدة مهذّبة ثم توقّف.

## مراحل الـ Pipeline

كل جهة مُتواصَل معها تمرّ بمراحل واضحة، تُسجَّل في reports/press/PRESS_PIPELINE.md:

1. **مُختارة (Selected)** — ضمن الثلاثة لهذا المحفّز، الزاوية محدّدة.
2. **طرح أُرسِل (Pitched)** — طرح مخصّص أُرسِل لصحفي مُسمّى، التاريخ مُسجَّل.
3. **انتظار (Waiting)** — داخل نافذة الـ 7 أيام، لا فعل.
4. **رد (Replied)** — اهتمام أو رفض أو طلب معلومات.
5. **مقابلة/تجهيز (Briefing)** — موعد محجوز، تجهيز 3 أيام للبثّ الحيّ (قاعدة الـ Press Kit).
6. **نُشِر (Published)** — التغطية صدرت؛ تُسجَّل في docs/wave6/live/press_log.jsonl.
7. **مغلق بلا رد (Closed-No-Reply)** — بعد المتابعة الواحدة دون رد؛ الجهة تعود للقائمة لمحفّز لاحق.

## مبادئ غير قابلة للتفاوض

- لا cold outreach جماعي للإعلام؛ تواصل 1:1 مخصّص فقط.
- لا أرقام معايير مُختلَقة في المقابلات؛ «لا نملك بيانات على ذلك بعد» إجابة مقبولة.
- لا أسماء عملاء بدون `signed_publish_permission` لكل عميل.
- لا ادّعاءات تنظيمية/قانونية بدون مراجعة قانونية.
- لا «نضمن» ولا أرقام مبيعات كحقائق؛ الإثبات موثَّق والنتائج تقديرية.
- أرفِق رابط الـ Press Kit مع كل طرح، ووفّر اقتباساً عربياً + إنجليزياً.

## الخطوة التالية

عند تحقّق أي محفّز: افتح صفّاً في reports/press/PRESS_PIPELINE.md، اختر 3 جهات من docs/press/MEDIA_TARGETS_AR.md بزاويتها، واسحب قالب الطرح من docs/BRAND_PRESS_KIT.md §5.

## English summary

Press outreach is a milestone-triggered system, not opportunistic. No campaign opens without a verifiable trigger (first 3 paid pilots, first Proof Pack, 10 paid customers, first partner renewal, a Saudi compliance milestone, or an approved case study). Each campaign follows the kit's rule: pick 3 outlets, write an ~80-word personalized pitch to a named journalist, wait 7 days, one polite follow-up, then stop. Pipeline stages run Selected → Pitched → Waiting → Replied → Briefing → Published → Closed-No-Reply, logged in reports/press/PRESS_PIPELINE.md. Nothing is announced before it is true: no "N customers" before N are payment-confirmed. This doc builds on docs/BRAND_PRESS_KIT.md (bios, templates, outlet list) and does not restate it. No guarantees, no invented benchmarks, no customer names without signed publish permission.

---

القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value.
