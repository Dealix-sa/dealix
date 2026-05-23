# Founder Console Architecture v3

## Flow

```
Frontend
  → Internal API
    → Trust Plane
      → Data Source
      → Audit Log
      → Worker Queue
      → External Action (only if approved)
```

## Frontend

Next.js app in `apps/web`. Pages live under `apps/web/app/<route>/page.tsx`.
A unified `FounderShell` component frames every page with the founder nav.

## Internal API

FastAPI routes under `/api/v1/internal/*`. Defined in
`api/routers/internal/founder_console.py`. Self-prefixed and registered from
`api/main.py`.

## Data Sources

- Postgres later (canonical).
- Private ops CSV while bootstrapping (`/opt/dealix-ops-private/...`).
- Worker reports for runtime status.
- Audit logs for trust decisions.

## Trust Plane

Must evaluate, before any approval permits an external action:

- approval class (A0/A1/A2/A3)
- reversibility
- sensitivity
- suppression
- no-overclaim
- evidence presence
- never-auto-execute list

## Audit

Every approval decision writes:

- approval_id
- decision
- actor
- reason
- timestamp
- policy_result
- source_endpoint
- external_action_allowed

## Rule

The UI never performs external-impacting actions directly. The UI sends a
decision to the internal API; the Trust Plane evaluates; the worker queue
or human operator executes.
