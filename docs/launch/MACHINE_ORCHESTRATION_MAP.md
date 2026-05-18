# Dealix — خريطة تنظيم المكاين · Machine Orchestration Map

**الحالة / Status:** DRAFT
**المالك / Owner:** Sami (founder)
**آخر تحديث / Last updated:** 2026-05-18
**وثائق مرافقة / Companion docs:** `CEO_LAUNCH_COCKPIT.md` · `FIRST_PILOT_PLAYBOOK.md` · `../V14_FOUNDER_DAILY_OPS.md` · `../commercial/COMMERCIAL_CONTROL_TOWER.md`

---

## الغرض · Purpose

هذه خريطة كاملة لكل "مكينة" أتمتة في Dealix، وكيف تنتظم جميعها في إيقاع واحد محكوم بالموافقة. المكاين تُحضّر وتصفّ — المؤسس يوافق.

This is a complete map of every automation "machine" in Dealix and how they fit one approval-gated rhythm. Machines prepare and queue; the founder approves.

---

## المكاين المجدولة — GitHub Actions cron · Scheduled machines

### المكاين القائمة · Existing workflows

| المكينة · Machine | الإيقاع · Cadence | المُطلِق · Trigger | ما تُنتجه · Produces | أين تصفّ للموافقة · Queues for approval |
|---|---|---|---|---|
| `daily-revenue-machine.yml` | يوميًا 04:00 UTC | cron | مسودات Gmail / LinkedIn / مكالمات / شركاء — لا تُرسَل أبدًا تلقائيًا | `approval_center` |
| `daily_digest.yml` | يوميًا 04:00 UTC | cron | ملخص بريد للمؤسس | بريد المؤسس (إخباري — لا فعل خارجي) |
| `daily_snapshot.yml` | يوميًا 05:00 UTC | cron | لقطة تدقيق (audit snapshot) | سجل تدقيق (لا موافقة) |
| `watchdog_drift.yml` | كل ساعة | cron | كشف انحراف (drift detection) | تنبيه للمؤسس عند انحراف |
| `scheduled_healthcheck.yml` | كل 15 دقيقة | cron | فحص صحة النظام | تنبيه عند فشل فقط |
| `dlq_check.yml` | كل 30 دقيقة | cron | فحص طابور الرسائل الميتة (DLQ) | تنبيه عند تراكم |
| `weekly_self_improvement.yml` | الأحد | cron | 3 اقتراحات تحسين | `approval_center` (صندوق الموافقة) |
| `reliability_drills_scorecard.yml` | الاثنين | cron | بطاقة نتائج تمارين الموثوقية | تقرير للمؤسس |

### المكاين الجديدة في هذا التغيير · New workflows added in this change

| المكينة · Machine | الإيقاع · Cadence | السكربت · Script | ما تُنتجه · Produces |
|---|---|---|---|
| `daily_lead_prep.yml` | يوميًا 03:30 UTC | `scripts/dealix_daily_lead_prep.py` | تحضير leads — **مسودات فقط (drafts only)** |
| `weekly_brief.yml` | الأحد 03:00 UTC | `scripts/weekly_brief_runner.py --all-active` | موجز أسبوعي لكل العملاء النشطين |
| `monthly_cadence.yml` | أول الشهر 03:00 UTC | `scripts/monthly_cadence_runner.py --all-active --schedule-renewals` | إيقاع شهري + جدولة تجديدات |

كل المخرجات أعلاه مسودات أو تقارير — لا فعل خارجي يُنفَّذ بلا موافقة.

---

## المكاين عند الطلب · On-demand machines

تُشغَّل يدويًا من المؤسس، لا بجدول:

- `scripts/warm_list_outreach.py` — تحضير لمسات دافئة لقائمة معروفة (مسودات تصفّ للموافقة).
- `scripts/dealix_proof_pack.py` — توليد Proof Pack من 14 قسمًا لعميل.
- `scripts/founder_daily_scorecard.py` — بطاقة نتائج المؤسس اليومية.

---

## مركز الموافقة · The approval center

كل فعل خارجي يصفّ في `auto_client_acquisition/approval_center/` عبر `ApprovalStore`. لا توجد قناة تتجاوزه.

- توجد **11 نوع فعل قانونيًا (canonical action types)**.
- المؤسس يراجع عبر `GET /api/v1/approvals/pending` ثم **يوافق / يرفض / يعدّل**.
- **WhatsApp / LinkedIn / الهاتف لا تُوافَق تلقائيًا أبدًا** — تتطلب موافقة صريحة في كل مرة.

Every external action queues in `auto_client_acquisition/approval_center/` via `ApprovalStore`. There are 11 canonical action types. The founder reviews via `GET /api/v1/approvals/pending` and approves, rejects, or edits. WhatsApp / LinkedIn / phone never auto-approve.

---

## المبدأ الحاكم · Governing principle

**المكاين تُحضّر وتصفّ؛ المؤسس يوافق عند كل حدّ خارجي.** هذا هو المعنى الوحيد لكلمة "تلقائي" في Dealix — تحضير مجدول، لا إرسال مجدول. هذا ما يُبقي `no_live_send` و`no_cold_whatsapp` سليمين.

Machines prepare and queue; the founder approves at every external boundary. That is the only meaning of "automatic" here — scheduled preparation, never scheduled sending. This keeps `no_live_send` and `no_cold_whatsapp` intact.

تجميد تجاري نشط (Commercial Freeze): الأولوية هي البيع وإنهاء تسليم Tier 0–1 وأول Pilot مدفوع — لا بناء جديد لـTier 2–5.

---

> النتائج التقديرية ليست نتائج مضمونة / Estimated outcomes are not guaranteed outcomes.
