## مصنع المحتوى — Content Factory (AR)

محتوى ديلكس لا يُكتب لـ "الانتشار". يُكتب ليُربط بعرض، يُقاس بتحويل، ويُعاد توظيفه كأصل. كل قطعة محتوى تجيب أربعة أسئلة قبل النشر: من جمهورها؟ ما العرض الذي تقود إليه؟ ما مقياس النجاح؟ ما الأصل الذي ستصبح عليه بعد 30 يوماً؟

### الأعمدة العشرة

| العمود | الزوايا الثلاث (AR) | العرض | الجمهور | CTA |
|--------|--------------------|--------|---------|-----|
| 1. AI يجلب إيراد | "ثلاث طرق يخسر بها فريقك إيراداً اليوم بسبب AI بلا حوكمة" / "كيف ربط فريقنا إشارة سوق واحدة بصفقة في 14 يوماً" / "حلقة الإيراد المغلقة: من إشارة إلى أصل" | Revenue Hunter Pilot | مدراء الإيراد B2B | "ابدأ الباي‌لوت بـ 999 ريال" |
| 2. AI يحتاج حوكمة | "لماذا 93% من فرق العمل يستخدمون GenAI بلا سجل أدلة" / "Permission Matrix قبل النشر: قالب" / "كيف يُكتب تقرير حوكمة AI تنفيذي" | AI Trust Kit | CIO، CTO، CISO | "احجز AI Trust Diagnostic" |
| 3. وكلاء AI للشركات | "وكيل واحد محكوم > 10 سكربتات بلا حوكمة" / "كيف يُسلَّم وكيل AI لمدير غير تقني" / "متى نقتل وكيلاً ومتى نوسّعه" | Governance OS | فرق العمليات | "احجز نقاشاً تنفيذياً" |
| 4. أمثلة سعودية / عربية | "تشخيص قطاع المقاولات السعودي: إشارات + ألم + عرض" / "كيف يتعامل قطاع الأغذية مع تقلّبات الطلب باستخدام AI محكوم" / "AI في السياحة السعودية: حالات استخدام واقعية" | Market Radar Subscription | فرق الاستراتيجية | "اشترك في الرادار" |
| 5. إنتاجية المؤسس | "30 دقيقة يومياً لإدارة قمع إيرادك بـ AI محكوم" / "نظام تشغيل المؤسس الأسبوعي" / "ثلاث أدوات AI يستخدمها مؤسسون لا تخسر بياناتهم" | Monthly Revenue Command | المؤسسون | "ابدأ القيادة الشهرية" |
| 6. أنظمة الإيراد | "أرقام تخفيها لوحات CRM عنك" / "Money Quality Score: مقياس وحيد يقول الحقيقة" / "كيف تربط كل قطعة محتوى بإيراد فعلي" | Monthly Revenue Command | مدراء المبيعات | "احجز جلسة قاموس المقاييس" |
| 7. وكالات / شركاء White-label | "كيف يقدّم وكيلك خدمات AI بدون فريق هندسي" / "تقرير عميل White-label في 60 دقيقة" / "هيكل عمولات لشركاء AI في السعودية" | Agency White-label Kit | الوكالات | "اطلب الكيت" |
| 8. قصص الحالات | "قبل / فعل / نتيجة / مخرج: قالب القصة" / "كيف نسرد قصة بلا ادعاءات" / "أصل واحد من قصة واحدة: كيف نوسّع التأثير" | Case Study Template | كل الجمهور | "حمّل قالب القصة" |
| 9. رادار السوق | "خمس إشارات سعودية تغيّر استراتيجيتك هذا الربع" / "كيف يصبح حدث تنظيمي حملة في 12 خطوة" / "TOC تقرير رادار السوق" | Market Radar Subscription | فرق الاستراتيجية | "اطلب عيّنة تقرير" |
| 10. الثقة والامتثال | "ميثاق ديلكس: ما لا نقوله أبداً" / "Evidence Pack: كيف يبدو سجل أدلة قرار AI" / "MCP Risk Review: قائمة فحص قبل الإطلاق" | AI Trust Kit | المدراء التنفيذيون | "احجز جلسة الحزمة" |

### قالب بطاقة المحتوى (Content Card)

استخدم هذا الجدول قبل كتابة أي قطعة. لا يبدأ الكاتب بدون بطاقة كاملة.

| الحقل | الوصف | مثال |
|-------|------|------|
| `pillar_id` | رقم العمود من 1 إلى 10 | 2 |
| `title_ar` | العنوان بالعربية ≤ 12 كلمة | "لماذا 93% من فرق العمل يستخدمون GenAI بلا سجل أدلة" |
| `title_en` | العنوان بالإنجليزية ≤ 12 كلمة | "Why 93% of teams use GenAI without an evidence ledger" |
| `audience` | الجمهور المحدّد | CIO سعودي |
| `pain_addressed` | الألم في جملة واحدة | "لا نعرف من يستخدم AI ولا ما الذي يخرج به" |
| `offer_id` | العرض الذي تقود إليه | ai_trust_kit |
| `channel_primary` | القناة الأولى | LinkedIn نص طويل |
| `channel_secondary` | القناة الثانية | نشرة بريد |
| `cta_ar` | CTA عربي | "احجز AI Trust Diagnostic" |
| `cta_en` | CTA إنجليزي | "Book AI Trust Diagnostic" |
| `success_metric` | المقياس الوحيد | حجوزات تشخيص خلال 14 يوماً |
| `kill_threshold` | حدّ الإلغاء | < 1 حجز بعد 1,000 ظهور |
| `evidence_required` | الدليل المطلوب قبل النشر | إحالة لمصدر 93% + قالب Permission Matrix |
| `asset_after_30d` | الأصل النهائي | قالب checklist قابل للتحميل |

نسخة YAML لمن يفضّل ملء بطاقة في ملف:

```yaml
content_card:
  pillar_id: 2
  title_ar: "لماذا 93% من فرق العمل يستخدمون GenAI بلا سجل أدلة"
  title_en: "Why 93% of teams use GenAI without an evidence ledger"
  audience: "CIO سعودي"
  pain_addressed: "لا نعرف من يستخدم AI ولا ما الذي يخرج به"
  offer_id: "ai_trust_kit"
  channel_primary: "linkedin_long"
  channel_secondary: "email_newsletter"
  cta_ar: "احجز AI Trust Diagnostic"
  cta_en: "Book AI Trust Diagnostic"
  success_metric: "diagnostic_bookings_14d"
  kill_threshold: "< 1 booking per 1000 impressions"
  evidence_required:
    - "source for 93% claim"
    - "Permission Matrix template"
  asset_after_30d: "downloadable_checklist"
```

### قواعد منع الزينة (Anti-vanity)

المقاييس التالية لا تُحتسب وحدها أبداً. كل واحد منها يجب أن يُربط بمقياس تحويل أدنى لا يقلّ عن واحد:

- إعجابات ومتابعون.
- مشاهدات الفيديو بلا اشتراك.
- ظهور Impressions بلا نقرة.
- نقرات بلا حجز.
- مشاركات بلا تعليق نوعي.
- اشتراكات نشرة بلا فتح ثلاث رسائل متتالية.

القاعدة المُلزمة: "Engagement metric must be paired with a downstream conversion ≥ 1." راجع `docs/revenue_marketing/anti_vanity_rules.md`.

---

## Content Factory (EN)

Dealix content is not written for reach. It is written to tie to an offer, be measured by a conversion, and be re-deployed as an asset. Every piece answers four questions before publication: who is the audience? what offer does it lead to? what is the success metric? what asset will it become after 30 days?

### The Ten Pillars

| Pillar | Three Angles (EN) | Offer | Audience | CTA |
|--------|--------------------|--------|----------|-----|
| 1. AI brings revenue | "Three ways your team loses revenue today from ungoverned AI" / "How we tied one market signal to a deal in 14 days" / "The closed revenue loop: signal to asset" | Revenue Hunter Pilot | B2B revenue leaders | "Start the pilot for 999 SAR" |
| 2. AI needs governance | "Why 93% of teams use GenAI without an evidence ledger" / "Permission Matrix before deploy: a template" / "How to write an executive AI governance report" | AI Trust Kit | CIO, CTO, CISO | "Book the AI Trust Diagnostic" |
| 3. AI agents for companies | "One governed agent > 10 ungoverned scripts" / "How to hand off an AI agent to a non-technical owner" / "When to kill an agent and when to scale it" | Governance OS | Operations teams | "Book exec discussion" |
| 4. Saudi / Arabic examples | "Diagnostic of the Saudi construction sector: signals, pain, offer" / "How food sector handles demand variability with governed AI" / "AI in Saudi tourism: real use cases" | Market Radar Subscription | Strategy teams | "Subscribe to Radar" |
| 5. Founder productivity | "30 daily minutes to run your revenue funnel with governed AI" / "The weekly founder operating system" / "Three AI tools founders use without leaking data" | Monthly Revenue Command | Founders | "Start Monthly Command" |
| 6. Revenue systems | "Numbers your CRM hides from you" / "Money Quality Score: one metric that tells the truth" / "How to tie every content piece to actual revenue" | Monthly Revenue Command | Sales leaders | "Book metrics glossary session" |
| 7. Agencies / White-label partners | "How your agency delivers AI services without an engineering team" / "A white-label client report in 60 minutes" / "Commission structure for AI partners in Saudi" | Agency White-label Kit | Agencies | "Request the kit" |
| 8. Case stories | "Before / Action / Output / Outcome: the story template" / "How to tell a story without overclaims" / "One asset from one story: scaling impact" | Case Study Template | All audiences | "Download the case template" |
| 9. Market radar | "Five Saudi signals that change your strategy this quarter" / "How a regulatory event becomes a campaign in 12 steps" / "Market Radar report TOC" | Market Radar Subscription | Strategy teams | "Request sample report" |
| 10. Trust and compliance | "Dealix charter: things we never say" / "Evidence Pack: what an AI decision audit looks like" / "MCP Risk Review: pre-launch checklist" | AI Trust Kit | Executives | "Book kit session" |

### Content Card Template

Use this table before writing any piece. Writers do not start without a completed card.

| Field | Description | Example |
|-------|-------------|---------|
| `pillar_id` | Pillar number 1–10 | 2 |
| `title_ar` | Arabic title ≤ 12 words | "لماذا 93% من فرق العمل يستخدمون GenAI بلا سجل أدلة" |
| `title_en` | English title ≤ 12 words | "Why 93% of teams use GenAI without an evidence ledger" |
| `audience` | Specific audience | Saudi CIO |
| `pain_addressed` | Pain in one sentence | "We don't know who uses AI or what it outputs" |
| `offer_id` | Offer it leads to | ai_trust_kit |
| `channel_primary` | First channel | LinkedIn long-form |
| `channel_secondary` | Second channel | Email newsletter |
| `cta_ar` | Arabic CTA | "احجز AI Trust Diagnostic" |
| `cta_en` | English CTA | "Book AI Trust Diagnostic" |
| `success_metric` | The single metric | Diagnostic bookings within 14 days |
| `kill_threshold` | Kill bar | < 1 booking per 1,000 impressions |
| `evidence_required` | Required proof before publish | Source for 93% claim + Permission Matrix template |
| `asset_after_30d` | Final asset | Downloadable checklist |

### Anti-Vanity Rules

The following metrics never count alone. Each must be paired with a downstream conversion of at least one:

- Likes and followers.
- Video views without subscription.
- Impressions without clicks.
- Clicks without bookings.
- Shares without qualitative comments.
- Newsletter subscriptions without three consecutive opens.

The binding rule: "Engagement metric must be paired with a downstream conversion ≥ 1." See `docs/revenue_marketing/anti_vanity_rules.md`.

---

**Disclosure / إفصاح:** Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.

Cross-links: `docs/revenue_marketing/offers_ladder.md`, `docs/revenue_marketing/message_variants.md`, `docs/revenue_marketing/anti_vanity_rules.md`.
