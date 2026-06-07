# خطة الإطلاق الحقيقية لـ Dealix — من الأهداف إلى الوصول
# Dealix Real-Launch Master Plan — From Goals to Go-Live

> **الحالة بصدق / Honest status:** Dealix منصة ناضجة تقنيًا (FastAPI + Next.js +
> عشرات الوحدات) لكنها **قبل أول إيراد** (دفعة تأسيسية). هذه الخطة تجعلها قابلة
> للإطلاق فعليًا، وتُصلح العوائق التي كانت تمنع الوصول.
> Technically mature, **pre-first-revenue** (founding cohort). This plan makes it
> truly launchable and removes the blockers that stood in the way.

تاريخ التحديث / Updated: 2026-06-07 · الفرع / Branch: `claude/affectionate-bohr-Du2Ha`

---

## 1) الهدف / The goal

محرّك إيرادات ونمو وامتثال بالذكاء الاصطناعي للشركات السعودية B2B — **مُحكَم بالدليل،
PDPL أصلاً، والموافقة أولاً.** ليس أداة AI عامة ولا أتمتة بريد بارد.

**هدف 90 يوم (واقعي):** 8–15K ر.س إيراد شهري متكرر + 30–40K ر.س لمرة واحدة
≈ **40–55K ر.س تراكمي** + 3 عملاء مستمرين، عبر سلّم العروض الخمسة.

---

## 2) سلّم العروض الخمسة / The five-tier ladder

| # | العرض / Offer | السعر / Price |
|---|---|---|
| 0 | تشخيص + Risk Score مجاني / Free diagnostic | 0 |
| 1 | Revenue Intelligence Sprint (7 أيام) | **499 ر.س** |
| 2 | Agency Proof Pack | 1,500 ر.س |
| 3 | Managed Ops Retainer | 2,999–4,999 ر.س/شهر |
| 4 | Custom AI Project / مشروع AI مخصص | 5,000–25,000 ر.س |

> قاعدة صارمة: **لا توسّع لمستوى أعلى قبل Proof Pack مُسلَّم من المستوى الأدنى.**
> No upsell without a delivered Proof Pack from the rung below.

الصفحات الحيّة / Live pages: `/services` · `/pricing` · `/custom-ai` ·
`/offer/lead-intelligence-sprint` · `/dealix-diagnostic` · `/risk-score` · `/proof-pack`.

---

## 3) العوائق التي وُجدت وحُلّت في هذه الدفعة / Blockers found & fixed now

| العائق / Blocker | الحل / Fix |
|---|---|
| **الصفحة الرئيسية كانت تنتهك العقيدة** — شعارات عملاء وهمية، أرقام مُختلقة (+500 عميل، 3.2x، 99.9%)، وشهادات عملاء مُزيّفة. خطر سمعة قاتل لشركة قيمتها "الثقة والدليل". | أُعيدت كتابة `CommercialLaunchHome` بالكامل: قطاعات بدل عملاء وهميين، إحصاءات قدرات صادقة، قسم "كيف يعمل"، قسم **الدفعة التأسيسية** الصريح، وشارة **"نتائج موثّقة فقط — لا أرقام مُختلقة"**. الصدق أصبح ميزة بيعية. |
| **واجهتان متضاربتان** — النشر (`Dockerfile.web`) كان يبني `apps/web` البسيطة، بينما القمع التجاري الحقيقي في `frontend/`. | أُعيد توجيه `Dockerfile.web` ليبني `frontend/` المرجعية (standalone). `apps/web` تبقى كعرض معماري عبر `apps/web/Dockerfile`. |
| **روابط مكسورة** — `/contact`, `/terms`, `/custom-ai` مربوطة لكنها مفقودة. | أُنشئت الصفحات الثلاث (ثنائية اللغة، على القشرة الرسمية، نماذج بتدهور آمن). |
| **"درافتات يومية" و"أرقام عملاء" غير موجودة فعليًا** — `data/founder_briefs` و`data/outreach` كانت فاضية. | شُغِّل المحرك وأُنتجت أصول حقيقية: موجز يومي + تحقّق 249 هدفًا + تصدير outreach + 10 مسودات مؤهَّلة → `docs/commercial/daily_ops/`. |
| **عدم وجود حارس ضد العودة** | أُضيف `tests/test_no_fabricated_web_claims.py` يفشل CI إذا عادت الادعاءات الوهمية. |

---

## 4) نموذج النشر / Deployment model

| الخدمة / Service | المصدر / Source | Health |
|---|---|---|
| API (FastAPI) | `Dockerfile` · `railway.toml` → `uvicorn api.main:app` | `/healthz` |
| Web (Next.js العام) | `Dockerfile.web` → `frontend/` (standalone) · `railway.web.toml` | `/healthz` |

الإطلاق الرسمي / Official launch gate:
```bash
bash scripts/verify_dealix_commercial_go_live.sh     # → DEALIX_OFFICIAL_LAUNCH_VERDICT
bash scripts/official_launch_verify.sh               # → OFFICIAL_LAUNCH_VERDICT=PASS
```
النطاقات / Domains: `dealix.me` (web) · `api.dealix.me` (API). متغيرات الواجهة:
`NEXT_PUBLIC_API_URL`, `NEXT_PUBLIC_SITE_URL`, `NEXT_PUBLIC_CALENDLY_URL`.

---

## 5) خطة 30 / 60 / 90 / The roadmap

**اليوم 0–30 — أطلِق وابدأ البيع / Launch & start selling**
- انشر الواجهة المرجعية + الـ API، وثبّت النطاقات و TLS.
- املأ أعلى 20 خانة في `outreach_ready` بأسماء حقيقية من شبكتك.
- أرسل ≤5 لمسات أولى/يوم (يدويًا، بعد موافقتك). احجز 5–8 مكالمات تشخيص.
- سلّم أول 3 تشخيصات مجانية → اعرض Sprint بـ 499.

**اليوم 31–60 — أثبت القيمة / Prove value**
- سلّم أول Sprint مدفوع + أول Proof Pack (درجة ≥ 70).
- انشر أول ملخّص حالة آمن (بإذن العميل) — أول دليل حقيقي على الموقع.
- فعّل الدفع الحيّ (Moyasar) بعد أول فاتورة.

**اليوم 61–90 — التكرار والاحتفاظ / Repeat & retain**
- 2–3 عملاء على Managed Ops. أول مشروع Custom AI في الأفق.
- مراجعة أسبوعية + سجل الاحتكاك (friction log) لإزالة العوائق التشغيلية.

---

## 6) الإيقاع اليومي/الأسبوعي / Operating rhythm

```bash
# صباحًا (≈30 دقيقة)
python3 scripts/dealix_founder_daily_brief.py        # موجز اليوم
python3 scripts/validate_warm_targeting_csv.py       # صحة الأهداف
# أسبوعيًا (الأحد)
bash scripts/founder_weekly_loop.sh                  # بوابات أسبوعية
```
لوحة المؤسس / Founder cockpit: `/[locale]/ops/founder` (بمفتاح المشرف).

---

## 7) الهوية البصرية / Visual identity (متابعة / follow-up)

البراند: **Navy `#001F3F` + Gold `#D4AF37`** (انظر `DESIGN_SYSTEM.md`).
**ملاحظة توحيد:** ثلاث لوحات متعايشة حاليًا — رموز tailwind (`navy`/`gold`)،
ومتغيرات CSS (`--dealix-deep-green`/`--dealix-gold`)، وقيَم hex مكتوبة يدويًا
(`#0A1628`/`#C9974B`). الصفحات الجديدة موحّدة على القشرة الرسمية. التوحيد الكامل
عبر الصفحات بند متابعة (P1) لا يحجب الإطلاق.

---

## 8) ما يحتاجه المؤسس (قرارات/أسرار) / Founder inputs needed

- أسماء حقيقية لأعلى 20 هدفًا (من شبكتك/CRM) — النظام لا يخترع جهات اتصال.
- مفاتيح الإنتاج على Railway: `APP_SECRET_KEY`, `DATABASE_URL`, Moyasar (للدفع).
- تأكيد نطاق `dealix.me` يخدم `frontend/` بعد إعادة توجيه `Dockerfile.web`.
- ربط Calendly (`NEXT_PUBLIC_CALENDLY_URL`) وبريد `hello@dealix.me`.

---

## 9) العقيدة — 11 لا للتفاوض / The 11 non-negotiables

1) لا scraping. 2) لا واتساب بارد آلي. 3) لا أتمتة LinkedIn. 4) لا ادعاءات بلا
مصدر. 5) لا ضمان نتائج. 6) لا PII في السجلات. 7) لا إجابة معرفية بلا مصدر.
8) لا إجراء خارجي بلا موافقة. 9) لا وكيل بلا هوية. 10) لا مشروع بلا Proof Pack.
11) لا مشروع بلا Capital Asset.

> القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.
