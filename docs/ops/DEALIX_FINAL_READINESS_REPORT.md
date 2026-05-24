# Dealix Final Readiness Report

Generated: `2026-05-24T14:22:19.916258+00:00`

| Check | Verdict | Exit |
|------|---------|------|
| `production_env` | **PASS** | 0 |
| `railway_readiness` | **WARN** | 0 |
| `live_send_safety` | **PASS** | 0 |
| `railway_production_config` | **PASS** | 0 |

## `production_env` — PASS

```
python scripts/verify_production_env.py --ci
```

```
== verify_production_env ==
  mode: ci
  app_env: unset
  is_production: False
  -- required --
    JWT_SECRET_KEY: declared
    APP_SECRET_KEY: declared
    API_KEYS: declared
    APP_ENV: declared
    DEALIX_PRIVATE_OPS: declared
    DATABASE_URL: declared
    CORS_ORIGINS: declared
    PUBLIC_BASE_URL: declared
  -- internal auth (need ≥1) --
    DEALIX_INTERNAL_TOKEN: ok (ci)
    ADMIN_API_KEYS: ok (ci)
  -- optional (warn if missing) --
    GROQ_API_KEY: ci-skip
    GOOGLE_SEARCH_API_KEY: ci-skip
    GOOGLE_SEARCH_CX: ci-skip
    HUBSPOT_ACCESS_TOKEN: ci-skip
    MOYASAR_SECRET_KEY: ci-skip
    POSTHOG_HOST: ci-skip
    SMTP_USER: ci-skip
    SMTP_PASSWORD: ci-skip
    SMTP_FROM: ci-skip
    GREEN_API_INSTANCE_ID: ci-skip
    GREEN_API_TOKEN: ci-skip
    WHATSAPP_DAILY_LIMIT: ci-skip
  -- conflict rules --
    skipped (ci)

PRODUCTION_ENV_VERDICT=PASS
```

## `railway_readiness` — WARN

```
python scripts/verify_railway_readiness.py
```

```
== verify_railway_readiness ==
  WARN: Procfile 'release: alembic upgrade head' overlaps with railway.toml preDeployCommand (railway_predeploy.sh already runs alembic). Consider removing release: from Procfile.
  WARN: frontend secret allow-listed (tech debt): frontend/src/components/services/SprintToolsPanel.tsx — ['NEXT_PUBLIC_DEMO_API_KEY']
  WARN: frontend secret allow-listed (tech debt): frontend/src/components/brand/PublicLaunchShell.tsx — ['NEXT_PUBLIC_DEALIX_ADMIN_API_KEY']
  WARN: frontend secret allow-listed (tech debt): frontend/src/components/business/BusinessNowContent.tsx — ['NEXT_PUBLIC_DEALIX_ADMIN_API_KEY']
  WARN: frontend secret allow-listed (tech debt): frontend/src/components/revenue-autopilot/OpsConsoles.tsx — ['NEXT_PUBLIC_DEALIX_ADMIN_API_KEY']
  WARN: frontend secret allow-listed (tech debt): frontend/src/components/gtm/FounderCommandCenter.tsx — ['NEXT_PUBLIC_DEALIX_ADMIN_API_KEY']
  WARN: frontend secret allow-listed (tech debt): frontend/src/components/gtm/OpsTargetingPanel.tsx — ['NEXT_PUBLIC_DEALIX_ADMIN_API_KEY']
  WARN: frontend secret allow-listed (tech debt): frontend/src/components/gtm/OpsPartnersPanel.tsx — ['NEXT_PUBLIC_DEALIX_ADMIN_API_KEY']
  WARN: frontend secret allow-listed (tech debt): frontend/src/components/gtm/OpsHubHealthCards.tsx — ['NEXT_PUBLIC_DEALIX_ADMIN_API_KEY']
  WARN: frontend secret allow-listed (tech debt): frontend/src/lib/api.ts — ['NEXT_PUBLIC_DEALIX_ADMIN_API_KEY']
RAILWAY_READINESS_VERDICT=WARN
```

## `live_send_safety` — PASS

```
python scripts/verify_live_send_safety.py
```

```
== verify_live_send_safety ==
  ok: all live-send safety gates wired
LIVE_SEND_SAFETY_VERDICT=PASS
```

## `railway_production_config` — PASS

```
python scripts/verify_railway_production_config.py --skip-live
```

```
== verify_railway_production_config ==
  WARN: Dockerfile HEALTHCHECK should prefer /healthz
  ok: repo railway config
  live /healthz: https://api.dealix.me/healthz -> 200
  live healthz: https://api.dealix.me/healthz -> 200
  live version: https://api.dealix.me/version -> 200
  live api_v1_meta: https://api.dealix.me/api/v1/meta -> 200
  live health: https://api.dealix.me/health -> 200
  settings: docs/ops/RAILWAY_PRODUCTION_SETTINGS_AR.md
RAILWAY_PRODUCTION_CONFIG_VERDICT=PASS
```
