# Vercel Environment Template for Dealix

Use this as a checklist in Vercel Project Settings. Do not paste real secret values into the repository.

## Runtime identity

```text
APP_ENV=production
ENVIRONMENT=production
APP_LOG_LEVEL=INFO
LOG_LEVEL=INFO
```

## Public URLs

```text
APP_URL=https://dealix.me
BASE_URL=https://dealix.me
DEALIX_API_BASE=https://api.dealix.me
CORS_ORIGINS=https://dealix.me,https://www.dealix.me,https://api.dealix.me,https://dealix.vercel.app
```

## Safety defaults

```text
EXTERNAL_SEND_ENABLED=false
OUTBOUND_MODE=draft_only
EMAIL_SEND_ENABLED=false
WHATSAPP_SEND_ENABLED=false
WHATSAPP_ALLOW_LIVE_SEND=false
SMS_SEND_ENABLED=false
```

## Production-only secure values

If the FastAPI API itself is deployed as production on Vercel, configure real secure values in Vercel only:

```text
APP_SECRET_KEY=<generated value>
JWT_SECRET_KEY=<generated value>
API_KEYS=<generated value list>
ADMIN_API_KEYS=<generated value list>
```

## Frontend project value

If `apps/web` is deployed as a separate Vercel project named `dealix-web`, add:

```text
NEXT_PUBLIC_DEALIX_API_BASE=https://api.dealix.me
```
