# Dealix — قمرة قيادة المؤسس · CEO Launch Cockpit

**الحالة / Status:** DRAFT
**المالك / Owner:** Sami (founder)
**آخر تحديث / Last updated:** 2026-05-18
**وثائق مرافقة / Companion docs:** `MACHINE_ORCHESTRATION_MAP.md` · `FIRST_PILOT_PLAYBOOK.md` · `../V14_FOUNDER_DAILY_OPS.md` · `../commercial/COMMERCIAL_CONTROL_TOWER.md`

---

## الغرض · Purpose

هذه الوثيقة تعرّف شاشة قيادة واحدة للمؤسس في الصباح. لا كود جديد — كل سطح هنا مبني على نقاط نهاية (endpoints) موجودة بالفعل. الهدف: أن يفتح المؤسس شاشة واحدة، يرى الحقيقة، ويقرّر.

This document defines the founder's single morning command screen. No new code — every surface here is built entirely on existing endpoints. The goal: the founder opens one screen, sees the truth, and decides.

تجميد تجاري نشط (Commercial Freeze): الأولوية هي البيع وإنهاء تسليم Tier 0–1 وأول Pilot مدفوع. القمرة موجودة لتركيز الانتباه على ذلك، لا لتوسيع البناء.

---

## أسطح القمرة · The Cockpit Surfaces

ثلاث نقاط نهاية تغذّي القمرة، وأربع صفحات تعرضها.

Three endpoints feed the cockpit, and four pages render it.

### نقاط النهاية · Endpoints

| نقطة النهاية · Endpoint | ماذا تُظهر · What it surfaces |
|---|---|
| `GET /api/v1/founder/beast-command-center` | أهم 3 قرارات اليوم، حقيقة الإيراد، الموجز المالي، حالة التسليم، تنبيهات الدعم، ملخّص الـProof، تنبيهات الالتزام، الخطوة التالية الأفضل، البوابات الصارمة (hard gates). |
| `GET /api/v1/founder/dashboard` | leads منتظرة 24h+، الاحتكاك خلال 7 أيام، تجديدات مستحقة، موافقات معلّقة، أحداث Proof حديثة، الأصول الرأسمالية (capital assets). |
| `GET /api/v1/revenue-metrics/dashboard` | MRR / ARR / NRR / churn / ARPA. |

### الصفحات · Founder-facing pages

| الصفحة · Page | الدور · Role |
|---|---|
| `landing/founder-dashboard.html` | اللوحة الرئيسية اليومية. · The main daily board. |
| `landing/decisions.html` | طابور الموافقة — وافِق / ارفض / عدّل. · The approval queue. |
| `landing/founder-leads.html` | الـleads المنتظرة والاحتكاك. · Waiting leads and friction. |
| `landing/command-center.html` | شاشة مركز القيادة التنفيذية. · The executive command-center screen. |

> **ملاحظة ربط / Link note:** القمرة تُجمَّع من النقاط والصفحات أعلاه. إن أراد المؤسس صفحة واحدة موحّدة باسم `founder-beast-command-center.html` فهي غير موجودة بعد — تُستخدم اليوم `landing/command-center.html`. لا تبنِ صفحة جديدة تحت التجميد التجاري.

---

## الرقم الوحيد المهم · The Single Number That Matters

| الرقم · Number | التعريف · Definition |
|---|---|
| **Paid pilots delivered / MRR** | عدد الـPilots المدفوعة المُسلَّمة، ثم الإيراد الشهري المتكرّر. |

كل رقم آخر في القمرة مساعِد. إذا تحرّك هذا الرقم، اليوم نجح. إذا لم يتحرّك، اسأل: ما الذي عطّل الانتقال من interest إلى payment إلى proof؟ راجع [`../commercial/COMMERCIAL_CONTROL_TOWER.md`](../commercial/COMMERCIAL_CONTROL_TOWER.md).

Every other number in the cockpit is supporting. If this number moves, the day worked. If it does not, ask what blocked the path from interest to payment to proof.

---

## الطقس اليومي · The Daily Ritual

### الصباح — ~45 دقيقة · Morning — ~45 min

1. **افتح القمرة** — `landing/founder-dashboard.html` و`landing/command-center.html`. اقرأ أهم 3 قرارات، حقيقة الإيراد، حالة التسليم.
2. **صفّر الموافقات المعلّقة** — `landing/decisions.html` (`GET /api/v1/approvals/pending`). وافِق / ارفض / عدّل كل عنصر. WhatsApp / LinkedIn / الهاتف لا تُوافَق تلقائيًا أبدًا — راجع [`MACHINE_ORCHESTRATION_MAP.md`](MACHINE_ORCHESTRATION_MAP.md).
3. **راجع الـleads** — `landing/founder-leads.html`. أعطِ الأولوية لما انتظر 24h+.
4. **أرسل اللمسات الدافئة المعتمَدة** — فقط ما تمت الموافقة عليه. لا إرسال آلي.

### المساء — ~15 دقيقة · Evening — ~15 min

اكتب بطاقة النتائج اليومية:

```
python scripts/founder_daily_scorecard.py
```

للموجز الصباحي المجمَّع يمكن أيضًا تشغيل `scripts/dealix_founder_daily_brief.py`.

---

## الطقس الأسبوعي · Weekly Ritual

مراجعة الأحد:

- اقرأ الموجز الأسبوعي الناتج عن `weekly_brief.yml` (الأحد 03:00 UTC).
- راجع 3 اقتراحات التحسين من `weekly_self_improvement.yml` في صندوق الموافقة.
- افحص اتجاه MRR / NRR / churn عبر `GET /api/v1/revenue-metrics/dashboard`.
- قرار واحد: ما الذي يتوقّف، ما الذي يستمر، ما الذي يتغيّر الأسبوع القادم؟

Sunday review: read the weekly brief, review the 3 improvement suggestions, check the revenue-metrics trend, and decide one stop/continue/change.

---

## الطقس الشهري · Monthly Ritual

مراجعة الإيقاع الشهري:

- اقرأ مخرجات `monthly_cadence.yml` (أول الشهر 03:00 UTC) — الإيقاع الشهري وجدولة التجديدات.
- راجع التجديدات المستحقة الظاهرة في `GET /api/v1/founder/dashboard`.
- قارن Paid pilots delivered هذا الشهر بالشهر السابق.
- حدِّث خطة الـ60/90 يومًا في [`../commercial/COMMERCIAL_CONTROL_TOWER.md`](../commercial/COMMERCIAL_CONTROL_TOWER.md).

Monthly cadence review: read the monthly cadence output, review renewals due, compare paid pilots delivered month over month.

---

## غير القابل للتفاوض · Non-negotiables honored

- **لا فعل خارجي بلا موافقة** — القمرة تعرض وتقرّر؛ الإرسال يمرّ بصندوق الموافقة (`no_live_send`, `no_cold_whatsapp`).
- **لا تأكيد دفع تلقائي** — `no_live_charge`؛ تأكيد الدفع بمبادرة المؤسس.
- **لا نتائج مضمونة** — أرقام الإيراد موسومة بتيرات `value_os`: estimated / observed / verified / client_confirmed.
- **لا كود جديد** — القمرة مبنية على نقاط نهاية موجودة فقط.

---

> النتائج التقديرية ليست نتائج مضمونة / Estimated outcomes are not guaranteed outcomes.
