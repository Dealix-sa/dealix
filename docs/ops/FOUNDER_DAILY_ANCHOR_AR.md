# مرساة اليوم — المؤسس (الإيقاع الذهبي)

**الغرض:** نقطة دخول واحدة كل صباح قبل أي شيء آخر. تربط النجم الشمالي (3 أرقام) + الإيقاع اليومي + الـ Master Plan.

> **الـ source of truth الأعلى:** [`/MASTER_PLAN.md`](../../MASTER_PLAN.md) — اقرأ عند تعارض، الـ master plan يفوز.

---

## النجم الشمالي — 3 أرقام فقط

| KPI | الهدف نهاية الشهر 12 | اليوم |
|---|---|---|
| **MRR** | 83K SAR | ___ (املأ من `pipeline_tracker.csv`) |
| **Active Paid Customers** | 20-22 | ___ |
| **Founder Touches/Day** | ≥ 5 (ثابت) | ___ من 5 |

أي رقم رابع = إلهاء. اتركه.

---

## الإيقاع اليومي (محمي)

| الوقت | النشاط | المخرَج |
|---|---|---|
| 09:00 | قراءة daily brief | `python scripts/dealix_pm_daily.py` → `data/daily_brief/YYYY-MM-DD.md` |
| 09:15-10:30 | **5 لمسات مبيعات** (مقدّس) | كل لمسة تُسجَّل في `pipeline_tracker.csv` |
| 10:30-12:30 | تسليم/تشغيل Sprint نشط | تحديث Proof Pack draft |
| 12:30-14:00 | غداء + استراحة | لا عمل |
| 14:00-16:00 | bug fix (من friction_log فقط) أو محتوى | PR draft أو LinkedIn post |
| 16:00 | تحديث pipeline + friction log | `pipeline_tracker.csv` + `friction_log/store.jsonl` |
| 17:00 | إنهاء اليوم | حماية الطاقة — لا عمل بعد 17:00 |

**اتصال خارجي محدود:**
- LinkedIn/X: 30 دقيقة/يوم فقط للنشر والرد. لا scroll.
- WhatsApp business: 10:30، 14:00، 16:30 فقط.
- إيميل: 11:00 و 15:00 فقط.

---

## الـ 5 لمسات اليومية بالتفصيل

1. **DM #1** — lead جديد من `pipeline_tracker.csv` (priority_rank 1 لم يُلمس بعد)
2. **DM #2** — lead جديد آخر (priority_rank التالي)
3. **Follow-up** — DM مُرسَل قبل 3+ أيام بدون رد
4. **رد على رد** — أي رد جاء من lead أو محادثة قائمة
5. **تأكيد/عرض** — حجز موعد جاء + إرسال calendar invite، أو إرسال proposal لـ demo سابق

كل لمسة = صف في `pipeline_tracker.csv` بتوقيت + channel + message_version.

---

## الإيقاع الأسبوعي

| اليوم | الوقت | النشاط |
|---|---|---|
| **الأحد** | 09:00 | مراجعة `dealix-pm` للأرقام الثلاثة + Gate check |
| **الأربعاء** | 09:00 | friction_log review + قرار "نبني أم نتأجل" |
| **الخميس** | 16:00 | weekly report + قرار الأسبوع القادم |
| **الجمعة** | كامل | إجازة (حماية الطاقة) |

**القرار الواحد الأسبوعي:** يُسجَّل في [`FOUNDER_WEEKLY_ONE_DECISION_AR.md`](FOUNDER_WEEKLY_ONE_DECISION_AR.md). قرار واحد فقط/أسبوع — الباقي يُؤجَّل أو يُفوَّض لـ sub-agents.

---

## حالة المؤسس الذهنية اليومية

قبل بدء اليوم، قيّم طاقتك من 10:

- **< 5/10 (يوم سيء):** 5 لمسات + Sprint delivery قائم فقط. **لا قرارات استراتيجية. لا فلسفة. لا متابعة LinkedIn news.**
- **5-7/10 (متوسط):** الروتين العادي كاملاً.
- **8-10/10 (ممتاز):** الروتين + تنفيذ القرار الأسبوعي + شيء جديد (نشر case study، اجتماع شريك، تعيين موعد كبير).

**لا تعاقب نفسك على يوم سيء.** الانهيار = خسارة الشركة. الحفاظ على الطاقة = KPI تجاري.

---

## المراجع الأساسية (افتح حسب الحاجة فقط)

| متى | الملف |
|---|---|
| Master plan (الأعلى) | [/MASTER_PLAN.md](../../MASTER_PLAN.md) |
| pipeline tracking | [pipeline_tracker.csv](pipeline_tracker.csv) |
| DMs جاهزة | [launch_content_queue.md](launch_content_queue.md) |
| Demo script (30 دقيقة) | [../sales-kit/DEALIX_MASTER_PLAYBOOK.md](../sales-kit/DEALIX_MASTER_PLAYBOOK.md) |
| Sprint delivery template | [FIRST_CUSTOMER_DELIVERY_TEMPLATE.md](FIRST_CUSTOMER_DELIVERY_TEMPLATE.md) |
| Control Center (Gates) | [COMPANY_CONTROL_CENTER.md](COMPANY_CONTROL_CENTER.md) |
| Weekly review SOP | [friction_log_review_weekly.md](friction_log_review_weekly.md) |
| Operating system (طويل) | [FOUNDER_OPERATING_SYSTEM_AR.md](FOUNDER_OPERATING_SYSTEM_AR.md) |

---

## أوامر سريعة

```bash
# الموجز الصباحي
python scripts/dealix_pm_daily.py

# حالة موحدة (إذا كانت متاحة)
python scripts/founder_comprehensive_plan_status.py 2>/dev/null

# تحقق sprint capacity
grep -c "in_delivery" docs/ops/pipeline_tracker.csv
# إذا ≥ 4 → STOP بيع Sprint جديد
```

---

## القاعدة الذهبية

> **القرار اليومي الوحيد المهم:** هل أرسلت 5 لمسات اليوم؟
> كل شيء آخر ثانوي. كل feature، كل deploy، كل LinkedIn post، كل اجتماع.
> 5 لمسات أولاً. الباقي بعد.

---

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة*

*Version 2.0 — 2026-05-24 — Replaces 2026-05-18 version. Aligned with MASTER_PLAN.md.*
