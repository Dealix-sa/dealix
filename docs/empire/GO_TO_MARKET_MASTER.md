<!-- LAYER: empire/doctrine | Owner: Founder | Bilingual AR+EN | draft_only -->
<!-- Part of the Dealix Operating Standard — see INDEX.md -->

# دليل الانتشار السوقي الرئيسي — Go-To-Market Master Playbook — استراتيجي وتكتيكي

> **AR:** هذه الوثيقة هي **دليل التشغيل الواحد** للانتشار السوقي. ما هو هنا يُنفَّذ؛ ما ليس هنا يُعتبر noise (per [`DEALIX_METHOD.md`](DEALIX_METHOD.md)).
> **EN:** This document is the **single operational GTM playbook**. What is here gets executed; what is not here is treated as noise.

> ⚠️ كل الأرقام أدناه **تقديرية للتخطيط** — معدّلات التحويل والإيراد ليست نتائج مضمونة. السعر المعتمد من [`../COMPANY_SERVICE_LADDER.md`](../COMPANY_SERVICE_LADDER.md). الأقفال من [`COMMERCIAL_GATES.md`](COMMERCIAL_GATES.md).
> **EN:** All figures below are planning estimates — conversion and revenue figures are not guaranteed outcomes.

---

## 0. كيف تُقرأ هذه الوثيقة / How to Read This

هذه الوثيقة لا تستبدل طبقة العقيدة — هي **تُركّبها في تنفيذ**. كل قسم يفترض أنك قرأت:
[`OFFER_LADDER.md`](OFFER_LADDER.md) · [`AGENCY_WEDGE.md`](AGENCY_WEDGE.md) · [`UNIT_ECONOMICS.md`](UNIT_ECONOMICS.md) · [`COMMERCIAL_GATES.md`](COMMERCIAL_GATES.md) · [`PARTNER_ECONOMY.md`](PARTNER_ECONOMY.md) · [`AUTHORITY_ENGINE.md`](AUTHORITY_ENGINE.md).

**EN:** This is not a replacement for the doctrine layer — it *assembles* it into execution. Each section assumes the doctrine docs above have been read.

السلم المرجعي لهذه الوثيقة — السلم التجاري بخمس درجات:

| الدرجة / Rung | العرض / Offer | السعر / Price |
|---|---|---|
| R0 | Free Diagnostic — التشخيص المجاني | مجاني / free |
| R1 | Revenue Intelligence Sprint — سبرنت ذكاء الإيراد | 499 SAR |
| R2 | Data-to-Revenue Pack — حزمة البيانات إلى الإيراد | 1,500 SAR |
| R3 | Managed Ops — التشغيل المُدار | 2,999–4,999 SAR/شهر |
| R4 | Custom AI — الذكاء الاصطناعي المخصّص | 5,000–25,000 SAR |

> R1 (499 SAR) هي المرساة الحية الوحيدة. R3 وR4 **مُغلقتان بقفل إثبات** — لا تُسعَّران علناً ولا تُباعان قبل تحقّق الشرط (per [`COMMERCIAL_GATES.md`](COMMERCIAL_GATES.md): لا retainer قبل scope، ولا custom قبل ≥3 paid pilots).

---

## 1. العميل المثالي والشرائح / ICP & Segments

### 1.1 من نلاحق بالضبط / Exactly Who We Pursue

**AR:** Dealix شريك تشغيل بالذكاء الاصطناعي للمنشآت الصغيرة والمتوسطة السعودية. العميل المثالي ليس «أي شركة» — هو منشأة لديها **اهتمام داخل وارد لا يتحوّل إلى إيراد**.

**EN:** Dealix is an AI Operating Partner for Saudi SMEs. The ICP is not "any company" — it is a business with **inbound interest that is not converting into revenue**.

| البُعد / Dimension | المواصفة / Specification |
|---|---|
| القطاعات / Sectors | وكالات تسويق ومزوّدو خدمات (الإسفين الأساسي) · عقارات وسيط · تجارة B2B وتوزيع · عيادات وخدمات صحية خاصة · مقاولات وخدمات هندسية صغيرة · تعليم وتدريب خاص |
| الحجم / Size | 5–60 موظفاً / 5–60 employees |
| نطاق الإيراد / Revenue band | ~2–30 مليون SAR سنوياً (تقديري) / ~SAR 2–30M annual (estimated) |
| البنية / Structure | فريق مبيعات أو خدمة عملاء قائم بالفعل (1–8 أشخاص) — يوجد leads ولا يوجد نظام متابعة محكوم |
| القناة الرقمية / Digital footprint | تنفق على إعلانات أو لديها وارد عضوي — أي يوجد **Signal** فعلي per [`DEALIX_METHOD.md`](DEALIX_METHOD.md) |
| صانع القرار / Decision-maker | المالك أو المدير العام أو مدير المبيعات — جهة واحدة تقرر، دورة بيع قصيرة |

### 1.2 محفّزات الشراء / Buying Triggers

العميل جاهز للشراء عند ظهور إشارة واضحة:

- إنفاق إعلاني مرتفع مع شكوى صريحة «الـleads ما تتحول» — high ad spend, low conversion complaint.
- توظيف موظف مبيعات جديد — سياق ألم متابعة واضح / new sales hire.
- موسم ذروة قادم (رمضان، نهاية السنة المالية، موسم القطاع) — peak season pressure.
- وكالة فقدت عميلاً بسبب «ما نعرف وش صار بعد الـlead» — agency churn from attribution gap.
- مالك قال صراحةً «نبي نستخدم AI بس ما ندري وش» — explicit AI intent without a plan.

### 1.3 العميل المضاد — من **لا** نلاحق / Anti-ICP

> هذه قائمة رفض. إذا ظهر عميل من هنا — نقول لا بأدب ونحيله، لا نخفض السعر له (per [`OFFER_LADDER.md`](OFFER_LADDER.md): لا تخفض السعر — خفّض النطاق).

- ❌ منشآت بلا leads أصلاً — Dealix يثبت ما حدث بعد الاهتمام، لا يخلق الاهتمام من الصفر.
- ❌ شركات تطلب scraping أو قوائم مشتراة أو رسائل آلية باردة — يخالف [`NON_NEGOTIABLES`](../00_constitution/NON_NEGOTIABLES.md).
- ❌ مؤسسات حكومية أو enterprise كبيرة — دورة شراء طويلة، تخالف قفل [`COMMERCIAL_GATES.md`](COMMERCIAL_GATES.md) (لا enterprise قبل repeatability).
- ❌ منشآت تطلب «ضمان مبيعات» كشرط — نحن نبيع **فرص مُثبتة بأدلة**، لا أرقام مضمونة.
- ❌ شركات بلا صانع قرار واضح — لجان، أكثر من ثلاث جهات اعتماد.
- ❌ عملاء يريدون منتج SaaS جاهز اليوم — المنتج مُغلق بقفل [`PRODUCTIZATION_PATH.md`](PRODUCTIZATION_PATH.md) (لا SaaS قبل 3 retainers).
- ❌ شركات ناشئة pre-revenue — لا اقتصاد وحدة يحتمل R2/R3.

**EN — Anti-ICP:** Businesses with no leads at all; anyone asking for scraping, purchased lists, or cold automation; government/large enterprise; anyone demanding a sales guarantee; no clear decision-maker; buyers wanting finished SaaS today; pre-revenue startups.

---

## 2. التموضع والفئة / Positioning & Category

### 2.1 الوعد في جملة واحدة / The One-Sentence Promise

> **AR:** «Dealix شريك تشغيل بالذكاء الاصطناعي يثبت ماذا حدث بعد كل lead — ويحوّل الاهتمام المُهدر إلى فرص إيراد مُثبتة بأدلة، خلال أيام لا أشهر.»
> **EN:** "Dealix is an AI Operating Partner that proves what happened after every lead — turning wasted interest into evidence-backed revenue opportunities, in days not months."

### 2.2 الإسفين / The Wedge

الإسفين ليس «منصة AI» — هو **عرض صغير لا يُرفَض**: R0 التشخيص المجاني ثم R1 سبرنت 499 SAR على 10 leads فقط. صغير بما يكفي لاتخاذ القرار اليوم، ومُثبِت بما يكفي لفتح الدرجة التالية. (per [`AGENCY_WEDGE.md`](AGENCY_WEDGE.md): «خلّونا نجرّب على عميل واحد فقط».)

**EN:** The wedge is not an "AI platform" — it is a small un-rejectable offer: free R0 diagnostic, then the 499 SAR R1 sprint on 10 leads only. Small enough to decide today, proof-rich enough to unlock the next rung.

### 2.3 لماذا الآن / Why Now

- المنشآت السعودية تزيد إنفاقها الرقمي بينما تبقى المتابعة يدوية فوضوية — الفجوة تتسع.
- موجة «نبي AI» وصلت السوق المتوسط — لكن العرض الموجود إما استشارات نظرية غالية أو أدوات بلا حوكمة.
- رؤية 2030 ترفع توقّع الكفاءة التشغيلية والحوكمة — Dealix يتموضع كـ**معيار تشغيل محكوم** لا كأداة.

### 2.4 التباين التنافسي / Competitive Contrast

| البُعد / Dimension | استشارات AI العامة / Generic AI Consulting | Dealix |
|---|---|---|
| المخرج / Output | شرائح وتوصيات / slide decks | Proof Pack بأدلة مُسجّلة خلال 48 ساعة |
| الالتزام الأول / First commitment | عقد كبير / large engagement | R0 مجاني ثم 499 SAR |
| الإثبات / Proof | وعود / promises | عمل حقيقي على 10 leads فعلية |
| الحوكمة / Governance | غائبة / absent | موافقة بشرية قبل أي إرسال خارجي |
| الادعاءات / Claims | «نضاعف مبيعاتك» | «فرص مُثبتة بأدلة» — لا ضمان أرقام |
| التوسّع / Expansion | إعادة بيع عقد / re-sell | سلم درجات مُثبت ([`OFFER_LADDER.md`](OFFER_LADDER.md)) |

> **القاعدة:** لا نبيع «AI». نبيع **ماذا حدث بعد الـlead**، مُثبَتاً بدليل.

---

## 3. مزيج القنوات / Channel Mix

أربع قنوات، مرتّبة بالأولوية لأول 90 يوماً. الترتيب مقصود — لا توزّع جهداً متساوياً.

### القناة 1 (الأولوية القصوى) — تواصل دافئ يقوده المؤسس / Founder-Led Warm Outreach

شبكة المؤسس المباشرة: عملاء سابقون، زملاء، إحالات شخصية، علاقات قطاعية. **دافئ أولاً** — كل لمسة لها Source معروف وOwner معروف (per [`DEALIX_METHOD.md`](DEALIX_METHOD.md)). تنفّذ عبر Commercial Proof Loop: 10 لمسات بشرية معتمدة يومياً.

### القناة 2 — حركة الشركاء عبر إسفين الوكالات / The Agency-Wedge Partner Motion

الوكالات ومزوّدو الخدمات هم الإسفين الأساسي ([`AGENCY_WEDGE.md`](AGENCY_WEDGE.md)) — كل وكالة = عميل + موزّع + مصدر إحالات. تفاصيل التنفيذ في القسم 7.

### القناة 3 — محرّك السلطة والمحتوى / Authority & Content Engine

كل Proof Pack يتحوّل إلى authority asset ([`AUTHORITY_ENGINE.md`](AUTHORITY_ENGINE.md)): insight مُجهّل → منشور LinkedIn → نشرة → أصل شريك. **محتوى من واقع لا من تنظير.** يبني الثقة قبل المكالمة ويغذّي القناة 4.

### القناة 4 — الوارد من الموقع / Inbound from the Landing Site

الموقع يحوّل الزائر إلى R0 (تشخيص مجاني). يبدأ صغيراً ويكبر مع نضج محرّك المحتوى. لا يُعتمد عليه كقناة أساسية في أول 90 يوماً.

### ترتيب أول 90 يوماً / 90-Day Channel Ranking

| الترتيب / Rank | القناة / Channel | حصة الجهد / Effort share | لماذا / Why |
|---|---|---|---|
| 1 | تواصل دافئ يقوده المؤسس | ~50% | أسرع طريق إلى أول paid pilots ودليل |
| 2 | حركة الشركاء (إسفين الوكالات) | ~30% | يضاعف التوزيع لكل وكالة موقّعة |
| 3 | محرّك السلطة والمحتوى | ~15% | يبني ثقة مركّبة ويغذّي الوارد |
| 4 | الوارد من الموقع | ~5% | يكبر لاحقاً؛ ليس رهان البداية |

**EN:** Four channels, priority-ranked. Warm founder-led outreach is the engine; the agency-wedge partner motion multiplies it; the authority engine compounds trust; inbound is a later bet. Effort is deliberately *not* spread evenly.

---

## 4. القمع والأهداف / Funnel & Targets

### 4.1 نموذج القمع / The Funnel Model

```text
Leads (touches)
  → R0 Free Diagnostic
    → R1 Sprint (499 SAR)
      → R2 Data-to-Revenue Pack (1,500 SAR)
        → R3 Managed Ops retainer (2,999–4,999 SAR/mo)
          → R4 Custom AI (5K–25K SAR)
```

معدّلات التحويل **تقديرية للتخطيط** (مُعايَرة من [`UNIT_ECONOMICS.md`](UNIT_ECONOMICS.md)) وتُعاد معايرتها من بيانات حقيقية في برج التحكم:

| الانتقال / Transition | المعدّل التقديري / Estimated rate |
|---|---|
| Leads → R0 Diagnostic | ~25–35% |
| R0 → R1 Sprint | ~25–35% |
| R1 → R2 Pack | ~30–40% |
| R2 → R3 Retainer | ~25–40% |
| R3 → R4 Custom AI | proof-gated — لا يُخطَّط له في أول 90 يوماً |

### 4.2 الأهداف الشهرية / Monthly Targets (Estimates)

> الأرقام تقديرية للتخطيط — ليست التزاماً ولا نتيجة مضمونة.

| المرحلة / Stage | الشهر 1 / M1 | الشهر 2 / M2 | الشهر 3 / M3 |
|---|---|---|---|
| Leads (touches معتمدة) | ~200 | ~220 | ~240 |
| R0 Free Diagnostic | ~24 | ~32 | ~40 |
| R1 Sprint (499 SAR) | ~6 | ~10 | ~14 |
| R2 Pack (1,500 SAR) | ~1 | ~3 | ~5 |
| R3 Retainer جديد (شهرياً) | 0 | ~1 | ~2 |
| شركاء موقّعون / partners signed | 1 | 2 | 2 |

### 4.3 حساب الإيراد / Revenue Math (Estimates)

| البند / Line | الشهر 1 / M1 | الشهر 2 / M2 | الشهر 3 / M3 |
|---|---|---|---|
| إيراد R1 — Sprints | 6 × 499 = ~2,994 | 10 × 499 = ~4,990 | 14 × 499 = ~6,986 |
| إيراد R2 — Packs | 1 × 1,500 = ~1,500 | 3 × 1,500 = ~4,500 | 5 × 1,500 = ~7,500 |
| إيراد R3 — Retainers (MRR تراكمي) | 0 | ~1 × 3,500 = ~3,500 | ~3 × 3,500 = ~10,500 |
| **إجمالي تقديري / Est. total** | **~4,494 SAR** | **~12,990 SAR** | **~24,986 SAR** |

> الافتراضات: متوسط retainer ~3,500 SAR/شهر (وسط نطاق R3)؛ R3 تراكمي لأنه MRR. R4 خارج خطة 90 يوماً (مُغلق بقفل ≥3 paid pilots per [`COMMERCIAL_GATES.md`](COMMERCIAL_GATES.md)).
> **EN:** Estimated 90-day exit run-rate ≈ SAR 25K/month blended — planning estimate, not a guaranteed result.

### 4.4 الهدف الحاكم لأول 90 يوماً / The Governing 90-Day Goal

> ليس الإيراد — بل **≥3 paid pilots مُسلَّمة مع Proof Pack** + **≥1 retainer حيّ**. هذا يفتح أقفال R3/R4 ويعيد معايرة سعر R1 (per [`OFFER_LADDER.md`](OFFER_LADDER.md)).

---

## 5. الإيقاع التشغيلي / Operating Rhythm

### 5.1 يومياً — المؤسس / Daily — Founder

Commercial Proof Loop (per [`AGENCY_WEDGE.md`](AGENCY_WEDGE.md) و[`COMMERCIAL_GATES.md`](COMMERCIAL_GATES.md)):

- 10 لمسات بشرية **معتمدة**: ~5 دافئة · ~3 بريد · ~1 LinkedIn (نشر/تفاعل لا automation) · ~1 محادثة شريك.
- ~5 follow-ups على لمسات سابقة.
- مراجعة كل مخرج خارجي قبل الإرسال — **موافقة بشرية إلزامية**.
- تسليم أي Proof Pack مُستحَق خلال 48 ساعة.
- تحديث برج التحكم: الرسائل، الردود، الـdemos، الفواتير ([`COMMERCIAL_CONTROL_TOWER.md`](COMMERCIAL_CONTROL_TOWER.md)).

### 5.2 يومياً — المحرّك الذاتي / Daily — The Autonomous Engine

- يقترح قائمة targets من ICP والإحالات الدافئة — **لا scraping، لا قوائم مشتراة**.
- يصيغ **مسودات** رسائل ومتابعات شخصية — تبقى مسودة حتى يعتمدها المؤسس.
- يجمع الأدلة في Proof Pack ويرصد فجوات الدليل.
- يرفع تنبيهات «risk» و«blocked» إلى البرج. لا يرسل شيئاً خارجياً تلقائياً.

> **القاعدة الحاكمة:** المحرّك **يقترح ويصيغ ويتتبّع**؛ المؤسس **يعتمد ويرسل**. لا إرسال خارجي بلا موافقة بشرية.

### 5.3 أسبوعياً / Weekly

- مراجعة البرج: أفضل شريحة، أفضل رسالة، أفضل عرض، أين توقف القمع، أي اعتراض تكرّر ([`COMMERCIAL_CONTROL_TOWER.md`](COMMERCIAL_CONTROL_TOWER.md)).
- قرار: ماذا نضاعف، ماذا نوقف، ماذا **لا** نبني.
- تحويل Proof Pack الأسبوع إلى ≥1 authority asset ([`AUTHORITY_ENGINE.md`](AUTHORITY_ENGINE.md)).
- متابعة شريك واحد على الأقل نحو pilot أو إحالة.
- فحص اقتصاد الوحدة: هل العرض يتحوّل للدرجة التالية؟ إن لا — طبّق قاعدة المراجعة في [`UNIT_ECONOMICS.md`](UNIT_ECONOMICS.md).

### 5.4 شهرياً / Monthly

- Board Pack: Revenue · Pipeline · Delivery · Partners · Governance · Learning · Next bet.
- مراجعة الأقفال: هل اقتربنا من ≥3 paid pilots؟ هل R3 جاهز للفتح؟
- إعادة معايرة معدّلات القمع من بيانات حقيقية.
- مراجعة الـAnti-ICP: من رفضنا ولماذا — هل القائمة دقيقة؟

---

## 6. تقويم الإطلاق 90 يوماً / 90-Day Launch Calendar

> أرقام التقويم تقديرية وتُعاد معايرتها أسبوعياً من البرج.

### الشهر 1 — الإثبات / Month 1 — Prove

- **الأسبوع 1:** تثبيت R0/R1، قوالب التواصل الدافئ، إعداد البرج. أول 10 لمسات/يوم. هدف: ~3 R0 محجوزة.
- **الأسبوع 2:** أول R0 مُسلَّمة. أول محادثتي شريك. هدف: ~2 R1 مدفوعة.
- **الأسبوع 3:** أول Proof Pack يُسلَّم خلال 48 ساعة → أول authority asset. أول شريك موقّع (referral).
- **الأسبوع 4:** ~6 R1 تراكمياً، أول R2. مراجعة شهرية أولى + إعادة معايرة.

### الشهر 2 — التكرار / Month 2 — Repeat

- **الأسبوع 5:** مضاعفة أفضل شريحة من بيانات الشهر 1. هدف: ~3 R1 جديدة.
- **الأسبوع 6:** أول scope لـR3 retainer. شريك ثانٍ موقّع.
- **الأسبوع 7:** أول R3 retainer حيّ (بعد scope مُثبت — قفل [`COMMERCIAL_GATES.md`](COMMERCIAL_GATES.md)). أول co-selling من شريك.
- **الأسبوع 8:** ~10 R1 تراكمياً، ~3 R2. مراجعة شهرية + Board Pack.

### الشهر 3 — التوسّع المحكوم / Month 3 — Governed Expansion

- **الأسبوع 9:** الوصول إلى ≥3 paid pilots مُسلَّمة — يفتح مسار تسعير R3 الكامل.
- **الأسبوع 10:** شريك ثالث/رابع. أول إحالة من عميل سابق.
- **الأسبوع 11:** R3 ثانٍ حيّ. تقييم: هل أي workflow تكرّر 3× → نحو module ([`PRODUCTIZATION_PATH.md`](PRODUCTIZATION_PATH.md))؟
- **الأسبوع 12:** مراجعة 90 يوماً. Board Pack. قرار الرهان الاستراتيجي التالي + معايرة سعر R1.

---

## 7. حركة استقطاب الشركاء / Partner-Recruitment Motion

الهدف: توقيع **3–5 شركاء** (وكالات/استشارات) خلال 90 يوماً. الشريك الواحد = توزيع مستمر.

### 7.1 الجملة / The Pitch

> **AR:** «أنتم تجيبون الاهتمام — Dealix يثبت ماذا حدث بعده. خلّونا نجرّب على عميل واحد من عملائكم: نراجع 10 leads، نسلّم Proof Pack، وأنتم تعرضونه كقيمة إضافية لعميلكم.»
> **EN:** "You bring the interest — Dealix proves what happened after it. Let us run it on one of your clients: 10 leads reviewed, a Proof Pack delivered, and you present it as added value."

### 7.2 الخطوات الخمس / The Five Steps

1. **استهداف:** ~10–15 وكالة من شبكة المؤسس الدافئة فقط — لا قوائم باردة.
2. **محادثة:** مكالمة واحدة، عرض «Agency Proof Pilot» ([`AGENCY_WEDGE.md`](AGENCY_WEDGE.md)).
3. **pilot واحد:** على عميل واحد من عملاء الوكالة — أصغر التزام، أسرع دليل.
4. **اتفاق مُهيكَل:** Referral أو Co-selling per [`PARTNER_ECONOMY.md`](PARTNER_ECONOMY.md) — لا «خلّنا نتعاون».
5. **تفعيل:** الشريك يجلب العميل الثاني → القناة تعمل.

### 7.3 الاقتصاد / Partner Economics (Negotiation Estimates)

| النوع / Type | النموذج / Model |
|---|---|
| Referral Partner | warm intro → ~15–25% من أول دفعة أو أول 3 أشهر |
| Co-selling Partner | الشريك يجلب العميل والسياق، Dealix يشغّل proof → تُقسَم pilot revenue |
| Implementation Partner | الشريك implementation fee، Dealix proof/diagnostic layer |

**حواجز ثابتة:** ❌ لا حصرية · ❌ لا بناء مخصّص قبل الدفع · ❌ لا white-label قبل إثبات الإيراد.

> **EN:** Sign 3–5 agency/consultancy partners via warm network only. Pitch the Agency Proof Pilot, run one pilot on one of their clients, formalize a structured Referral or Co-selling agreement, then let them bring client #2. Commission ranges are negotiation estimates.

---

## 8. استراتيجية الاستهداف / Targeting Strategy

كيف تُصنع كل lead — أربعة مصادر مشروعة فقط:

1. **مبني على ICP — دافئ أولاً:** المحرّك يقترح targets مطابقة لمواصفة القسم 1 من شبكة المؤسس والعلاقات القائمة. كل target له **Source معروف**.
2. **إحالات الشركاء:** warm intros من الشركاء الموقّعين — السياق يأتي مع الـlead.
3. **الوارد:** من الموقع (R0) ومن محرّك المحتوى — العميل بادر بالاتصال.
4. **إحالات العملاء:** من عملاء سلّمنا لهم Proof Pack — أعلى جودة.

### الممنوع صراحةً / Explicitly Forbidden

> per [`NON_NEGOTIABLES`](../00_constitution/NON_NEGOTIABLES.md) و[`AGENCY_WEDGE.md`](AGENCY_WEDGE.md) و[`COMMERCIAL_GATES.md`](COMMERCIAL_GATES.md):

- ❌ **لا scraping** لأي بيانات.
- ❌ **لا قوائم مشتراة** ولا قواعد بيانات خارجية.
- ❌ **لا رسائل آلية باردة** — لا WhatsApp بارد، لا LinkedIn automation، لا mass DMs.
- ❌ **لا إرسال خارجي بلا موافقة بشرية** — المحرّك يصيغ مسودة، المؤسس يعتمد ويرسل.
- ❌ **لا PII في المحتوى أو الحالات** — لا أسماء، لا بريد، لا هواتف، لا هويات (per [`AUTHORITY_ENGINE.md`](AUTHORITY_ENGINE.md)).

سلسلة كل lead تتبع [`DEALIX_METHOD.md`](DEALIX_METHOD.md):
`Signal → Source → Owner → Approval → Action → Evidence → Decision → Value → Asset`.

**EN:** Every lead is sourced one of four legitimate ways — ICP-based warm-first, partner-referred, inbound, or customer-referred. No scraping, no purchased lists, no cold automation, no external send without human approval, no PII in content or case studies.

---

## 9. روابط / Cross-links

- [`INDEX.md`](INDEX.md) — فهرس طبقة العقيدة / doctrine index
- [`OFFER_LADDER.md`](OFFER_LADDER.md) — سلم العروض / offer ladder
- [`AGENCY_WEDGE.md`](AGENCY_WEDGE.md) — مدخل الوكالات / agency wedge
- [`DEALIX_METHOD.md`](DEALIX_METHOD.md) — المنهجية / the method
- [`UNIT_ECONOMICS.md`](UNIT_ECONOMICS.md) — اقتصاد الوحدة / unit economics
- [`COMMERCIAL_GATES.md`](COMMERCIAL_GATES.md) — البوابات / the gates
- [`COMMERCIAL_CONTROL_TOWER.md`](COMMERCIAL_CONTROL_TOWER.md) — برج التحكم / control tower
- [`PARTNER_ECONOMY.md`](PARTNER_ECONOMY.md) — اقتصاد الشركاء / partner economy
- [`AUTHORITY_ENGINE.md`](AUTHORITY_ENGINE.md) — محرّك السلطة / authority engine
- [`PRODUCTIZATION_PATH.md`](PRODUCTIZATION_PATH.md) — مسار المنتج / productization path
- [`../COMPANY_SERVICE_LADDER.md`](../COMPANY_SERVICE_LADDER.md) — السلم الحي للأسعار / live pricing source of truth
- [`../00_constitution/NON_NEGOTIABLES.md`](../00_constitution/NON_NEGOTIABLES.md) — غير القابل للتفاوض / non-negotiables

---

> **تنبيه:** كل الأرقام ومعدّلات التحويل والإيراد في هذه الوثيقة تقديرية للتخطيط. القيمة التقديرية ليست قيمة مُتحقَّقة.
> **Note / Disclosure:** All figures, conversion rates, and revenue numbers in this document are planning estimates. Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
