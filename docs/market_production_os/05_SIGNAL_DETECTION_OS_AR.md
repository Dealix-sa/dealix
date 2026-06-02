# Signal Detection OS — كشف إشارات الشراء — Signal Detection OS

> الموضع في العمود الفقري: المكوّن الخامس في طبقة *Market Production OS*.
> راجع [`00_MARKET_PRODUCTION_OS_MASTER_AR.md`](00_MARKET_PRODUCTION_OS_MASTER_AR.md) §4، ويُغذّي مباشرةً
> عامل `pain_signal` في [`04_PROSPECT_RESEARCH_OS_AR.md`](04_PROSPECT_RESEARCH_OS_AR.md).

هذا المستند يحوّل **الملاحظات العامة إلى إشارات شراء موثّقة**، ويربط كل إشارة بعرض من السلّم
الخماسي وبزاوية رسالة محترمة. الإشارة ليست تخمينًا — هي حدث عام موثّق له `evidence_ref`.
المبدأ: **كل إشارة تحمل مصدرًا ومعنى وعرضًا مطابقًا**، وإلا فهي ضوضاء تُهمَل.

> تنبيه عقيدي: كشف الإشارة **يدوي أو من ويب عام أو من مصدر معلن**. لا scraping، ولا أتمتة
> LinkedIn، ولا سحب آلي. الإشارة تُسجَّل لرفع جودة التخصيص، لا لتبرير تواصل بارد جماعي.

---

## 1. أنواع الإشارات وزاوية الرسالة

الزاوية الموحّدة لكل إشارة وظيفية: **«لاحظت أنكم تبحثون عن [role]… Dealix لا يستبدل الشخص بل
يجهّز له operational layer».** الرسالة تساعد الدور لا تنافسه — هذا فارق التموضع الأساسي.

### 1.1 إشارات الوظائف (Job Signals)

إعلان توظيف عام = دليل على ألم تشغيلي قابل للقياس:

| الدور المُعلَن | المعنى (الألم) | العرض المطابق من السلّم | زاوية الرسالة |
|---|---|---|---|
| `Sales Ops` | عمليات بيع تحتاج هيكلة بيانات وقرار | الدرجة 1: 7-Day Revenue Intelligence Sprint | «لاحظت أنكم تبحثون عن Sales Ops — Dealix يجهّز operational layer للبيانات والقرار قبل/مع التعيين» |
| `CRM Manager` | بيانات CRM غير منظّمة، قرارات بطيئة | الدرجة 2: Data-to-Revenue Pack | «بناء CRM يحتاج طبقة قرار — Dealix يكمّل لا يستبدل المدير» |
| `Marketing Coordinator` | حملات بلا قياس إيراد واضح | الدرجة 1 ثم 2 | «نجهّز قياس الإيراد خلف الحملات، والمنسّق يقودها» |
| `Customer Support` / `Support Lead` | حجم ردود يكشف تدفّق عملاء فعليًا | الدرجة 1 (تشخيص) | «حجم الدعم إشارة تدفّق — نحوّله لذاكرة إيراد قابلة للتدقيق» |
| `Growth` / `RevOps` | نية توسيع منظّم للإيراد | الدرجة 2–3 | «طبقة RevOps مع Decision Passport — الشخص يقود، النظام يوثّق» |

> المخطط: `schemas/job_signal.schema.json`. كل job_signal يُربط بـ prospect قائم، ويرفع
> `pain_signal` و`personalization_signal` بحسب قوة الدليل (ليس تلقائيًا — مدعوم بأدلة).

### 1.2 إشارات الموقع (Website Signals)

| الإشارة | المعنى | العرض المطابق |
|---|---|---|
| نموذج تسجيل/طلب عرض سعر نشط | تدفّق inbound قائم بلا طبقة قرار | الدرجة 1: تشخيص |
| متجر/حجز إلكتروني | حجم معاملات → بيانات قابلة للتحويل لإيراد | الدرجة 2: Data-to-Revenue Pack |
| دعم متعدد القنوات (chat/تذاكر) | بيانات تفاعل غير مستثمَرة | الدرجة 2–3 |
| غياب CRM واضح مع تدفّق عالٍ | فجوة عملياتية ظاهرة | الدرجة 1 ثم 3 |

### 1.3 إشارات المحتوى (Content Signals)

| الإشارة | المعنى | العرض المطابق |
|---|---|---|
| منشور عام عن «صعوبة تتبّع المبيعات/الإيراد» | ألم مُصرَّح به علنًا | الدرجة 1 — زاوية مباشرة على الألم |
| إعلان توسّع/فرع جديد عام | نمو يحتاج عمليات تتّسع معه | الدرجة 2–3 |
| ندوة/محتوى عن النمو أو البيانات | اهتمام مؤسسي بالموضوع | الدرجة 1: تشخيص |

### 1.4 صفحة وظائف نشطة (Active Careers Page)

صفحة توظيف عامة نشطة بأدوار بيع/عمليات/دعم = إشارة مركّبة قوية. تُعامَل كـ job_signal مجمّع
وترفع `likely_lead_flow` (نمو الفريق التجاري دليل على تدفّق متوقّع).

### 1.5 إطلاق حملة/خدمة (Campaign / Service Launch)

| الإشارة | المعنى | العرض المطابق |
|---|---|---|
| إطلاق خدمة/منتج جديد عام | حاجة لقياس إيراد الإطلاق | الدرجة 1: 7-Day Sprint |
| حملة تسويقية كبيرة معلنة | تدفّق leads متوقّع يحتاج طبقة قرار | الدرجة 2: Data-to-Revenue Pack |
| دخول قطاع/سوق جديد معلن | عمليات جديدة بلا ذاكرة إيراد | الدرجة 3: Managed Revenue Ops |

---

## 2. كائن Company Signal — الحقول

المخطط: `schemas/company_signal.schema.json` (قيد البناء). يجمع الإشارات غير الوظيفية على مستوى الشركة:

```json
{
  "signal_id": "string",
  "prospect_id": "string",
  "signal_type": "website|content|careers_page|campaign_launch|service_launch|expansion",
  "observed_at": "ISO-8601 date",
  "source": "public_web_manual|founder_supplied|inbound|linkedin_company_search",
  "source_passport_id": "string",
  "evidence_ref": "string",
  "meaning": "string",
  "matched_offer_tier": "0|1|2|3|4|enterprise",
  "message_angle": "string",
  "personalization_uplift": "P0|P1|P2|P3|P4",
  "confidence": "low|medium|high",
  "governance_decision": "string|null"
}
```

كائن `job_signal` مماثل في `schemas/job_signal.schema.json` مع `role`, `seniority`,
`posting_url_ref`, و`pain_mapping`.

---

## 3. قواعد التحويل من إشارة إلى تخصيص

- **إشارة واحدة موثّقة → P2** على الأقل (ألم من موقع/وظيفة/محتوى).
- **إشارة حديثة (آخر 30–60 يومًا) → P3** (trigger حديث).
- **إشارة + proof/offer مخصص للقطاع → P4.**
- **بلا إشارة موثّقة** → تبقى P1 كحد أقصى (شركة+قطاع فقط).

> هذه القواعد تربط طبقة الإشارات بعامل `personalization_signal` في المقياس. لا تُرفع المستويات
> بالتخمين؛ كل ارتفاع يحتاج `evidence_ref` قابلًا للتدقيق.

---

## 4. ما لا تفعله طبقة الإشارات (Out of Scope)

- لا تكتب رسائل ولا ترسلها — تنتج `message_angle` فقط كمادة خام للمصنع.
- لا تجمع PII (أسماء/بريد/جوال) — تسجّل دورًا عامًا وملاحظة، لا هوية شخصية.
- لا تستنتج «نية شراء مؤكدة» — كل إشارة احتمالية، والثقة (`confidence`) معلنة دائمًا.
- لا ادعاء بنتيجة: الإشارة ترفع الأولوية، لا تَعِد بصفقة.

---

## 5. الربط مع الطبقات الأخرى

- المدخل: prospects بحالة `researched`/`qualified` من [`04_PROSPECT_RESEARCH_OS_AR.md`](04_PROSPECT_RESEARCH_OS_AR.md).
- النواة المعاد استخدامها: `revenue_os/signal_normalizer` + `radar_events` + `market_intelligence`.
- المخرج: يرفع `pain_signal` و`personalization_signal`، ويُمرَّر إلى [`06_COLD_EMAIL_DRAFT_FACTORY_AR.md`](06_COLD_EMAIL_DRAFT_FACTORY_AR.md).
- العروض: السلّم الخماسي في المرجع الرئيسي §5 — لا تخترع عرضًا خارجه.

---

## EN summary

`Signal Detection OS` is the fifth Market Production OS component. It converts **public,
documented observations into buying signals**, each carrying a source, an evidence reference, a
meaning, and a matched offer tier from the five-step ladder. Job signals (Sales Ops, CRM Manager,
Marketing Coordinator, Support roles, Growth/RevOps), website signals, content signals, an active
careers page, and campaign/service launches each map to a specific offer and a respectful message
angle: *"I noticed you're hiring for [role] — Dealix doesn't replace the person, it prepares an
operational layer for them."* Detection is manual or public-web only — no scraping, no LinkedIn
automation, no automated contact pulling. One documented signal lifts personalization to P2, a
recent trigger to P3, and a sector-specific proof/offer to P4; nothing rises without an evidence
reference. This layer never writes or sends messages and stores no PII — it produces a
`message_angle` as raw material for the factory. Schemas: `schemas/job_signal.schema.json` and
`schemas/company_signal.schema.json`.

> القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.
