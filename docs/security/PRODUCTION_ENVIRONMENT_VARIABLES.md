# Production environment variables — reference

This document is the **names-only** list of environment variables the
backend reads in production. Values live on Railway; nothing is committed
to git.

`scripts/verify_production_env.py` enforces presence; it never prints
values. CI runs it with `--ci` so missing values are tolerated but missing
**names** in `core.config.settings.Settings` are not.

## Required in `APP_ENV=production`

| Variable | Used for | Source of truth |
|---|---|---|
| `APP_ENV` | `Settings.app_env` | pydantic |
| `APP_SECRET_KEY` | Session/crypto | `Settings.app_secret_key` |
| `JWT_SECRET_KEY` | Auth tokens | `Settings.jwt_secret_key` |
| `API_KEYS` | `X-API-Key` allow-list (general) | `api.security.api_key` |
| `ADMIN_API_KEYS` | Admin paths + alt internal auth | `Settings.admin_api_keys` |
| `DEALIX_INTERNAL_TOKEN` | `X-Dealix-Internal-Token` for `/api/v1/internal/*` | `Settings.dealix_internal_token` |
| `DEALIX_PRIVATE_OPS` | Ledger root path | `Settings.dealix_private_ops` |
| `DATABASE_URL` | Postgres | `Settings.database_url` (auto-rewritten to `+asyncpg`) |
| `CORS_ORIGINS` | Browser allow-list | `Settings.cors_origins` |
| `PUBLIC_BASE_URL` | Smoke + email links | `Settings.public_base_url` |

You must set **either** `DEALIX_INTERNAL_TOKEN` **or** `ADMIN_API_KEYS`
(or both) to permit `/api/v1/internal/*` traffic in production.

## Kill switches

| Variable | Default | Purpose |
|---|---|---|
| `WHATSAPP_MOCK_MODE` | `true` | Block real WhatsApp send even when live flag is true |
| `WHATSAPP_ALLOW_LIVE_SEND` | `false` | Master flag; safe-send gateway still required |
| `WHATSAPP_DAILY_LIMIT` | `10` | Per-day outbound ceiling |

Computed: `Settings.is_live_send_allowed` is the only property other code
should consult. It returns `True` **only** when all three conditions hold:
production env, live flag on, mock mode off.

## Optional (warn-if-missing)

`GROQ_API_KEY`, `GOOGLE_SEARCH_API_KEY`, `GOOGLE_SEARCH_CX`,
`HUBSPOT_ACCESS_TOKEN`, `MOYASAR_SECRET_KEY`, `POSTHOG_HOST`, `SMTP_USER`,
`SMTP_PASSWORD`, `SMTP_FROM`, `GREEN_API_INSTANCE_ID`, `GREEN_API_TOKEN`.

## Never commit

This list is informational. Values must come from Railway Variables
**only**. The verifier prints `set` or `missing` for each — never the
value.
