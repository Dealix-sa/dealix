# Dealix — Working Guide (Sources of Truth)

Dealix is a Saudi-first B2B Revenue Operating System: approval-first, governance-native,
proof-driven AI revenue ops + compliance (PDPL/ZATCA). Service delivery, not pure SaaS.

This file exists to prevent drift. When a fact lives in more than one place, the
**canonical source** below wins — change it there first.

## Canonical sources of truth

| Concern | Canonical source | Notes |
|---|---|---|
| Offers & prices | `auto_client_acquisition/service_catalog/registry.py` (`OFFERINGS`) | Read by `GET /api/v1/pricing/plans` and `POST /api/v1/checkout`. Frontend mirrors it in `frontend/src/content/pricing.ts` (keep IDs/prices in sync). |
| The 11 non-negotiables | `dealix/commercial_ops/doctrine.py` | Enforced by tests (`tests/test_*doctrine*`, `tests/test_no_cold_whatsapp.py`, `tests/test_no_scraping_engine.py`, `tests/test_no_guaranteed_claims.py`). |
| Brand palette | Navy `#001F3F` + Gold `#D4AF37` + Sand `#F4F0E8` | Runtime: `frontend/tailwind.config` + `frontend/src/styles/dealix-brand.css`. Docs: `docs/sales-kit/dealix_brand_guidelines.md`. The green palette (`#0A4D3F`/`#C9A961`) is retired. |
| Public website | `frontend/` (Next.js 15, `app/[locale]/…`, i18n ar/en) | `landing/` is legacy static HTML — do not extend it. |
| Delivery SOP (7-day sprint) | `docs/PILOT_DELIVERY_SOP.md` | |
| Leads / targets | `docs/ops/lead_machine/*.csv` (+ `*.json`) | Real Saudi B2B targets. Imported into the war-room via the ops console. |

## The non-negotiables (summary — see doctrine.py)

No cold WhatsApp · no LinkedIn automation · no external send without approval ·
no scraping / purchased lists · no invented CRM/KPI numbers · no guaranteed-results
claims · no PII in external outputs · no source-less knowledge answers · no revenue
before invoice paid · no upsell before a delivered Proof Pack · every engagement
closes with a Proof Pack (≥70) + a capital asset.

Every external-facing output is a **draft for human approval**, never an auto-send.

## Run it

```bash
# Backend (FastAPI)
make run                      # http://localhost:8000 ; docs at /docs
make test                     # pytest (must pass doctrine tests before commit)
make lint && make type-check

# Frontend (Next.js)
cd frontend && npm install
npm run dev                   # http://localhost:3000  (default locale: /ar)
npm run typecheck && npm run build
```

## Public website map (`frontend/src/app/[locale]/`)

Marketing: `/` (home) · `/services` · `/pricing` · `/custom` (Custom AI intake) ·
`/dealix-diagnostic` · `/risk-score` · `/proof-pack` · `/about` · `/contact` ·
`/partners` · `/learn` · `/trust` · `/privacy` · `/terms`.
App/ops (gated): `/ops/*`, `/admin`, `/dashboard`, `/customer-portal`, …

Conventions:
- Add a page = create `app/[locale]/<route>/page.tsx` (file-system routing). Wrap
  public pages in `PublicGtmShell` or `PublicLaunchShell`; set metadata via
  `lib/gtmMetadata.ts`; add the route to `app/sitemap.ts`.
- Body copy is kept as in-component bilingual objects `{ ar, en }`; only `nav` and a
  few shared namespaces live in `frontend/messages/{ar,en}.json`.
- RTL for Arabic (`dir="rtl"`). No fabricated logos / stats / testimonials — pre-launch
  copy must be honest (no real customers yet).

## Money path (self-serve)

`/pricing` (or `/services` paid tiers) → `CheckoutPanel` → `POST /api/v1/checkout`
`{ plan, email }` (public, no admin key) → Moyasar invoice → `/checkout/return`.
Webhook: `POST /api/v1/webhooks/moyasar`. `APP_URL` must be the **web** origin
(`https://dealix.me`) so the callback resolves.

The Custom AI intake (`/custom`) posts to `POST /api/v1/public/custom-brief`
(doctrine-safe, draft-first, queued for founder review).

## Module layout

`auto_client_acquisition/` holds the `*_os` modules: `data_os`, `governance_os`,
`proof_os`, `value_os`, `capital_os`, `adoption_os` (incl. `friction_log`),
`service_catalog`, `revenue_ops_autopilot`, … Higher-order business logic in
`dealix/`. HTTP surface in `api/` (FastAPI, routers in `api/routers/`).
