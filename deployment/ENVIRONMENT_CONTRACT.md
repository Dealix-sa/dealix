# Dealix Environment Contract

## Required
- `APP_ENV`: development | staging | production
- `NEXT_PUBLIC_SITE_URL`: public website URL
- `LEADS_STORAGE_MODE`: jsonl | database | webhook

## Optional
- `DATABASE_URL`: Postgres connection string
- `POSTHOG_KEY`: analytics key
- `HUBSPOT_ACCESS_TOKEN`: CRM sync
- `SLACK_WEBHOOK_URL`: internal alerts
- `SMTP_HOST`, `SMTP_USER`, `SMTP_PASSWORD`: email sending, if enabled

## Forbidden in public frontend
- API private keys
- database credentials
- SMTP passwords
- CRM private tokens
- payment secrets
