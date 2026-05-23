# Founder Console Production Gate

## Purpose

Define when the Founder Console is truly ready for daily use — not just
when pages render.

## Gates

| Gate | Name | Check |
| --- | --- | --- |
| F1 | Build Ready | `apps/web` `npm run build` passes |
| F2 | Route Ready | All 10 founder routes exist and render |
| F3 | API Ready | `/api/v1/internal/*` endpoints return JSON |
| F4 | Action Ready | approve / reject / request-edit endpoints exist |
| F5 | Trust Ready | approval actions write audit and pass policy evaluator |
| F6 | Runtime Ready | pages show real source data, not fallback zeros |
| F7 | Daily Use Ready | Sami can open `/ceo` and get one top action |

## Not Ready If

- Frontend only shows fallback / placeholder values.
- Approval buttons do not write to the audit ledger.
- Internal API is not authenticated for the founder session.
- An external action (WhatsApp, payment, email) can bypass Trust Plane.
- Metrics are hard-coded in the UI.
- `apps/web` `npm run build` fails on `main`.
- Server-rendered data is older than the SLA defined per worker.

## Rule

Founder Console is **production-ready** only when **F1 → F5** all pass.
F6 and F7 are graduation gates from "production-ready" to "Sami's
single screen".

## Current State (as of v2 runtime layer PR)

| Gate | Status |
| --- | --- |
| F1 Build Ready | enforced by `scripts/verify_founder_console_v2.py` |
| F2 Route Ready | enforced by verifier (10 page paths checked) |
| F3 API Ready | enforced by `scripts/verify_internal_api_layer.py` |
| F4 Action Ready | router exposes approve / reject / request-edit |
| F5 Trust Ready | not yet — audit + policy wiring is the next PR |
| F6 Runtime Ready | not yet — sources return safe zeros |
| F7 Daily Use Ready | not yet — depends on F5 + F6 |
