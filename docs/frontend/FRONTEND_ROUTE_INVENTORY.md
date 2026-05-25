# Frontend Route Inventory (canonical)

> Generated mirror lives at `FRONTEND_ROUTE_INVENTORY.generated.md` (built by
> `scripts/generate_frontend_route_inventory.py`). This file is the *curated*
> view with ownership, purpose, and trust status.

## Required Route Classes

### Public Marketing (landing/)
- `/` — Dealix home (index.html)
- `/pricing.html` — Anchor pricing
- `/diagnostic.html` — Free diagnostic
- `/checkout.html` — Sprint / Data Pack checkout
- `/case-study.html`
- `/proof.html`
- `/trust-center.html`
- `/agency-partner.html`

### Founder Internal (apps/web)
- `/ceo` — CEO Command Center
- `/sales-cockpit` — Sales pipeline
- `/approvals` — Approval Center
- `/distribution` — Channels × sectors
- `/workers` — Worker health
- `/trust` — Policy decisions
- `/finance` — Cash · MRR · runway

### Customer (frontend/)
- `/[locale]/customer-portal`
- `/[locale]/onboarding`
- `/[locale]/reports`

### Partner
- `/agency-partner.html` (landing)
- `/partner-referral.html` (landing, if exists)

## Required Metadata (per route)
Every route in this inventory must have:
- **owner** — who maintains it
- **purpose** — what decision it serves
- **CTA** — single primary action
- **data source** — API endpoint or static
- **trust status** — public / admin-key / founder-only
- **build status** — F0 / F1 / F2 / F3 / F5

## Founder P0 — current status

| Route | Owner | Purpose | Data source | Trust | Build |
|---|---|---|---|---|---|
| `/ceo` | Founder | One-screen control | `/api/v1/business-now/snapshot` | founder | F2 |
| `/sales-cockpit` | Founder | Pipeline | `/api/v1/sales`, `/api/v1/revenue-pipeline` | founder | F2 |
| `/approvals` | Founder | Approval inbox | `/api/v1/approvals` | founder | F2 |
| `/distribution` | Founder | Channels × sectors | `/api/v1/expansion-engine` | founder | F2 |
| `/workers` | Founder | Machine health | `/api/v1/observability` | founder | F2 |
| `/trust` | Founder | Policy decisions | `/api/v1/safety`, audit sink | founder | F2 |
| `/finance` | Founder | Cash · MRR · runway | `/api/v1/finance` | founder | F2 |
