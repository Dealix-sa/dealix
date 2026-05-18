# نظام التشغيل التنفيذي للمؤسس — Dealix

نقطة دخول واحدة لصباح المؤسس كـ CEO + founder: تجاري، تقني، وكلاء، إنتاج.

## صباح (30–45 دقيقة)

```bash
# الأقوى — كل الطبقات
bash scripts/run_founder_master_day.sh

# أو صباح تجاري مركّز
bash scripts/run_founder_commercial_day.sh

# Windows
powershell -File scripts/run_founder_commercial_day.ps1
$env:DEALIX_VERIFY_PROD = "1"
powershell -File scripts/run_founder_commercial_day.ps1
```

**مخرجات تلقائية:** `data/founder_briefs/brief_{date}.md` · `data/founder_briefs/executive_day_{date}.md` · `data/founder_agent/queue_today.json`

## تحقق إنتاج (أوامرك)

```powershell
py -3 scripts/verify_railway_production_config.py
curl.exe -fsS https://api.dealix.me/healthz
curl.exe -fsS https://api.dealix.me/version
```

أو:

```powershell
powershell -File scripts/founder_production_probe.ps1
```

| Endpoint | متوقع بعد نشر `main` |
|----------|----------------------|
| `/healthz` | 200 — `status`, `version`, `git_sha` |
| `/version` | 200 — هوية النشر |
| `/api/v1/meta` | 200 — سجل surfaces GTM |

إذا `/version` = 404 والـ repo أخضر: **ادفع `main` → انتظر CI → أعد نشر Railway** وصحّح UI (Start Command فارغ، Pre-deploy من toml).

## أسبوعي (أحد)

```bash
bash scripts/founder_weekly_loop.sh
powershell -File scripts/founder_weekly_loop.ps1
```

## طبقات المرجع

| طبقة | مرجع |
|------|------|
| Commercial OS | [MASTER_COMMERCIAL_OPERATING_PLAN_AR.md](../commercial/MASTER_COMMERCIAL_OPERATING_PLAN_AR.md) |
| GTM عميق | [DEALIX_SALES_GTM_SOVEREIGN_MASTER_AR.md](../commercial/DEALIX_SALES_GTM_SOVEREIGN_MASTER_AR.md) |
| CEO GTM | [CEO_GTM_OPERATING_SYSTEM_AR.md](CEO_GTM_OPERATING_SYSTEM_AR.md) |
| أسطول وكلاء | [AGENT_FLEET_OPERATING_SYSTEM_AR.md](../agentic_operations/AGENT_FLEET_OPERATING_SYSTEM_AR.md) |
| Railway | [RAILWAY_PRODUCTION_SETTINGS_AR.md](RAILWAY_PRODUCTION_SETTINGS_AR.md) |
| SKU | [COMMERCIAL_SKU_LADDER_AR.md](../commercial/COMMERCIAL_SKU_LADDER_AR.md) |
| ICP | [ICP_HYBRID_GTM_PLAYBOOK_AR.md](../commercial/operations/ICP_HYBRID_GTM_PLAYBOOK_AR.md) |
| 90 يوم | [data/commercial/90_day_activation_plan.yaml](../../data/commercial/90_day_activation_plan.yaml) |
| أول إغلاق | [FIRST_PAID_DIAGNOSTIC_DOD_AR.md](../commercial/operations/FIRST_PAID_DIAGNOSTIC_DOD_AR.md) |

## إيقاع القرار (CEO)

| التكرار | قرار |
|---------|------|
| يومي | 3 إجراءات من `executive_day_{date}.md` — لا أكثر |
| أسبوعي | قرار واحد في `data/founder_weekly/decision_*.yaml` |
| شهري | مراجعة SKU + ICP — لا عرض جديد بدون Proof Pack |

## ممنوعات

لا واتساب بارد · لا LinkedIn آلي · لا Gmail خارجي بدون موافقة · لا KPI مخترعة · لا upsell قبل Proof Pack.
