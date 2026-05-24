# مرساة اليوم — المؤسس (3 مراجع + تنفيذ)

**الغرض:** نقطة دخول صباحية واحدة قبل أي مستند آخر — تربط نظام التشغيل، الخطة التجارية 5 دقائق، وغرفة التصريف.

---

## المراجع الثلاثة (ثابتة)

| # | متى | المستند |
|---|-----|---------|
| 1 | تشغيل + حوكمة | [FOUNDER_OPERATING_SYSTEM_AR.md](FOUNDER_OPERATING_SYSTEM_AR.md) |
| 2 | 5 دقائق Control Tower | [MASTER_COMMERCIAL_OPERATING_PLAN_AR.md](../commercial/MASTER_COMMERCIAL_OPERATING_PLAN_AR.md) |
| 3 | أعلى 10 + متابعات | [DEALIX_REVENUE_WAR_ROOM_AR.md](DEALIX_REVENUE_WAR_ROOM_AR.md) |

**تنفيذ الخطة الشاملة (بحث + Dealix):** [FOUNDER_COMPREHENSIVE_PLAN_EXECUTION_AR.md](FOUNDER_COMPREHENSIVE_PLAN_EXECUTION_AR.md)

---

## أقصى أتمتة (فل أوبس ذاتي — موصى به)

```bash
py -3 scripts/run_dealix_complete_autonomous_day.py
# أو من الواجهة: /ar/ops/founder → «شغّل يوم موحّد كامل»
py -3 scripts/run_dealix_unified_founder_day.py
```

مقارنة السوق: موجز صباحي + مسودات (Management OS / Zealos) — Dealix يضيف حوكمة PDPL، بوابة 0–1، وأدلة CSV. التفاصيل: [FULL_AUTONOMOUS_COMMERCIAL_OPS_AR.md](../commercial/FULL_AUTONOMOUS_COMMERCIAL_OPS_AR.md).

---

## تسلسل الصباح (10–15 دقيقة)

1. `bash scripts/founder_launch_day0.sh` (بوابة يوم 0 — ops-autopilot + AI runtime)
2. `bash scripts/run_founder_agent_fleet_rhythm.sh` (حزم الوكلاء)
3. `bash scripts/run_founder_commercial_day.sh --full` (أو `founder_cadence.sh`)
4. افتح الموجز: `data/founder_briefs/commercial_YYYY-MM-DD.md`
5. نفّذ مسار الـ 5 دقائق من MASTER (War Room → Evidence)
6. `/ar/ops/founder` · `/ar/ops/war-room` · `/ar/ops/approvals` (يتطلب `AUTOPILOT_ROUTERS` في API)

**API محلي:** `GET /api/v1/ops-autopilot/war-room/today-pack` · `GET /api/v1/ai-runtime/status` (مفتاح admin)

**حالة موحّدة:**

```bash
py -3 scripts/founder_comprehensive_plan_status.py
```

---

## المساء والجمعة

| وقت | أمر |
|-----|-----|
| مساء | `powershell -File scripts/founder_cadence.ps1 -Evening` |
| جمعة | `powershell -File scripts/founder_cadence.ps1 -Weekly` |

---

*آخر تحديث: 2026-05-18*
