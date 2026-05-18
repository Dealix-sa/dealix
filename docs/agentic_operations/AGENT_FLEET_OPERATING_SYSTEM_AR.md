# نظام تشغيل أسطول الوكلاء — Dealix

**عقود YAML:** [`dealix/config/agent_fleet_io.yaml`](../../dealix/config/agent_fleet_io.yaml) · [`dealix/config/founder_agent_task_queue.yaml`](../../dealix/config/founder_agent_task_queue.yaml) · [`dealix/config/ceo_agent_roster.yaml`](../../dealix/config/ceo_agent_roster.yaml)

## صباح واحد (ترتيب التنفيذ)

| # | الوكيل | أمر / مخرج |
|---|--------|------------|
| 1 | **dealix-pm** | `bash scripts/run_founder_commercial_day.sh` يبدأ اليوم |
| 2 | **dealix-pm** | `founder_north_star_status.py` — شمال منتج/تجاري |
| 3 | **الكل** | `run_founder_agent_fleet_rhythm.sh` — بذر `queue_today.json` + حزم |
| 4 | **dealix-engineer** | `verify_railway_production_config.py` / `railway_ui_alignment.sh` |
| 5 | **dealix-sales** | مسودات War Room — موافقة فقط |
| 6 | **dealix-delivery** | Proof Pack checklist |
| 7 | **dealix-content** | مسودة AEO/LinkedIn — موافقة فقط |

## مصدر الحقيقة

- خطة 90 يوم: [`data/commercial/90_day_activation_plan.yaml`](../../data/commercial/90_day_activation_plan.yaml)
- طابور اليوم: `data/founder_agent/queue_today.json` عبر `founder_agent_queue_status.py --seed-today`

## مراجع

- [`docs/ops/AGENT_DAILY_WORK_PACKETS_AR.md`](../ops/AGENT_DAILY_WORK_PACKETS_AR.md)
- [`docs/ops/FOUNDER_AGENT_PLAYBOOK_AR.md`](../ops/FOUNDER_AGENT_PLAYBOOK_AR.md)
