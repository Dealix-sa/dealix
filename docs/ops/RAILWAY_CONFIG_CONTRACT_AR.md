# Railway Config Contract — عقد إعدادات Railway (مُلزَم آليًا)

هذا المستند يوثّق **العقد المُلزَم آليًا** لإعدادات Railway الإنتاجية. المصدر الوحيد
للحقيقة هو `dealix/config/railway_ui_canonical.yaml`، ويتم فرضه عبر اختبار وسكربت تحقق —
أي انحراف (drift) يصير فشلًا صريحًا وليس تحذيرًا صامتًا.

## المصدر الوحيد للحقيقة | Single source of truth

`dealix/config/railway_ui_canonical.yaml`

كل قيمة في `railway.toml` و`railway.json` و`Dockerfile` تُقارَن بهذا الملف.

## العقد | The contract

| المفتاح | القيمة الأساسية (canonical) | يُفرَض في |
|--------|------------------------------|-----------|
| `build.builder` | `DOCKERFILE` | railway.toml, railway.json |
| `build.dockerfilePath` | `Dockerfile` | railway.toml, railway.json |
| `deploy.startCommand` | **فارغ / null** — لا يُضبط أبدًا | railway.toml (محذوف), railway.json (`null`) |
| بدء التشغيل الفعلي | Dockerfile `CMD ["/app/start.sh"]` → uvicorn يقرأ `$PORT` | Dockerfile |
| `deploy.healthcheckPath` | `/healthz` | railway.toml, railway.json |
| `deploy.healthcheckTimeout` | `300` | railway.toml, railway.json |
| `deploy.restartPolicyType` | `ON_FAILURE` | railway.toml, railway.json |
| `deploy.restartPolicyMaxRetries` | `3` | railway.toml, railway.json |
| `deploy.preDeployCommand` | يستدعي `scripts/railway_predeploy.sh` | railway.toml, railway.json |
| `deploy.numReplicas` | `1` | railway.toml, railway.json |

### أوامر بدء ممنوعة | Forbidden start commands

هذه القيم يجب ألا تظهر في `railway.toml` أو `railway.json` أو حقل Start Command في لوحة Railway:

- `uvicorn api.main:app` (يكسر توسيع `$PORT` ويتجاوز نقطة دخول Dockerfile)
- `./start.sh` (مسار خاطئ — الصحيح `/app/start.sh` من Dockerfile CMD)

**القاعدة:** اترك حقل Start Command في لوحة Railway **فارغًا** ليعمل Dockerfile `CMD`.

## لماذا لا نضبط `startCommand`؟

Dockerfile يُنشئ `/app/start.sh` الذي ينفّذ:

```sh
exec uvicorn api.main:app --host 0.0.0.0 --port "${PORT:-8000}" --workers 1
```

هذا سكربت shell حقيقي يوسّع `${PORT:-8000}` الذي تحقنه Railway. ضبط `startCommand`
مباشرةً في config-as-code أو في اللوحة يكرّر المنطق ويخاطر بكسر توسيع المنفذ.

## كيف يُفرَض العقد | Enforcement

| الطبقة | الأمر | ماذا يفعل |
|--------|-------|-----------|
| اختبار | `pytest tests/test_railway_config_foundation.py` | يقفل كل مفتاح مقابل canonical + يتحقق أن الحارس يكتشف الانحراف فعليًا |
| سكربت (repo) | `make railway-config-verify` | `verify_railway_production_config.py --skip-live` — فحص الريبو فقط |
| سكربت (حي) | `python3 scripts/verify_railway_production_config.py` | نفس الفحص + probe حي لـ `/healthz` على الإنتاج |
| كود | `dealix.commercial_ops.railway_production.check_config_matches_canonical()` | يقارن toml/json/Dockerfile بـ canonical yaml |

انحراف أي قيمة → `RAILWAY_PRODUCTION_CONFIG_VERDICT=FAIL` وفشل الاختبار.

## ماذا لا تفعل | What NOT to do

- لا تُعِد إضافة `startCommand` إلى `railway.toml` أو `railway.json`.
- لا تملأ حقل Start Command في لوحة Railway — اتركه فارغًا.
- لا تُغيّر `builder` إلى `NIXPACKS`.
- لا تحذف `healthcheckPath`.
- لا تُضعف حارس أسرار الإنتاج (`api/main.py:_validate_production_secrets`) لتشغيل Railway.
- إذا تعطّل Railway: أصلح الفوترة والمصدر والمتغيرات — راجع
  [`RAILWAY_RECOVERY_RUNBOOK.md`](RAILWAY_RECOVERY_RUNBOOK.md).

## مستندات ذات صلة | Related

- [`RAILWAY_PRODUCTION_SETTINGS_AR.md`](RAILWAY_PRODUCTION_SETTINGS_AR.md) — إعدادات اللوحة
- [`RAILWAY_GO_LIVE_CHECKLIST.md`](RAILWAY_GO_LIVE_CHECKLIST.md) — قائمة الإطلاق
- [`RAILWAY_RECOVERY_RUNBOOK.md`](RAILWAY_RECOVERY_RUNBOOK.md) — إجراء الاستعادة
