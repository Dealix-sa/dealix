# سياسة إنتاج Railway — Dealix

## Pre-deploy

| الحالة | السلوك |
|--------|--------|
| افتراضي | `RAILWAY_PREDEPLOY: SKIP` — لا ترحيل |
| `RUN_RAILWAY_PRE_DEPLOY_MIGRATE=1` + `DATABASE_URL` | `alembic upgrade head` |
| `RUN_RAILWAY_PRE_DEPLOY_MIGRATE=0` | تخطي صريح |

الأمر في [`railway.toml`](../../railway.toml): `sh /app/scripts/railway_predeploy.sh`

**ممنوع في UI:** `echo "no migration needed"`

## Start command

- **مسموح:** فارغ · `/app/start.sh`
- **ممنوع:** `./start.sh` · `uvicorn ...` بدون توسيع `$PORT`

## Probes بعد النشر

```bash
curl -fsS https://api.dealix.me/healthz
curl -fsS https://api.dealix.me/version
curl -fsS https://api.dealix.me/api/v1/meta
python scripts/verify_railway_production_config.py
```

إذا `/version` يعيد 404 والكود على `main` يحتوي المسار — أعد النشر بعد CI.

## مراجع

- [RAILWAY_PRODUCTION_SETTINGS_AR.md](RAILWAY_PRODUCTION_SETTINGS_AR.md)
- [dealix/config/railway_ui_canonical.yaml](../../dealix/config/railway_ui_canonical.yaml)
