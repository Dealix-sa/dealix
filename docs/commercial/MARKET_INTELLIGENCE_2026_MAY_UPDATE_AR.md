# تحديث استخبارات السوق — مايو 2026

> **الغرض:** تحديث تنفيذي شهري يربط أحدث تطورات السوق السعودي (PDPL، Vision 2030 AI، التسعير، الامتثال) بقرارات Dealix اليومية. **ليس** بحثاً نظرياً — كل فقرة تنتهي بـ "ماذا يعني لـ Dealix هذا الأسبوع".

- **تاريخ التحديث:** 2026-05-24
- **مصدر الحقيقة:** بحث ويب مباشر + مصادر أُولية (SDAIA, Vision 2030, IAPP, Clyde & Co)
- **يكمّل:** [MARKET_INTELLIGENCE_MASTER_INDEX_AR.md](MARKET_INTELLIGENCE_MASTER_INDEX_AR.md) — لا يستبدل المحاور السبعة
- **مرتبط بـ:** [FOUNDER_PDPL_COMPLIANCE_PASS_AR.md](FOUNDER_PDPL_COMPLIANCE_PASS_AR.md) · [MARKET_INTELLIGENCE_PDPL_ENFORCEMENT_2026_AR.md](MARKET_INTELLIGENCE_PDPL_ENFORCEMENT_2026_AR.md)

---

## 1) PDPL أصبح ساري الإنفاذ — هذا يغيّر اللعبة

**الواقع (مصادر أولية):**

- SDAIA أصدرت **48 قرار إنفاذ** حتى منتصف يناير 2026 — لم تعد فترة "تطبيق ناعم".
- **الغرامات حتى 5 مليون ريال** لكل مخالفة، **تتضاعف** عند التكرار.
- **مخالفات سعودية شائعة وردت صراحة في قرارات الإنفاذ:**
  1. معالجة بيانات بدون أساس قانوني صحيح
  2. كشف بيانات شخصية بدون تخويل
  3. غياب الضمانات التقنية والتنظيمية
  4. **إرسال اتصالات تسويقية بدون موافقة موثّقة** ← هذا الأهم لنا
- مهلة الرد بعد إخطار SDAIA: **5 أيام عمل فقط**.
- المخالفات المتعمّدة أو المتكررة على بيانات حساسة → ملاحقة جنائية + سجن حتى سنتين.
- التسجيل إلزامي في **منصة حوكمة البيانات الوطنية** لكل من: الجهات العامة، معالجي البيانات الحساسة، ناقلي البيانات عبر الحدود، معالجي بيانات الأطفال والفئات الضعيفة.

**ماذا يعني لـ Dealix هذا الأسبوع:**

1. **"لا cold outreach" تحوّل من سياسة داخلية إلى قيمة عميل قابلة للبيع** — كل صفقة جديدة يمكن تأطيرها كـ "نحميك من غرامة 5M ريال".
2. **بطاقة الاعتراضات** (`objection_engine_registry.yaml`) يجب أن تتضمن سؤالاً مباشراً عن PDPL — وكيل dealix-content يضيف 5 اعتراضات جديدة بالتوازي.
3. **كل warm-list draft** يصدر اليوم يحتاج حقل `consent_on_file=yes` — وإلا يُرفض من سكربت `warm_list_outreach.py`.
4. **خانة DPA** في كل عقد عميل: المرجع [MARKET_INTELLIGENCE_PDPL_LEGAL_REVIEW_AR.md](MARKET_INTELLIGENCE_PDPL_LEGAL_REVIEW_AR.md).
5. **التسجيل في منصة حوكمة البيانات الوطنية:** Dealix شركة تعالج بيانات عملاء B2B — قد لا تكون "حساسة" بمعنى PDPL لكن **النقل عبر الحدود** (لو استضافة خارج المملكة) يُلزم التسجيل. → **قرار مؤسس مطلوب هذا الأسبوع**: هل نسجّل الآن استباقاً، أم ننتظر أول عميل enterprise؟

**أدلة (Sources):**
- [Saudi PDPL enforcement live (Clyde & Co)](https://www.clydeco.com/en/insights/2026/03/enforcement-of-the-saudi-pdp-law)
- [SDAIA active enforcement (Global Privacy Blog)](https://www.globalprivacyblog.com/2026/05/active-enforcement-of-saudi-arabia-privacy-regime-implications-for-businesses/)
- [IAPP — Saudi PDPL first anniversary](https://iapp.org/news/a/saudi-pdpl-s-first-anniversary-amendments-enforcement-and-ongoing-developments)
- [SDAIA — Data Protection Law](https://sdaia.gov.sa/en/Research/Pages/DataProtection.aspx)

---

## 2) سوق الذكاء الاصطناعي السعودي — أرقام تدعم Why Now

**الواقع (مصادر متعددة، تختلف في الحجم لكن تتفق على الاتجاه):**

| مقياس | القيمة 2025 | الهدف/التوقع |
|------|------------|---------------|
| حجم سوق AI السعودي | 1.24 – 2.14 مليار $ | 4.37 – 16.9 مليار $ بحلول 2032/34 |
| CAGR | — | 15% – 34% (حسب التقرير) |
| استثمار Vision 2030 في AI infra + talent | **20+ مليار $** | — |
| مساهمة AI في الناتج المحلي (هدف 2030) | — | **50 مليار $** |
| متخصصو AI/Data (هدف) | — | 20,000 |
| ستارت-أبس AI نشطة (هدف) | — | 300+ |
| قطاع Sales & Marketing AI (2025) | **580 مليون $** | الأكبر بين القطاعات |
| قطاع تكنولوجيا الذكاء الاصطناعي (CAGR متوقع) | — | **38.4%** — الأسرع نمواً |

**ماذا يعني لـ Dealix هذا الأسبوع:**

- **ICP صحيح:** SMEs السعودية تبدأ فعلياً استكشاف AI لـ **customer retention, pricing, ops planning** — هذه بالضبط فئة Dealix (RevOps + Sales Intelligence).
- **زاوية "Vision 2030 alignment"** صالحة في عروض المؤسسات الكبيرة والشراكات الحكومية.
- **القطاع الأسرع نمواً (Sales/Marketing AI 38.4%)** يطابق Free Diagnostic → Sprint → Managed Ops ladder.
- **عقبة معروفة:** "ندرة المواهب المحلية + تفاوت جاهزية المؤسسات التقليدية" → **خدمة Dealix الإدارية (Managed Ops) تحلّ هذه العقبة مباشرة** — لا حاجة لتوظيف Data Scientist محلي.

**أدلة:**
- [Saudi AI Market Report 2025–2032 (MarketsandMarkets)](https://www.marketsandmarkets.com/Market-Reports/saudi-arabia-artificial-intelligence-market-160864989.html)
- [Vision 2030 official](https://www.vision2030.gov.sa/en)
- [Trade.gov Saudi digital economy](https://www.trade.gov/country-commercial-guides/saudi-arabia-digital-economy-0)

---

## 3) معيار التسعير — Dealix أرخص من جميع البدائل (لـ SME)

**بحث السوق السعودي لاستشارات AI (2026):**

| نوع الالتزام | سعر السوق |
|-------|---------|
| Use Case Assessment / Discovery Roadmap | **25,000 – 150,000 ريال** |
| Proof-of-Concept (case واحد) | **200,000 – 400,000 ريال** |
| تكاملات أساسية API | 20,000 – 50,000 ريال |
| مشروع ChatGPT/AI كامل | 100,000 ريال إلى نصف مليون+ |

**سلم Dealix الحالي (5 درجات):**

| الدرجة | السعر | ما يحصل عليه العميل |
|--------|------|---------------------|
| Free Diagnostic | 0 | جلسة 15 دقيقة + ICP Match snapshot |
| Sprint | **499 ريال** | تشخيص أسبوع + Proof Pack |
| Data Pack | **1,500 ريال** | استخبارات حساب + توصيات تنفيذ |
| Managed Ops | **2,999 – 4,999 ريال/شهرياً** | تشغيل + حوكمة + تقارير |
| Custom AI | **5,000 – 25,000 ريال** | حلول مخصصة بعقد |

**ماذا يعني لـ Dealix هذا الأسبوع:**

- **Sprint 499 ريال = 5% من أرخص بديل سوقي** (5000/25000 = 0.2 = 20%؛ Sprint أقل بكثير). هذا **ليس تسعيراً منخفضاً عن طريق الخطأ** — هذا قرار استراتيجي لكسر حاجز الدخول SME.
- **Managed Ops 2,999–4,999 شهرياً** = 36K–60K ريال سنوياً → يضع Dealix في موقع "أرخص من توظيف بائع متخصص واحد" (راتب سعودي متوسط لـ Sales Ops Manager ~ 12K–18K شهرياً).
- **لا يوجد سبب** لرفع السعر قبل **3 صفقات مغلقة + 3 case studies منشورة بموافقة العميل**.
- **تحذير doctrine:** لا تنخدع بمقارنة "السوق يبيع بـ 100K، نحن بـ 499" — الـ 499 SAR Sprint **مصمم** كرافعة لكسر no-build gate، ليس نموذجاً مستداماً للإيراد. الإيراد المستدام = Managed Ops + Custom AI.

**أدلة:**
- [AI Consulting Cost UAE/Saudi 2026 (Suffescom)](https://www.suffescom.com/blog/ai-consulting-services-cost)
- [Best Gen-AI Firms for Saudi SMEs (Competenza)](https://competenza.ae/blog/generative-ai-consulting-firms-saudi-arabia-smes/)
- [AI App Development Cost Saudi 2026 (Cmarix)](https://www.cmarix.com/blog/ai-app-development-cost-in-saudi-arabia/)

---

## 4) WhatsApp / LinkedIn Outreach — قواعد 2026 الجديدة

**الواقع:**

- **WhatsApp يُلزم opt-in صريح موثّق** (نص الموافقة + ختم زمني + قناة الجمع). الموافقة الضمنية في T&Cs **لا تكفي**.
- **حدود محفظة WhatsApp (تبدأ 15 يناير 2026):** بداية 100K مستخدم/يوم لتمبليتات outbound، توسّع آلي كل 6 ساعات حسب engagement quality.
- **زر إلغاء اشتراك** يجب أن يكون **بنفس سهولة الاشتراك** (مثلاً: رد "STOP" → إلغاء فوري + تأكيد).
- **LinkedIn:** نفس معاملة البريد — opt-in مزدوج موصى به، التركيز على intent-scored leads فقط.
- **Saudi PDPL** يفرض حفظ سجل الموافقات: متى، كيف، من أي قناة، نص الموافقة الفعلي.

**ماذا يعني لـ Dealix هذا الأسبوع:**

1. **لا يوجد ولن يوجد** integration مع WhatsApp Business API لإرسال آلي — Dealix يولّد drafts فقط، المؤسس يرسل يدوياً من رقمه الشخصي إلى **علاقات warm مسبقة فقط**.
2. **حقل `consent_on_file`** في كل سجل warm-list = شرط قبل ظهور أي draft (وكيل dealix-sales يطبّق هذه القاعدة هذا الأسبوع).
3. **`approval_center`** هو البوابة الوحيدة لأي رسالة — لا exception.
4. **سجل موافقات منفصل** عند إطلاق نموذج العميل الذاتي (PLS): جدول `consent_records` (channel, content_id, timestamp, opt_in_text_version, source_url) — هذا **بناء لاحق** بعد Phase 0-1 unlock.

**أدلة:**
- [WhatsApp Business API Compliance Saudi 2026 (GMCS)](https://gmcsco.com/whatsapp-business-api-compliance-saudi-arabia-2026/)
- [Meta — Get opt-in for WhatsApp](https://developers.facebook.com/documentation/business-messaging/whatsapp/getting-opt-in)
- [PDPL-compliant SMS messaging (Unifonic)](https://www.unifonic.com/en/resources/how-and-when-to-collect-consent-a-guide-to-pdpl-compliant-practices-for-business-sms-messaging)

---

## 5) المشهد التنافسي السعودي — أين يقف Dealix

**اللاعبون المحليون والإقليميون:**

| اللاعب | الفئة | نقطة الفصل عن Dealix |
|--------|------|----------------------|
| PACT Revenu CRM | CRM محلي سعودي | CRM فقط — لا يقدّم RevOps managed service ولا حوكمة AI |
| SAS / SAP / IBM | منصات مؤسسات كبيرة | أسعار 6 أرقام، تنفيذ 6–18 شهر، لا تناسب SME |
| Tableau / Qlik | تحليلات | تحتاج Data Engineer داخلي |
| ChatGPT consultancies المحلية | استشارات AI | مشاريع 100K–500K بدون حوكمة أو إثبات قيمة قابل للتدقيق |
| Bilytica / Symloop | تنفيذ AI | لا يربطون AI بـ Sales Pipeline قابل للقياس |

**سوق CRM السعودي:**

- 741M $ في 2025 → 1.78 مليار $ بحلول 2035 (CAGR 9.2%).
- قطاع Sales & Marketing AI داخل سوق AI الكلي = **580M $ في 2025** — الأكبر.

**ماذا يعني لـ Dealix هذا الأسبوع:**

- **التموضع الفائز ليس "بديل CRM"** — هو **"طبقة استخبارات وتشغيل فوق CRM موجود"** (HubSpot/Pact/Salesforce). هذا يمنعنا من المعركة المباشرة مع PACT أو SAP.
- **القيمة المختلفة:** PDPL-first + Trust Plane + Decision Passport + Capital Asset Registry — لا يوجد لاعب محلي يقدّمها مجتمعة.
- **خطر تموضع:** إذا تموضعنا كـ "RevOps tool"، نفقد الجزء الأهم — Dealix هو **نظام دلائل revenue يحوّل كل لمسة عميل إلى أصل قابل للتدقيق وإعادة الاستخدام**.
- **بطاقة المعركة الحالية** ([MARKET_INTELLIGENCE_CATEGORY_BATTLECARD_AR.md](MARKET_INTELLIGENCE_CATEGORY_BATTLECARD_AR.md)) تحتاج صف "PACT Revenu" + "SAP RevOps" لتكتمل — **يضاف بعد التحديث القادم**.

**أدلة:**
- [Saudi CRM Market 2035 (Expert Market Research)](https://www.expertmarketresearch.com/reports/saudi-arabia-customer-relationship-management-market)
- [PACT Revenu CRM](https://pactsoft.sa/products/sales/)

---

## 6) قرارات المؤسس هذا الأسبوع (مرتبة)

> **3 قرارات فقط** — كل قرار يستهلك ≤ 20 دقيقة من تفكير المؤسس.

| # | قرار | بيانات داعمة | المُخرج المتوقّع |
|---|------|---------------|-------------------|
| 1 | هل نسجّل في منصة حوكمة البيانات الوطنية (SDAIA) استباقاً؟ | §1 — الإلزام يبدأ من النقل عبر الحدود. Dealix يستضيف على Railway (EU/US) → ينطبق | نعم/لا + تاريخ التسجيل في `founder_weekly_one_decision.yaml` |
| 2 | هل نضيف "PDPL-shield" كميزة بيع صريحة في صفحة الهبوط `/dealix-diagnostic`؟ | §1 — الزاوية تحوّلت من سياسة إلى قيمة عميل | نعم → ticket لـ dealix-engineer (يضاف في الموجة القادمة، بعد payment_received) |
| 3 | هل نرفع سقف Managed Ops من 4,999 إلى 7,499 بعد أول 3 صفقات؟ | §3 — هامش السوق ضخم؛ Sprint 499 يكفي للدخول | قرار يُسجل **بعد** Phase 0-1 unlock، ليس قبله |

> **قرار حالي مؤقت (لا يحتاج 20 دقيقة):** إعادة تقييم سلم التسعير ممنوع قبل 3 صفقات Managed Ops حقيقية. تثبيت الأسعار يحفظ التركيز.

---

## 7) قاعدة no-build مفعّلة

> ⚠️ هذا التحديث **بحث وتوثيق**. لا ميزات جديدة. لا APIs جديدة. لا تغيير معمار. التنفيذ التقني الوحيد المسموح هذا الأسبوع:
>
> 1. وكيل dealix-content يكتب 5 أقسام PDPL + 5 اعتراضات
> 2. وكيل dealix-sales يولّد drafts queue (لا إرسال)
> 3. وكيل dealix-delivery يلمّع Proof Pack template
> 4. وكيل dealix-engineer يضيف KPI placeholder guardrail + doctrine test
>
> أي شيء أكبر من ذلك يحتاج `payment_received` + `proof_pack_delivered` أولاً.

---

## 8) جدول تحقق

| سؤال | جواب |
|------|------|
| هل غيّر هذا التحديث الـ ICP؟ | لا — أكّده فقط |
| هل غيّر سلم التسعير؟ | لا — أكّد أنه تحت السوق بفارق صحي |
| هل غيّر التموضع؟ | نعم — PDPL-first أصبح زاوية بيع، ليس فقط سياسة |
| هل غيّر الإطلاق العام؟ | لا — `launch_mode=soft` يبقى |
| هل أضاف بناء؟ | لا — كل شيء كان موجوداً ضمن النموذج |

---

## 9) كيفية استخدام هذا الملف

- **يومياً (المؤسس):** اقرأ §6 (قرارات الأسبوع) فقط
- **أسبوعياً (Friday Scorecard):** أكّد أنه لم يطرأ تغيير على §1 (PDPL) — أي قرار إنفاذ جديد لـ SDAIA → حدّث الملف
- **عند كل اجتماع warm:** اقتبس §1 (الغرامات 5M) و §3 (Sprint 499) إذا اعتُرض على السعر
- **شهرياً:** اكتب نسخة `MARKET_INTELLIGENCE_2026_<MONTH>_UPDATE_AR.md` جديدة (لا تستبدل القديم — يبقى للسجل الزمني)

---

*المؤسس: قراءة هذا الملف لا تبدّل اجتماع مع محامٍ سعودي مرخّص متخصص في PDPL. هذا الملف بحث للقرار، ليس استشارة قانونية.*

*Generated: 2026-05-24 · Next review: 2026-06-21 · Source: web research + Vision 2030 + SDAIA enforcement registry*
