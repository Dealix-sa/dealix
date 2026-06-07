# Dealix — الإطلاق الآن / Launch Now

_آخر تحديث: 2026-06-07_

هذا المستند يلخّص ما أصبح **حقيقياً وقابلاً للتشغيل اليوم**، والحلقة اليومية، والأمور
المحجوزة لك أنت (المؤسس) بحكم الدستور. أمر واحد يعطيك الحالة:

```bash
python3 scripts/dealix_company_live_check.py
```

> One command tells you if the company is operating and what's left to you.

---

## ما أصبح حقيقياً ومُتحقَّقاً / What is real & verified

| المجال | الحالة | الدليل |
|---|---|---|
| **مكينة ليدز سعودية حقيقية** | ✅ | 24 حساب مُصدَّر، مُقيَّم ICP، بلا PII — `scripts/dealix_target_universe.py` |
| **مسودات يومية بموافقة** | ✅ | 80 مسودة (واتساب+بريد، عربي/إنجليزي) — `scripts/dealix_daily_draft_pack.py` |
| **حُرّاس دستوريون** | ✅ | 13 اختبار يرفض أي مصدر مفقود / PII / قناة باردة — `tests/test_target_universe.py` |
| **ظهور في الكوكبت** | ✅ | `GET /api/v1/ops-autopilot/targeting/universe-today` + بطاقة في `/[locale]/ops` |
| **الموقع يبني** | ✅ | `frontend/` Next.js 15.5.19 — يبني نظيفاً |
| **أمان مُصحَّح** | ✅ | ترقية Next.js تُزيل CVE حرِجة (تجاوز موافقة middleware) — Trivy نظيف |
| **CI غير معطّل** | ✅ | Gitleaks (OSS CLI) + Trivy (CLI) بدل Actions المعطّلة |

---

## الحلقة اليومية (٩٠ ثانية) / The daily loop

```bash
# 1) حسابات اليوم (الأعلى قيمة) + 2) ولّد المسودات بموافقة
python3 scripts/dealix_daily_draft_pack.py --top 10
# 3) افتح: data/outreach/drafts/<اليوم>/INDEX.md
```

لكل حساب: مقدمة دافئة/أساس قانوني ← عبّئ الاسم الحقيقي ← راجع ← **أرسل يدوياً بنفسك** ←
سجّل النتيجة. (راجع `docs/ops/SAUDI_LEAD_MACHINE_REAL_AR.md`.)

---

## محجوز لك أنت (المؤسس) — بحكم الدستور لا الكسل / Reserved for you, by doctrine

الدستور (#8: لا إجراء خارجي بلا موافقة) يحجز هذه عمداً — هي أصل ثقة Dealix، لا عائق:

1. **النشر + الدومين:** انشر على Railway واربط النطاق (تحتاج اعتماداتك). دليل:
   `docs/RAILWAY_DEPLOY_GUIDE_AR.md` · بوابة: `bash scripts/official_launch_verify.sh`.
2. **الدفع الحقيقي:** Moyasar في وضع sandbox حتى تقلبه live بنفسك عند الجاهزية.
3. **شبكتك الدافئة:** أضف صفوفك (CRM/معارف) في أعلى عالم الحسابات — ستتصدّر التقييم.
4. **الإرسال:** راجع كل مسودة وأرسلها **يدوياً** — لا إرسال آلي إطلاقاً.

> لماذا لا أرقام جوال جاهزة؟ تلفيق/شراء بيانات شخصية يخالف الدستور (#1،#4،#6) ويدمّر
> أكبر أصل لديك: الثقة (PDPL أصلاً، الموافقة أولاً). الطريق الصحيح = مقدمة دافئة + موافقتك.

---

## الاعتمادات عند النشر / Env at deploy time

`DATABASE_URL` · `ADMIN_API_KEYS` · `APP_SECRET_KEY` (إلزامي) · `MOYASAR_API_KEY` (للدفع) ·
`ANTHROPIC_API_KEY`/`HUBSPOT_ACCESS_TOKEN`/`CALENDLY_URL` (اختياري). التطبيق يتدرّج بأمان
بدون الاختيارية. تفاصيل: `docs/contributing/DEPLOYMENT.md`.

---

_القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value_
