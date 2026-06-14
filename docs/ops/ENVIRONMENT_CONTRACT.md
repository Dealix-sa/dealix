# ENVIRONMENT CONTRACT — Dealix

## Required (Production Blocks Without These)

| Variable | Purpose | Validation |
|----------|---------|------------|
| `APP_SECRET_KEY` | Signing key (64-byte hex) | `_validate_production_secrets` rejects placeholders |
| `JWT_SECRET_KEY` | JWT signing (32+ chars) | Rejected if < 32 chars or contains "change-me" |
| `DATABASE_URL` | PostgreSQL | Auto-normalized `postgres://` → `postgresql+asyncpg://` |
| `ENVIRONMENT` | Runtime mode | `development` / `staging` / `production` |
| `API_KEYS` | Client API keys | Required comma-separated in production |
| `ADMIN_API_KEYS` | Admin API keys | Required for `/api/v1/admin/*` in production |

## Revenue (Required for Payments)

| Variable | Purpose | Default |
|----------|---------|---------|
| `MOYASAR_SECRET_KEY` | Payment gateway | `sk_live_REPLACE_ME` (sandbox) |
| `MOYASAR_WEBHOOK_SECRET` | Webhook verification | `REPLACE_with_shared_secret_from_dashboard` |
| `MOYASAR_LIVE_MODE` | Live mode toggle | `0` (sandbox); set `1` for live |
| `APP_URL` | Checkout callback URL | `https://dealix.sa` |

## Optional (Graceful Degradation)

| Variable | Purpose | When Missing |
|----------|---------|-------------|
| `OPENAI_API_KEY` | GPT models | OpenAI features disabled |
| `OPENROUTER_API_KEY` | Model routing | OpenRouter features disabled |
| `DEEPSEEK_API_KEY` | DeepSeek models | DeepSeek features disabled |
| `GROQ_API_KEY` | Groq inference | Groq features disabled |
| `ANTHROPIC_API_KEY` | Claude models | Claude features disabled |
| `GOOGLE_API_KEY` | Gemini models | Gemini features disabled |
| `HUBSPOT_ACCESS_TOKEN` | CRM sync | CRM sync skipped |
| `WHATSAPP_*` | WhatsApp integration | WhatsApp features disabled |
| `CALENDLY_URL` | Booking links | Calendly booking disabled |
| `POSTHOG_API_KEY` | Analytics | Analytics disabled |
| `REDIS_URL` | Cache/queue | In-memory fallback |
| `SENTRY_DSN` | Error tracking | Sentry disabled |

## Frontend-Only Variables (NEXT_PUBLIC_*)

| Variable | Purpose | Location |
|----------|---------|----------|
| `NEXT_PUBLIC_API_URL` | Backend URL | `frontend/src/lib/api.ts` |
| `NEXT_PUBLIC_APP_URL` | Public URL | SEO/metadata |
| `NEXT_PUBLIC_USE_DEALIX_OPS_PROXY` | Ops proxy toggle | Founder ops pages |

## Secret Safety Rules
- Server-only secrets NEVER use `NEXT_PUBLIC_` prefix
- `.env` is gitignored — never commit
- `.env.example` uses `REPLACE_ME` / `CHANGE_ME` placeholders
- `scripts/security_smoke.py` scans for live token patterns

## Env Template Locations
1. `.env.example` — 175 lines, primary template
2. `.env.railway.example` — Railway deployment
3. `frontend/.env.example` — Frontend dashboard
4. `apps/web/.env.example` — Legacy web app

## Audit Result
- ✅ No duplicate/conflicting env definitions between templates
- ✅ All placeholders use safe markers (REPLACE, CHANGE_ME, test-)
- ✅ Frontend variables correctly use NEXT_PUBLIC_* prefix
- ✅ Server-only secrets never exposed to frontend
- ✅ LLM providers are all optional
- ✅ `MOYASAR_LIVE_MODE=0` default prevents accidental charges
