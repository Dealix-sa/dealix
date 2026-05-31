# إطار حوكمة الذكاء الاصطناعي — AI Governance Framework

> الغرض: تحديد المبادئ غير القابلة للتفاوض، قواعد التصنيف، ومتطلبات المراجعة البشرية التي تحكم كل مخرج ذكاء اصطناعي في ديلكس. هذا الإطار يُطبَّق على جميع نماذج اللغة، وكلاء الذكاء الاصطناعي، وخطوط معالجة البيانات.
>
> Purpose: Define the non-negotiables, classification rules, and human review requirements governing every AI output in Dealix. This framework applies to all language models, AI agents, and data processing pipelines.
>
> وثائق ذات صلة: [`docs/05_governance_os/GOVERNANCE_OS.md`](../05_governance_os/GOVERNANCE_OS.md) | [`docs/04_data_os/PII_CLASSIFICATION.md`](../04_data_os/PII_CLASSIFICATION.md) | [`docs/06_llm_gateway/LLM_GATEWAY.md`](../06_llm_gateway/LLM_GATEWAY.md) | [`docs/00_constitution/NON_NEGOTIABLES.md`](../00_constitution/NON_NEGOTIABLES.md)

---

## 1. المبادئ الأحد عشر غير القابلة للتفاوض — 11 Non-Negotiables

### العربية

هذه المبادئ تتفوق على أي طلب عميل أو ضغط تشغيلي أو قرار تجاري. لا استثناءات.

**المبدأ الأول: الموافقة أولاً (APPROVAL_FIRST)**
لا يُنفَّذ أي إجراء خارجي — إرسال رسالة، تعديل سجل، تحرير قرار — إلا بعد موافقة صريحة ومُسجَّلة من الشخص المسؤول. "الموافقة الضمنية" أو "الموافقة بالصمت" غير مقبولة. كل موافقة تُسجَّل مع الطابع الزمني ومعرِّف الموافق.

**المبدأ الثاني: لا إرسال خارجي من بنية ديلكس**
منصة ديلكس لا تُرسِل رسائل نيابةً عن العميل من خوادمها. المسودات تُسلَّم للعميل الذي يُرسِلها من قنواته الخاصة. هذا الحد لا علاقة له بالتقنية — هو اختيار تصميمي واعٍ لحماية العميل والمنصة من المسؤولية القانونية.

**المبدأ الثالث: لا تجريف للبيانات (No Scraping)**
مصادر البيانات المقبولة: `client_upload`, `crm_export`, `manual_entry`, `api_authorized`. مصدر `scraped` مرفوض في جميع الأحوال — حتى إذا طلبه العميل، حتى إذا كانت البيانات "متاحة للعموم".

**المبدأ الرابع: لا ادعاءات ضامنة للعائد**
كل مخرج ذكاء اصطناعي يتضمن تصنيف القيمة: مُقدَّرة أو مُرصَدة أو مُتحقَّقة. لا خوارزمية تُصدِر نتيجة بصياغة "هذا سيُحقِّق X ريال". الصياغة الصحيحة: "هذا النمط مرتبط بـ X ريال في حالات مماثلة (تقدير)".

**المبدأ الخامس: لا PII في السجلات التشغيلية**
سجلات التشغيل، ملفات الأخطاء، ومخرجات التصحيح لا تحتوي على بيانات شخصية. PII في خطوط المعالجة يُزال أو يُحجَّب قبل التسجيل. هذا إلزامي وفق PDPL بصرف النظر عن موافقة العميل.

**المبدأ السادس: هوية الوكيل موثَّقة (Agent Identity)**
كل وكيل ذكاء اصطناعي يعمل في ديلكس له معرِّف فريد، نطاق صلاحيات مُقيَّد، ومالك بشري محدد. لا "وكيل مجهول". لا وكيل يعمل بصلاحيات أوسع مما يحتاجه مهمته المحددة.

**المبدأ السابع: القابلية للتفسير شرط الشحن**
لا مخرج ذكاء اصطناعي يُشحَن إلى العميل بدون تفسير مقروء للإنسان. "البياض" ليس قيمة — هو خطر. إذا لم نستطع شرح لماذا وصل الوكيل إلى هذه النتيجة، فالنتيجة لا تُشحَن.

**المبدأ الثامن: التكافؤ الثنائي (Bilingual Parity)**
المخرجات العربية والإنجليزية تحمل نفس المعنى والدقة. الترجمة الآلية دون مراجعة بشرية غير مقبولة للمخرجات النهائية الموجَّهة للعميل. اختلال التكافؤ يُشكِّل ادعاءاً مضللاً.

**المبدأ التاسع: الاحتفاظ بالبيانات محدود بالغرض**
البيانات تُحتجَز فقط طوال المدة المُعلَنة في جواز المصدر. بعد الإغلاق، تُحذَف البيانات الخام وفق الجدول المحدد. لا يُعاد استخدام بيانات العميل لتدريب نماذج دون موافقة صريحة مُوثَّقة.

**المبدأ العاشر: الانجراف مُراقَب ومعالَج (Model Drift Monitoring)**
النماذج المُنشورة تخضع لمراقبة مستمرة. الانجراف المكتشَف يُوقِف المخرجات الآلية تلقائياً حتى يُراجَع النموذج. لا نموذج يعمل "في الظلام" بدون لوحة مقاييس مرئية.

**المبدأ الحادي عشر: سجل التدقيق دائم (Immutable Audit Log)**
كل إجراء اتخذه وكيل ذكاء اصطناعي يُسجَّل في سجل تدقيق لا يمكن تعديله أو حذفه. يشمل: معرِّف الوكيل، نوع الإجراء، الطابع الزمني، معرِّف المُدخل، نتيجة قرار الحوكمة، ومعرِّف الموافق إن وُجِد.

### English

These eleven principles are not guidelines or best practices. They are constraints built into the system architecture. A feature request that violates any of them is declined at design time, not patched afterward. Every new capability introduced to the Dealix platform must be evaluated against this list before moving from concept to development.

The most important property of these principles is their unconditional nature. There are no exceptions granted for large clients, urgent timelines, or competitive pressure. The moment an exception is made, the principle ceases to function as a constraint and becomes merely a preference.

---

## 2. تصنيف قرارات الذكاء الاصطناعي — AI Decision Classification

### العربية

كل مخرج يُنتِجه الذكاء الاصطناعي في ديلكس يقع ضمن أحد سبعة تصنيفات. التصنيف يُحدَّد بالسياق والخطورة، لا بالميزة أو الوكيل.

| التصنيف | المعنى | أمثلة |
|--------|--------|-------|
| `ALLOW` | يُنفَّذ مباشرة دون مراجعة إضافية | احتساب DQ Score، ترتيب البيانات الداخلي، توليد تقرير إحصائي بدون PII |
| `ALLOW_WITH_REVIEW` | يُنفَّذ لكن يُراجَع بشكل دوري في مراجعة الجودة | توليد مسودات داخلية، احتساب تقييم الحساب، توليد نص غير موجَّه للخارج |
| `DRAFT_ONLY` | المخرج جاهز للعرض للعميل لكن لا يُصبح فعَّالاً | مسودات التواصل الخارجي، اقتراحات السعر، ملخصات العميل |
| `REQUIRE_APPROVAL` | يتطلب موافقة صريحة من الشخص المُخوَّل قبل أي خطوة | أي إجراء خارجي، تعديل البيانات الرئيسية، مخرجات تمس PDPL |
| `REDACT` | المخرج يحتوي على PII أو معلومات حساسة تستوجب التحجيب | أي نص يتضمن أسماء أو جوالات أو أرقاماً هوية |
| `RATE_LIMIT` | الحجم أو التكرار يتجاوز الحد المعقول للمراجعة البشرية | طلبات توليد أكثر من 50 مسودة في ساعة واحدة |
| `BLOCK` | مرفوض نهائياً — يُسجَّل في السجل ولا يُنتَج | أي طلب يتضمن تجريف بيانات، واتساب بارد، أو ادعاءات ضامنة |

**قاعدة التخصيص:** إذا شكَّ الوكيل أو المشغِّل البشري في التصنيف، يُطبَّق التصنيف الأعلى احترازاً. الشك يعني `REQUIRE_APPROVAL`، لا `ALLOW`.

### English

The seven-class decision taxonomy applies at two levels: the automated governance engine applies it at runtime for every AI action, and the founder applies it manually during the daily delivery review for any edge case the automated engine flags as uncertain.

`ALLOW_WITH_REVIEW` is the most commonly misunderstood class. It does not mean "do it now and check later if there is a problem." It means "execute and log, and a human reviews the pattern periodically." The review frequency is defined per capability type in the capability matrix.

---

## 3. متطلبات الإنسان في الحلقة — Human-in-the-Loop Requirements

### العربية

الإنسان في الحلقة ليس خياراً تصميمياً اختيارياً — هو ضمانة تشغيلية لكل مخرج يمس العميل النهائي أو يُنتِج ادعاءً قيمياً.

| نوع المخرج | هل يتطلب مراجعة بشرية؟ | المرحلة |
|-----------|------------------------|---------|
| مسودات تواصل موجَّهة للخارج | نعم — المؤسس أو المراجع المُعيَّن | قبل تسليمها للعميل |
| تقييم الحسابات (Top 10) | نعم — المؤسس يقرأ كل تفسير | قبل إدراجها في حزمة الإثبات |
| DQ Score | مراجعة عند النقاط العتبية (< 40 أو > 90) | لا مراجعة روتينية في النطاق الطبيعي |
| قرارات `BLOCK` | نعم — توثيق السبب الجذري | عند كل حدث `BLOCK` |
| تصنيف القيمة (مُقدَّر/مُرصَد/مُتحقَّق) | نعم — مراجعة قبل الإصدار | قبل شحن حزمة الإثبات |
| ملخصات الحالات (Case Summaries) | نعم — مراجعة كاملة للتجهيل | قبل النشر |
| تقارير قطاعية | نعم — مراجعة المنهجية والادعاءات | قبل أي توزيع |

**معيار المراجعة البشرية:** المراجع يتحقق من ثلاثة أشياء: (1) هل المخرج قابل للتفسير؟ (2) هل التصنيف (مُقدَّر/مُرصَد/مُتحقَّق) دقيق؟ (3) هل يحتوي على ادعاءات ضامنة غير مدعومة بأدلة؟

### English

Human review is not a bottleneck to be engineered away — it is the quality signal that makes Dealix's outputs distinguishable from automated noise. The founder's daily review of AI outputs is an investment in the Proof Pack's credibility, not an operational inefficiency.

As Dealix scales and a delivery team is added, the human review responsibility transfers to trained reviewers with explicit authority to approve or reject any output before it reaches a client. The review standards defined in this table are the training baseline for those reviewers.

---

## 4. متطلبات اختبار التحيز في نماذج اللغة العربية — Bias Testing Requirements for Arabic NLP

### العربية

النماذج اللغوية المُنشورة في ديلكس تعمل بشكل أساسي على المحتوى العربي. التحيز في السياق العربي يأخذ أشكالاً لا تكتشفها الاختبارات القياسية الإنجليزية:

**1. التحيز الجنساني في العربية**
العربية لغة مُجنْدَرة نحوياً. النماذج قد تُصنِّف الأسماء المؤنثة بشكل مختلف عن المذكرة حتى في السياقات المهنية. يُختبَر النموذج على مجموعة بيانات متوازنة تحتوي على أسماء عربية مُجنْدَرة بوضوح مع مهام تسجيل متطابقة.

**2. التحيز الجغرافي (المناطق السعودية)**
الرياض ≠ جدة ≠ الدمام في سلوك النماذج المُدرَّبة على بيانات غير متوازنة. يُختبَر النموذج على مدخلات متماثلة من مناطق مختلفة للكشف عن تباين غير مبرر في النتائج.

**3. التحيز القطاعي**
النماذج المُدرَّبة على بيانات غير متوازنة قد تُولِّد نتائج أفضل لقطاعات معينة (مثلاً التقنية) على حساب قطاعات أخرى (مثلاً التجزئة، الصناعة الغذائية). يُختبَر على عينات عبر القطاعات المستهدفة.

**4. تحيز الحجم (حجم الشركة)**
الشركات الكبيرة قد تحصل على ترتيبات أعلى بشكل منهجي بسبب الحجم لا الجدارة. تُفصَل ميزة الحجم عن مقاييس الترتيب الأخرى وتُختبَر تأثيراتها بشكل مستقل.

**دورة الاختبار:** قبل كل نشر لنموذج جديد أو إصدار رئيسي. النتائج تُسجَّل في سجل التقييم مع حدود القبول المُعلَنة مسبقاً. نموذج لا يجتاز اختبار التحيز لا يُنشَر.

### English

Bias testing is not a checkbox — it is a deployment gate. A model that passes accuracy benchmarks but fails bias tests is blocked from production until the bias source is identified and addressed. The bias test results are documented in the model evaluation registry and referenced in any client-facing reporting that uses that model.

Arabic NLP presents unique challenges because most open-source bias datasets are English-centric. Dealix maintains an internal Arabic bias test set that is updated as new patterns are identified in production. Contributions to this test set from delivery experience (anonymized) are a form of capital asset registration.

---

## 5. الامتثال لـ PDPL في خطوط الذكاء الاصطناعي — PDPL Compliance in AI Pipelines

### العربية

**تقليص البيانات (Data Minimization)**
خط معالجة الذكاء الاصطناعي يُطلَب منه فقط الحقول اللازمة لأداء مهمته المحددة. المعالجة لا تُحمِّل بيانات إضافية "قد تكون مفيدة". كل نموذج أو وكيل له قائمة حقول مُحدَّدة في سجل التقييم — ما ليس في القائمة لا يُمرَّر.

**تحديد الغرض (Purpose Limitation)**
البيانات المُعالَجة لترتيب الحسابات لا تُستخدَم لتدريب نموذج. البيانات المُعالَجة لتوليد المسودات لا تُستخدَم لأغراض تحليلية. كل استخدام جديد يتطلب تقييماً مستقلاً وجواز مصدر جديداً.

**الاستبعاد من المعالجة الآلية**
إذا طلب شخص طبيعي عدم إخضاع بياناته لقرارات آلية وفق PDPL، يُعلَّم هذا السجل بـ `opt_out_automated = true` ويُستبعَد من خطوط الذكاء الاصطناعي تلقائياً. الاستبعاد لا يُلغي الخدمة — يُحوِّلها إلى مسار يدوي.

**إشعار المعالجة**
كل موافقة جديدة على معالجة بيانات تشمل: وصف الغرض، مدة الاحتجاز، حق الوصول والتصحيح، وحق سحب الموافقة. هذا الإشعار يُوثَّق في جواز المصدر.

### English

PDPL compliance in AI pipelines is more demanding than traditional data protection because AI processing is iterative and multi-stage. A single data point may pass through a preprocessing pipeline, a model inference call, a post-processing step, and a report generation stage — each of which constitutes a distinct processing activity.

Dealix's architectural response is the Source Passport: a single document that declares the permitted processing chain for each data batch. Any processing step not listed in the Source Passport is blocked at the pipeline level, not reviewed case by case.

---

## 6. متطلبات سجل التدقيق — Audit Logging Requirements

### العربية

**ما يُسجَّل إلزامياً لكل إجراء وكيل:**

| الحقل | الوصف | مثال |
|-------|-------|------|
| `event_id` | معرِّف فريد للحدث | `evt_20260531_001` |
| `agent_id` | معرِّف الوكيل المُنفِّذ | `agent_revenue_scoring_v2` |
| `action_type` | نوع الإجراء | `score_accounts`, `generate_draft`, `block_request` |
| `timestamp_utc` | توقيت التنفيذ بالتوقيت العالمي | `2026-05-31T10:23:44Z` |
| `input_ref` | مرجع المُدخل (لا البيانات الفعلية) | `passport_id: pp_001` |
| `governance_decision` | قرار الحوكمة | `ALLOW`, `BLOCK`, `REQUIRE_APPROVAL` |
| `approver_id` | معرِّف الموافق إن وُجِد | `founder_001` أو فارغ |
| `output_ref` | مرجع المخرج (لا البيانات الفعلية) | `scoring_output_001` |
| `pii_touched` | هل مُعولِجت بيانات شخصية؟ | `true` / `false` |
| `redaction_applied` | هل طُبِّق حجب؟ | `true` / `false` |

**فترة الاحتجاز:** سجلات التدقيق تُحتَجَز لمدة لا تقل عن 5 سنوات. لا يمكن حذفها أو تعديلها بعد الإيداع — سجل التدقيق هو سجل غير قابل للتغيير (Immutable Ledger).

**الوصول:** سجلات التدقيق متاحة للمؤسس ولأي جهة تنظيمية معتمدة. لا تُشارَك مع العملاء بشكل كامل — يُوفَّر ملخص مُعالَج في حزمة الإثبات.

### English

The audit log is the operational backbone of Dealix's trust model. When a client asks "what did your platform do with our data?", the answer comes from the audit log — not from memory, not from a general policy statement. Every entry is timestamped, attributable to a specific agent, and linked to the governance decision that authorized or blocked the action.

The five-year retention requirement exceeds PDPL's minimum statutory period. This is a deliberate business decision: in B2B relationships, disputes can surface years after delivery. The audit log is Dealix's evidence in those disputes.

---

## 7. مراقبة انجراف النماذج — Model Drift Monitoring

### العربية

**تعريف الانجراف:** تغيُّر سلوك النموذج بمرور الوقت بسبب تغيُّر توزيع البيانات الواردة دون تغيُّر النموذج نفسه. الانجراف لا يعني أن النموذج أُصيب بعطل — يعني أن بيانات العالم الحقيقي تتغيَّر وأن النموذج لم يعد مُعايَراً لها.

**المقاييس المُراقَبة لكل نموذج في الإنتاج:**

| المقياس | العتبة الصفراء | العتبة الحمراء | الإجراء |
|--------|---------------|--------------|---------|
| التوزيع الإحصائي للمدخلات (PSI) | > 0.1 | > 0.25 | أصفر: مراقبة مكثفة. أحمر: إيقاف مؤقت + مراجعة |
| توزيع المخرجات | انحراف > 10% عن الخط الأساسي | انحراف > 20% | أصفر: تقييم. أحمر: إيقاف |
| معدل قرارات `BLOCK` | ارتفاع > 20% عن المتوسط الشهري | ارتفاع > 50% | أصفر: مراجعة المحفز. أحمر: إيقاف |
| دقة التفسيرات | تراجع > 5% في تقييم المراجع البشري | تراجع > 15% | أصفر: مراجعة. أحمر: إيقاف + إعادة تدريب |

**إجراء الاستجابة عند العتبة الحمراء:**
1. إيقاف تلقائي للمخرجات الآلية للنموذج المتضرر.
2. إعلام المؤسس خلال 30 دقيقة.
3. تحليل العينات للكشف عن مصدر الانجراف.
4. قرار: (أ) ضبط المعاملات، (ب) إعادة التدريب، (ج) استبدال النموذج.
5. اختبار قبل إعادة التفعيل.
6. توثيق الحادثة كاملة في سجل التدقيق.

### English

Model drift monitoring is the operational manifestation of the tenth non-negotiable: no model operates in the dark. The thresholds defined above are starting points calibrated for Dealix's current scale. As the client base and data volume grow, these thresholds should be reviewed quarterly and adjusted based on observed variance patterns.

The stopping condition is not punitive — it is protective. A model producing subtly degraded outputs that no one has caught is a risk to every client engagement that relies on it. The drift monitoring system is the mechanism that surfaces that risk before it becomes a client-facing failure.

---

## 8. الاستخدامات الممنوعة للذكاء الاصطناعي — Prohibited AI Uses

### العربية

هذه قائمة نهائية وغير قابلة للتفاوض. ديلكس لن تبني هذه الاستخدامات، ولن تدعمها كمزود، ولن تقبل عقداً يُلزِمها بتقديمها.

**1. أتمتة التواصل البارد عبر واتساب أو أي منصة مراسلة**
إرسال رسائل آلية لأشخاص لم يُعطوا موافقة صريحة — بغض النظر عن مصدر قائمة جهات الاتصال.

**2. تجريف المواقع أو منصات التواصل الاجتماعي**
استخراج بيانات عبر أدوات تجريف آلي من أي مصدر لم يُعطِ وصولاً مُصرَّحاً به صراحةً.

**3. أتمتة التواصل على LinkedIn أو أي منصة مهنية**
إرسال طلبات تواصل، رسائل، أو تعليقات آلية على أي منصة مهنية.

**4. ادعاءات الإيرادات المضمونة**
أي نموذج أو وكيل يُولِّد تنبؤات إيرادات تُقدَّم كضمانات لا كتقديرات.

**5. مراقبة الموظفين دون موافقة**
أي حل يراقب نشاط الموظفين (الرسائل، الإنتاجية، السلوك) دون إشعار وموافقة وفق قوانين العمل السعودية.

**6. التلاعب بالمشاعر أو الضغط النفسي**
أي نموذج يُصمَّم لاستغلال نقاط ضعف نفسية لزيادة مبيعات أو إقناع العميل باتخاذ قرار لا يصب في مصلحته.

**7. التحقق المزوَّر (Fake Proof)**
أي مخرج يُقدِّم قيمة مُقدَّرة على أنها مُتحقَّقة، أو يُقدِّم نتائج حالة افتراضية على أنها نتائج حقيقية.

**8. أنظمة التسجيل الاجتماعي أو نتائج البشر**
لا تُبني أنظمة تُصنِّف أشخاصاً بشكل آلي بطريقة تُميِّز ضدهم في الوصول إلى خدمات أو فرص.

**9. إعادة بيع بيانات العميل**
بيانات العميل ملك للعميل. لا تُستخدَم لإثراء نماذج تُباع لأطراف أخرى دون موافقة صريحة شاملة.

**10. التحايل على الامتثال التنظيمي**
أي حل يُساعد العميل على تجنب متطلبات ZATCA أو PDPL أو أي لائحة تنظيمية سعودية.

### English

These ten prohibited categories are not ranked by severity — they are all equally disqualifying. A potential client engagement that requires any of these capabilities is declined regardless of the revenue opportunity it represents. The refusal is logged in the engagement record with a clear reason.

The practical test: if a requested feature would appear on this list if described accurately, it belongs on this list even if the client has given it a different name. The governance review applies substance, not label.

---

> **القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.**

---

*آخر مراجعة: 2026-05-31 | Last reviewed: 2026-05-31*
*يُقرأ جنباً إلى جنب مع: [`docs/05_governance_os/GOVERNANCE_OS.md`](../05_governance_os/GOVERNANCE_OS.md) | [`docs/00_constitution/NON_NEGOTIABLES.md`](../00_constitution/NON_NEGOTIABLES.md) | [`docs/06_llm_gateway/LLM_GATEWAY.md`](../06_llm_gateway/LLM_GATEWAY.md)*
