# Production Server Layout

## Purpose
Define how Dealix runs on the connected server.

## Paths
```txt
/opt/dealix
/opt/dealix-ops-private
/var/log/dealix
/etc/dealix
/var/lib/dealix
```

## Services

### API
FastAPI app.

### Web
Next.js / landing / dashboard.

### Workers
Background jobs for growth, scoring, approvals, follow-ups, reports.

### Database
Postgres.

### Queue
Redis later.

### Logs
Structured logs.

### Backups
Daily private ops and database backup.

## Non-Negotiables
- secrets stay outside repo
- private ops outside public repo
- no external sending without approval
- workers log every run
- failed worker alerts CEO
