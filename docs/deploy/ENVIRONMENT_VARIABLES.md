# Environment Variables Reference

## Required
| Variable | Example | Purpose |
|----------|---------|---------|
| APP_ENV | development | development / staging / production |
| DATABASE_URL | postgresql+asyncpg://... | Postgres connection |
| APP_SECRET_KEY | long-random-string | JWT/signing |

## Optional
| Variable | Example | Purpose |
|----------|---------|---------|
| REDIS_URL | redis://localhost:6379 | Cache/queue |
| HUBSPOT_ACCESS_TOKEN | ... | CRM sync |
| MOYASAR_SECRET_KEY | ... | Payments |
| MOYASAR_PUBLISHABLE_KEY | ... | Payments frontend |
| CALENDLY_URL | ... | Booking link |

## Frontend
| Variable | Example | Purpose |
|----------|---------|---------|
| NEXT_PUBLIC_API_URL | http://localhost:8000 | API base |
| NEXT_PUBLIC_DEALIX_ADMIN_API_KEY | ... | Ops UI local |

## Safety
- Never commit `.env`
- Rotate keys quarterly
- Use Railway/Vercel dashboard for secrets
