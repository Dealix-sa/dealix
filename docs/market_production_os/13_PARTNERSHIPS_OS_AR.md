# 13 — الشراكات — Partnerships OS

> الموقع في الطبقة: المكوّن رقم 14 من *Market Production OS*. قناة نموّ غير مباشرة: الشريك يجلب العميل،
> Dealix تشغّل Revenue OS. العمود الفقري: [`00_MARKET_PRODUCTION_OS_MASTER_AR.md`](00_MARKET_PRODUCTION_OS_MASTER_AR.md).

هذا المستند يحدّد أنواع الشركاء، والعرض المقدّم للشريك، وهيكل الإحالة. كل تواصل مع شريك **مسودة بموافقة
المؤسس** — لا تواصل بارد، ولا تواصل باسم الشريك بلا إذنه. الطبقة تعيد استخدام `partnership_os` وتوثيق
[`docs/partners/`](../partners/) و[`docs/partner_os/`](../partner_os/)، ولا تكرّرها.

> القاعدة الأساسية: **الشريك يجلب العميل، Dealix تشغّل الـ Revenue OS، والشريك يحصل على قيمته** — رسم إحالة
> أو حصة إيراد أو هامش تنفيذ. كل خطوة تواصل = مسودة بموافقة المؤسس. 250 مسودة/يوم، صفر إرسال تلقائي.

---

## 0. النموذج (من `PARTNER_PROGRAM.md`، يُعاد بحرفه)

**Dealix تشخّص · الشريك ينفّذ · العميل يحصل على إثبات · الشريك يحصل على أعمال تنفيذ · Dealix تحتفظ
بطبقة الحوكمة/الإثبات.** ابدأ مرنًا، شروط بسيطة، هدف أولي: pilot واحد أو إحالة واحدة، ثم تعميق.

---

## 1. أنواع الشركاء (Partner Types)

| النوع | ما يجلبه | الزاوية |
|---|---|---|
| وكالات التسويق | عملاء عندهم leads متفرقة | تشخيص إيرادي يكمّل خدماتهم |
| مستشارو الأعمال | علاقات قرار + ثقة | إثبات سريع يدعم توصياتهم |
| منفّذو CRM | حسابات بحاجة لترتيب البيانات | طبقة بيانات → إيراد فوق الـ CRM |
| مكاتب المحاسبة | عملاء بفواتير/متابعات متفرقة | ترتيب الإشارات المالية كإشارة شراء |
| مزوّدو التدريب | شبكة شركات ناشئة | محتوى/تشخيص كقيمة مضافة لبرامجهم |
| موزّعو البرمجيات | حسابات قابلة للترقية | اكتشاف حسابات مؤهّلة للترقية |
| وكالات الويب | عملاء بعد إطلاق الموقع | تحويل الزيارات إلى عمليات إيراد مُحوكَمة |

> البحث العام عن شركة شريكة محتملة يتم عبر `linkedin_company_search (manual, founder-approved per call)`
> — بحث يدوي بموافقة المؤسس لكل حالة. لا أتمتة، لا scraping، لا جمع جماعي.

---

## 2. العرض للشريك (Partner Offer)

العرض الموحّد بسيط ومباشر:

> **أنت تجلب العميل؛ Dealix تشغّل الـ Revenue OS؛ وأنت تحصل على رسم إحالة / حصة إيراد / هامش تنفيذ.**

| نمط الشراكة | ما يحتفظ به الشريك | ما تحتفظ به Dealix | المرجع |
|---|---|---|---|
| Referral Partner | رسم إحالة (مثال تشغيلي 10–20% حسب الاتفاق) | التشخيص + طبقة الإثبات | [`PARTNER_PROGRAM.md`](../partners/PARTNER_PROGRAM.md) |
| Implementation Partner | أتعاب التنفيذ | التشخيص + طبقة الإثبات | [`PARTNER_PACKAGES.md`](../partners/PARTNER_PACKAGES.md) |
| Co-selling Pilot | حصة إيراد pilot | الحوكمة + الإثبات | [`PARTNER_PROGRAM.md`](../partners/PARTNER_PROGRAM.md) |
| White-label | سعر خاص (بعد عدة عملاء مدفوعين) | المحرّك الخلفي | [`PARTNER_PACKAGES.md`](../partners/PARTNER_PACKAGES.md) |

> لا اختراع نسب جديدة. الأرقام أمثلة تشغيلية من [`docs/partners/`](../partners/) و
> [`PARTNER_REFERRAL_SYSTEM_AR.md`](../partner_os/PARTNER_REFERRAL_SYSTEM_AR.md)؛ التعاقد يحسم النسبة.

---

## 3. هيكل برنامج الإحالة (Referral Program Outline)

| الخطوة | الفعل | البوابة |
|---|---|---|
| 1 | اكتشاف شريك محتمل + تسجيل ملف (`partner_profile`) | تلقائي (بحث يدوي معتمد) |
| 2 | درجة ملاءمة الشريك (`fit_score`) | تلقائي |
| 3 | مسودة رسالة تواصل مخصّصة | موافقة المؤسس |
| 4 | اتفاق مرن: pilot واحد أو إحالة واحدة | المؤسس + الشريك |
| 5 | إسناد العميل المُحال (`referral_tracker`) | تلقائي |
| 6 | احتساب الرسم/الحصة بعد الاستلام، لا بعد الوعد | المؤسس |
| 7 | تعميق النمط عند تكرار القيمة | المؤسس + الشريك |

- الرسم يُدفَع **بعد التسليم المؤكَّد**، لا بعد الوعد (يتسق مع
  [`LINKEDIN_CADENCE_PLAN.md` أسبوع 8](../content/LINKEDIN_CADENCE_PLAN.md)).
- لا تجديد تلقائي، ولا نسب من الإيراد تُفسد المحاسبة دون اتفاق صريح.

---

## 4. إعادة الاستخدام (Reuse)

- `auto_client_acquisition/partnership_os/` — `partner_profile.py`، `fit_score.py`،
  `referral_tracker.py`، `referral_store.py`، `partner_motion.py`.
- [`docs/partners/`](../partners/) — البرنامج، الباقات، الإعداد (`PARTNER_ONBOARDING.md`)،
  رسائل التواصل (`PARTNER_OUTREACH_MESSAGES.md`)، خط التجارب (`PARTNER_PILOT_PIPELINE.yaml`).
- [`docs/partner_os/PARTNER_REFERRAL_SYSTEM_AR.md`](../partner_os/PARTNER_REFERRAL_SYSTEM_AR.md) — نظام الإحالة الأساسي.

> أعد الاستخدام قبل أن تكتب: نظام الشركاء موثّق ومبني. الجديد هنا = **ربط الشراكات بطبقة الإنتاج + قاعدة
> الموافقة على كل تواصل**.

---

## 5. القياس (يُغذّي التقرير اليومي/الأسبوعي)

عدد الشركاء المحتملين المكتشَفين، رسائل التواصل المُسوَّدة/المعتمدة، الـ leads والاجتماعات والمدفوعات
المُسندة للشريك، وإيراد الشريك. التفاصيل في
[`14_GTM_METRICS_AND_LEARNING_AR.md`](14_GTM_METRICS_AND_LEARNING_AR.md).

---

## 6. اللاءات المطبَّقة هنا

- لا تواصل بارد مع شركاء، ولا تواصل باسم الشريك بلا إذنه (`ممنوع` في
  [`PARTNER_REFERRAL_SYSTEM_AR.md`](../partner_os/PARTNER_REFERRAL_SYSTEM_AR.md)).
- لا scraping ولا جمع جماعي. البحث العام عبر `linkedin_company_search (manual, founder-approved per call)` فقط.
- لا ضمان نتائج للعميل المُحال. لا PII في سجلات الشركاء. كل تواصل مسودة بموافقة المؤسس.

---

## EN summary

Partnerships OS is component #14: an indirect growth channel where the partner brings the client and
Dealix runs the Revenue OS. Partner types include marketing agencies, business consultants, CRM
implementers, accounting firms, training providers, software resellers, and web agencies. The unified
offer: you bring the client; Dealix runs the Revenue OS; you get a referral fee, revenue share, or
implementation margin — Dealix retains the governance and proof layer. Partnership shapes (referral,
implementation, co-selling pilot, white-label) and their example splits come from `docs/partners/` and
`docs/partner_os/`; we do not invent new percentages — the contract settles them. The referral program
runs: discover prospect (manual, founder-approved lookup) → fit score → drafted custom outreach →
flexible one-pilot/one-referral agreement → referral attribution → fee paid after confirmed delivery,
not after promise → deepen on repeat value. Every partner outreach is a draft requiring founder
approval; there is no cold partner outreach and no outreach in the partner's name without consent.
Public partner-company lookup uses `linkedin_company_search (manual, founder-approved per call)` only —
no automation, no scraping, no bulk collection. No guaranteed outcomes for the referred client, no PII
in partner records. The layer reuses `partnership_os/` and the existing partner docs. Core rule holds:
250 drafts/day, 0 auto-sends.

---

القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.
