# Dealix — 30-Day Launch Master Plan · خطة الإطلاق الرئيسية في 30 يوماً

<!-- Owner: Founder / CEO · Bilingual (AR primary + EN) · Mode: draft_only · No overclaim -->
<!-- Single source of truth for the 30-day go-live + first-paying-customer sprint -->
<!-- Companion to: docs/STRATEGIC_MASTER_PLAN_2026.md · docs/OFFER_LADDER_AND_PRICING.md -->

> **الهدف الوحيد للـ30 يوم:** أن نصبح **حيّين على الإنترنت** + نُغلق **أول عميل
> مدفوع** (Sprint بـ499 ريال) + نُسلّم **أول Proof Pack موقّع** — مع التزام كامل
> بالحوكمة وصفر مبالغة.
>
> **The single 30-day goal:** go **live in public** + close the **first paying
> customer** (499 SAR Sprint) + deliver the **first signed Proof Pack** — with full
> doctrine compliance and zero overclaim.

---

## 0) القرار التنفيذي · Executive Decision

**النجمة القطبية (North-Star) — مؤشر واحد لا يقبل التأويل:**
> **1 فاتورة مدفوعة + 1 Proof Pack موقّع خلال 30 يوماً.**
> (Stretch: 3 مدفوعة.) كل شيء آخر مؤشر مساعد.

**الحالة الصادقة للأعمال (سطر واحد):** Dealix منتج مكتمل هندسياً ومُختبَر بكثافة
(179 router، +4500 اختبار، تكامل PDPL/ZATCA، Moyasar، 10 وكلاء، سلّم 6 درجات،
حوكمة مفروضة باختبارات، CI أخضر) — **لكنه لم يخدم عميلاً حقيقياً واحداً بعد.** لا
دومين حيّ، لا `RAILWAY_TOKEN`، لا pilots، لا إيراد. **الفجوة ليست هندسية —
الفجوة تشغيلية: الانطلاق الحيّ + تفعيل أول عميل.** هذه الخطة تُغلق تلك الفجوة في
30 يوماً.

**Honest one-liner:** Dealix is engineering-complete and test-heavy but has never
served a real customer. The gap is operational go-live + customer activation — not
code. This plan closes that gap in 30 days.

**ما لا نفعله في الـ30 يوم (تركيز قاتل):** لا نبني ميزات جديدة، لا نطارد
Enterprise، لا نفتح الدرجات 3–5، لا نوظّف، لا حملات مدفوعة. **نُطلق ما هو
مُتحقَّق منه (الدرجتان 0 و1) ونبيعه يدوياً لقائمة دافئة.**

---

## 1) لقطة الجاهزية الصادقة · Honest Readiness Snapshot

سجل عدم-المبالغة (`dealix/registers/no_overclaim.yaml`) هو **أصل تسويقي**، لا
عبء. ننشره علناً كـ ميزة ثقة لا يفعلها أحد في السوق.

| الحالة · Status | العدد | ماذا نفعل بها في الإطلاق |
|---|---|---|
| **Production** (مُتحقَّق) | 16 | نبيعه ونعد به علناً |
| **Partial** | 5 | نُفصح عنه، لا نبيعه كمكتمل |
| **Pilot** | 5 | تجريبي داخلي فقط |
| **Planned** | 2 | لا ذكر له كقدرة حالية |

**القاعدة:** أي قدرة نَعِد بها علناً يجب أن تُقابِل صفّاً بحالة `Production`.
الباقي يُفصَح عنه بصراحة. → **هذا هو خندق صدق العلامة (Brand-honesty moat).**

**Launch rule:** every public promise maps to a `Production`-status capability;
everything else is disclosed, never sold as done. This radical honesty is the moat.

---

## 2) العرض عند الإطلاق · The Launch Offer

نركّز الـ30 يوم على **الدرجتين المُتحقَّق منهما فقط**:

| الدرجة | الاسم | السعر | الدور في الإطلاق |
|---|---|---|---|
| **0** | Free AI Ops Diagnostic · التشخيص المجاني | **0 SAR** | **الطُّعم / الوتد** — تقرير صفحة واحدة + 3 أولويات (15 دقيقة) |
| **1** | 7-Day Revenue Proof Sprint · سبرنت الإثبات | **499 SAR** | **أول إيراد** — تشخيص مفصّل + 5 مسودات + Proof Pack يوم 7 + خطة 30 يوم |

الدرجات 2–5 (1,500 / 2,999–4,999 / 7,500–15,000 / rev-share) **مُعلنة لكن
مُقفلة** خلف القاعدة الذهبية: *كل درجة تُفتح فقط بعد إثبات حقيقي من السابقة.* الدرجات
3–5 يُفصح عنها كـ **بقيادة المؤسس / شبه-مؤتمتة** — لا تُباع كخدمات مُدارة بالكامل.

**معادلة التحويل المستهدفة:** Diagnostic مجاني → 30% يرتقون إلى Sprint 499 ريال →
بعد Proof Pack ناجح يُفتح مسار 1,500 ثم 2,999/شهر.

**The launch wedge:** Free Diagnostic → 499 SAR Sprint. Rungs 2–5 are announced but
gated behind documented proof; rungs 3–5 disclosed as founder-assisted. Hamish
(margin) on the Sprint is ~85% (2–3 founder-hours + <10 SAR LLM).

---

## 3) العميل المثالي والشاطئ الأول · ICP & Beachhead

لا نغلي المحيط. نختار **قطاعين فقط** للـ30 يوم (من `docs/ops/sector_playbooks.md`):

| القطاع | زاوية الإثبات (Proof Angle) | جملة الفتح |
|---|---|---|
| **B2B SaaS (Series A/B)** | يفقدون 20–30% من العملاء المحتملين في أول 4 ساعات صمت | "نُثبت خلال 7 أيام كم صفقة تتسرّب من pipeline قبل أن تردّ عليها" |
| **العقار / Proptech** | 70% من استفسارات واتساب ليست مشترين جادّين | "نُرتّب استفساراتك حسب جدية الشراء قبل أن يضيع وقت مندوبك" |

**ICP الدقيق:** شركة B2B سعودية، 20–500 موظف، ميزانية مبيعات/تسويق سنوية
20K–500K ريال، المشتري = المؤسس أو VP Sales، مُحفِّز الإلحاح = بطء الرد على
العملاء المحتملين. **مُستبعَد الآن:** Enterprise بـ white-label كامل، ضمانات
إيراد، أتمتة واتساب/LinkedIn باردة.

**Beachhead:** 2 sectors only (B2B SaaS + Real Estate), Saudi, 20–500 employees,
founder/VP Sales as buyer. Excluded for now: full white-label enterprise, revenue
guarantees, cold automation.

---

## 4) Runbook الانطلاق التقني · Technical Go-Live Runbook (Week 1 critical path)

الفجوة الحقيقية. كل خطوة لها مالك ومعيار إنجاز. الأوامر حقيقية وموجودة في الريبو.

| # | الخطوة | الأمر / الإجراء الفعلي | معيار الإنجاز (Done-check) |
|---|---|---|---|
| 1 | تهيئة النشر | ضبط `RAILWAY_TOKEN` كسر في إعدادات البيئة | متغيّر موجود، `railway_deploy.yml` يعمل |
| 2 | نشر staging | تشغيل النشر إلى Railway (staging) | الخدمة ترفع، `/health` يرجع healthy |
| 3 | تحقّق الجاهزية | `make prod-verify` | يمرّ بلا أخطاء P0 |
| 4 | دومين + TLS | شراء/ربط `dealix.me` + `api.dealix.me`، DNS، TLS | الصفحة + `/status` تُحمّل، شهادة صالحة |
| 5 | اختبار دخان حيّ | `make production-smoke PRODUCTION_BASE_URL=https://api.dealix.me` | يمرّ، وسجل Production Smoke حديث ناجح |
| 6 | تحقّق تجاري | `python scripts/verify_commercial_launch_ready.py` | أخضر |
| 7 | المراقبة | تفعيل لوحات Sentry / Langfuse، Request IDs في السجل | الأخطاء والتكاليف مرئية للمشغّل |
| 8 | بوابة الانطلاق | اجتياز كل بنود `docs/ops/COMMERCIAL_GO_LIVE_GATE.md` (6 أقسام) | كل بنود P0 مكتملة أو مقبولة المخاطرة موثّقة |
| 9 | السجل علني | نشر `no_overclaim.yaml` على صفحة الثقة | الصفحة تعرض الحالة الحقيقية (16/5/5/2) |
| 10 | مسار الدفع | اختبار Moyasar في وضع الإنتاج بمبلغ حقيقي صغير ثم استرداد | الفاتورة تُدفع، webhook يتحقق، callback على الدومين الحيّ |

**بوابة الانطلاق (6 أقسام من COMMERCIAL_GO_LIVE_GATE):** (1) الموقع العام (2) API
ودخان (3) مسار طلب الديمو (4) الدفع (5) الثقة والامتثال (6) المراقبة. **لا
إطلاق عام ولا ديمو رسمي قبل اكتمال P0.**

**Go-live runbook (real commands):** set `RAILWAY_TOKEN` → deploy staging →
`make prod-verify` → buy/point `dealix.me`+`api.dealix.me` (DNS/TLS) →
`make production-smoke` → `verify_commercial_launch_ready.py` → wire Sentry/Langfuse
→ pass all 6 sections of `COMMERCIAL_GO_LIVE_GATE.md` → publish no-overclaim register
→ test Moyasar live (small real charge + refund). **No public launch before all P0
items are complete or risk-accepted.**

---

## 5) حركة المبيعات بقيادة المؤسس · Founder-Led Sales Motion

صفر أتمتة. كله مسودات + موافقة. المرجع: `docs/sales-kit/WARM_LIST_WORKFLOW.md`.

**الإيقاع:** قائمة دافئة من **20 جهة**، **5/يوم** على مدى 4 أيام. طلب من سطر واحد
(عربي/إنجليزي). معالِجات الردود: (مهتم / غير مهتم / يطلب تفاصيل).

**بوابة التأهيل + 5 قرارات:** `ACCEPT` · `DIAGNOSTIC_ONLY` · `REFRAME` ·
`REJECT` · `REFER_OUT`. لا نقبل كل أحد — نحمي وقت التسليم.

**العرض التقديمي:** ديمو 12 دقيقة → تشخيص مجاني → عرض Sprint 499 ريال. المسودة
تُرندَر من `templates/PROPOSAL_SPRINT_ARABIC_FULL.md.j2` (والإنجليزي)، وتُوضع في
طابور الموافقة `/ar/ops/approvals` — **لا إرسال خارجي بدون موافقة صريحة.**

**CTA واحد فقط** (قاعدة SOAEN): Risk Score أو Sample Proof أو ديمو 10 دقائق.

**Sales motion:** 20 warm contacts, 5/day, one-line ask, qualification gate with 5
decision types, 12-min demo → free diagnostic → 499 Sprint proposal rendered from the
Jinja2 template and queued for approval. Zero automation, draft-only, one CTA.

---

## 6) التسليم · Delivery — The 7-Day Sprint

المرجع: `docs/services/lead_intelligence_sprint/`. كله **draft-only، approval-first**.

| اليوم | المرحلة | المخرَج |
|---|---|---|
| 0–1 | Intake | أسئلة العمل/البيانات/المبيعات/الحوكمة + استلام CSV |
| 1–5 | Build | استيراد + تنظيف + إزالة تكرار + تسجيل الحسابات + تجزئة + ترتيب الفرص |
| 1–5 | Drafts | 5+ مسودات تواصل (عربي/إنجليزي) — بلا إرسال |
| 5–6 | QA Gates | Business / Data / AI / Compliance QA |
| 5–7 | Outputs | تقرير تنفيذي + **Proof Pack** (صفوف مستلمة/منظّفة، حسابات مُسجّلة، مسودات، جودة قبل/بعد، خطوات تالية) |
| 7 | Handoff | توقيع العميل + توصية الترقية (1,500 / 2,999) |

**النطاق المستثنى:** إرسال واتساب، أتمتة LinkedIn، scraping، تكاملات معقدة، تنفيذ
مبيعات نيابة عن العميل. **Excluded:** live sends, automation, scraping, complex
integrations, doing the customer's selling for them.

---

## 7) التسعير والمالية وأول إيراد · Pricing & First-Revenue Finance

- **مسار الدفع:** Moyasar (`/api/v1/checkout` + `/api/v1/webhooks/moyasar`)، وضع
  إنتاج، callback على الدومين الحيّ.
- **القاعدة الحديدية:** `no_revenue_before_paid` — **لا إيراد يُسجَّل قبل
  `invoice_paid`. لا upsell قبل Proof.**
- **اقتصاد الوحدة (Sprint):** سعر 499 ريال · تكلفة ~2–3 ساعات مؤسس + <10 ريال
  LLM · هامش ~85%.
- **هدف الـ30 يوم:** ≥1 Sprint مدفوع (499 ريال). Stretch: 3 (~1,497 ريال) +
  مسار ترقية واحد مفتوح.

**Finance:** Moyasar production checkout, invoice-before-revenue is hard-coded,
Sprint margin ~85%, target ≥1 paid Sprint in 30 days (stretch 3).

---

## 8) التسويق والمحتوى والإطلاق العام · Marketing & Public Launch

- **LinkedIn يدوي** بعد SOAEN — 4 منشورات/أسبوع، لا أتمتة. ثيمات: درس من call،
  Proof، معالجة اعتراض.
- **إعلان الإطلاق العام** مربوط بـ **سجل عدم-المبالغة الحيّ** كقصة التمييز: "نُعلن
  ما هو حقيقي فقط — انظر سجلنا العلني."
- **لا ادعاءات أرقام** (مثل "استرجاع 30% من العملاء") إلا إذا كانت `Production`
  وموثّقة. الأرقام من `kpi_founder_commercial_import.yaml` فقط — **لا KPI مخترع.**

**Marketing:** manual LinkedIn (4/wk, post-SOAEN), public launch anchored to the live
no-overclaim register, no invented KPIs — numbers come from the import file only.

---

## 9) الحوكمة والخطوط الحمراء · Governance & Guardrails

الخطوط الخمسة غير القابلة للتجاوز (`dealix/commercial_ops/doctrine.py`) — تُفرَض
باختبارات تمرّ في CI:

1. **`no_cold_whatsapp`** — لا واتساب بارد، مسودة + موافقة فقط.
2. **`no_linkedin_automation`** — لا أتمتة LinkedIn، نشر يدوي بعد SOAEN.
3. **`no_external_gmail_without_approval`** — لا أي إجراء خارجي بدون موافقة صريحة.
4. **`no_invented_crm_kpi`** — لا أرقام CRM/KPI مخترعة، من الاستيراد فقط.
5. **`no_revenue_before_paid`** — لا upsell قبل Proof، لا إيراد قبل دفع مثبت.

**+ البوابات الصلبة الثماني (الدستور):** NO_LIVE_SEND · NO_LIVE_CHARGE ·
NO_COLD_WHATSAPP · NO_LINKEDIN_AUTOMATION · NO_SCRAPING · NO_FAKE_PROOF ·
NO_FAKE_REVENUE · NO_UNAPPROVED_TESTIMONIAL.

**وضع التشغيل طوال الإطلاق: `draft_only`.** Operating mode throughout: draft-only,
approval-first. These 5 non-negotiables + 8 hard gates are enforced by passing tests.

---

## 10) الجدول اليومي للـ30 يوم · Day-by-Day Timeline

### الأسبوع 1 (أيام 1–7): **الانطلاق الحيّ · Go Live**
- **يوم 1–2:** ضبط `RAILWAY_TOKEN`، نشر staging، `make prod-verify`.
- **يوم 3–4:** ربط `dealix.me` + `api.dealix.me`، DNS/TLS، `make production-smoke`.
- **يوم 5:** `verify_commercial_launch_ready.py`، تفعيل Sentry/Langfuse، اختبار Moyasar حيّ + استرداد.
- **يوم 6:** اجتياز بوابة الانطلاق (6 أقسام)، نشر سجل عدم-المبالغة علناً.
- **يوم 7:** تجهيز قائمة 20 جهة دافئة + رندرة قالبَي العرض. **بوابة قرار: حيّ؟**

### الأسبوع 2 (أيام 8–14): **أول المحادثات · First Conversations**
- **يوم 8–11:** تواصل القائمة الدافئة 5/يوم، حجز التشخيصات.
- **يوم 12–13:** إجراء أول 3–5 تشخيصات مجانية (15 دقيقة لكل).
- **يوم 14:** وضع أول عروض Sprint في طابور الموافقة. **بوابة قرار: ≥3 تشخيصات؟**

### الأسبوع 3 (أيام 15–21): **أول بيع + بدء التسليم · First Sale + Delivery**
- **يوم 15–17:** متابعة العروض، معالجة الاعتراضات، إغلاق ≥1 Sprint.
- **يوم 18:** تحصيل الدفع عبر Moyasar (`invoice_paid`).
- **يوم 19–21:** Intake + بدء تسليم Sprint (استيراد، تنظيف، تسجيل، مسودات). **بوابة قرار: ≥1 مدفوع؟**

### الأسبوع 4 (أيام 22–30): **أول Proof Pack + تجهيز التوسّع · Proof + Expansion**
- **يوم 22–25:** QA gates، تقرير تنفيذي، إكمال Proof Pack.
- **يوم 26–27:** توقيع العميل على Proof Pack + تسجيل أصل رأسمالي (`capital_asset_registry.py`).
- **يوم 28:** فحص أهلية الاشتراك (`retainer_eligibility.py`: Proof≥L1، رضا≥7، نتيجة مقيسة).
- **يوم 29:** عرض الترقية (1,500 ريال Pack أو 2,999/شهر) للعميل المؤهَّل.
- **يوم 30:** مراجعة تنفيذية + سجل احتكاك (friction log) + قرار الـ90 يوم. **بوابة قرار: Proof Pack موقّع؟**

---

## 11) المؤشرات ولوحة قيادة المؤسس · Metrics & CEO Dashboard

مراجعة يومية عبر `scripts/run_founder_commercial_day.sh`.

| النوع | المؤشر | هدف الـ30 يوم |
|---|---|---|
| **نجمة قطبية** | Proof Pack موقّع + فاتورة مدفوعة | **1** (stretch 3) |
| رائد (Leading) | مقدّمات دافئة مُرسَلة | 20 |
| رائد | تشخيصات مجانية مُجراة | ≥5 |
| رائد | عروض Sprint في الطابور | ≥3 |
| متأخر (Lagging) | Sprints مباعة | ≥1 |
| متأخر | ريال محصّل | ≥499 |
| متأخر | أصول رأسمالية مُسجّلة | ≥1 |

**Dashboard:** north-star = 1 signed Proof Pack + 1 paid invoice; leading = intros/
diagnostics/proposals; lagging = sprints sold / SAR collected. Reviewed daily.

---

## 12) المخاطر والطوارئ · Risk Register

| الخطر | المُحفِّز | التخفيف / البديل |
|---|---|---|
| لا وصول للدومين/الأسرار | يوم 2 بلا `RAILWAY_TOKEN` | تشغيل على نطاق Railway المؤقت + شراء الدومين بالتوازي |
| فشل الدفع الحيّ | اختبار Moyasar يفشل يوم 5 | حصر على فاتورة يدوية مُوافقة + إصلاح webhook قبل أي عرض عام |
| صفر ردود من القائمة الدافئة | يوم 11 بلا ردود | إعادة صياغة الطلب (REFRAME)، توسيع القائمة بـ5 مقدّمات، تبديل القطاع |
| انزلاق حوكمي | أي إجراء خارجي بلا موافقة | إيقاف فوري، `draft_only` يبقى، مراجعة SOAEN |
| لا تأهّل لأي عميل | يوم 14 كل القرارات REJECT | إعادة فحص ICP والقطاع، تضييق زاوية الإثبات |

---

## 13) بوابات القرار · Decision Gates (Go/No-Go)

| اليوم | البوابة | إن فشلت |
|---|---|---|
| **7** | هل نحن حيّون (الموقع + API + الدفع + المراقبة)؟ | لا تواصل خارجي حتى الاكتمال |
| **14** | ≥3 تشخيصات مُجراة؟ | إعادة تقييم القطاع/الرسالة قبل المتابعة |
| **21** | ≥1 Sprint مدفوع؟ | مراجعة العرض/التسعير/الاعتراضات |
| **30** | Proof Pack موقّع؟ | تشريح السبب، إعادة ضبط ICP قبل الـ90 يوم |

---

## 14) ما بعد الـ30 يوم · Bridge to 90 Days

الـ30 يوماً منصّة إطلاق لا نهاية. عند توقيع أول Proof Pack نفتح:
- مسار التوسّع: 1,500 ريال Pack → 2,999/شهر Managed Ops (بعد إثبات).
- التسلسل الكامل والخنادق في `docs/STRATEGIC_MASTER_PLAN_2026.md` (90 يوم → 12 شهر).
- منطق الاشتراك والأصول الرأسمالية: `retainer_eligibility.py` + `capital_asset_registry.py`.

**After 30 days:** the sprint is a launchpad. First Proof Pack opens the expansion
path (1,500 → 2,999/mo) and connects to the 90-day → 12-month trajectory in
`STRATEGIC_MASTER_PLAN_2026.md`. Retainer + capital-asset logic already coded.

---

*وضع التشغيل: `draft_only` · لا مبالغة · الأرقام من الاستيراد فقط · كل درجة تُفتح
بإثبات. Operating mode: draft-only · no overclaim · numbers from import only · every
rung unlocks on proof.*
