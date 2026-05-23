# Founder Console Runtime Binding Plan

## Purpose

Move the Founder Console from a buildable skeleton to a live operating
interface. Each phase below preserves the shape of `dealix-runtime.ts`
TypeScript types so that the frontend never needs structural rework
between phases.

## Phase 1 — Buildable (this PR)

- All 10 pages exist under `apps/web/app/<slug>/page.tsx`
- `FounderShell` renders a working sidebar on every page
- `apps/web/lib/dealix-runtime.ts` exposes `safeGet<T>` and the public types
- `api/routers/internal/founder.py` registers 7 endpoints, each gated by
  `require_super_admin`, each returning placeholder JSON
- `apps/web/` builds clean via `npm run build`
- `make founder-console` exits 0
- `.github/workflows/dealix-founder-console.yml` runs on PR and push to main

## Phase 2 — Read-only runtime binding

Replace placeholder JSON with real data, **without** changing response
shapes:

| Endpoint | Real source |
|----------|-------------|
| `/ceo/summary` | aggregate from `founder_dashboard` + `execution_assurance.health` + finance counters |
| `/sales/funnel` | counts from existing sales / outreach tables |
| `/approvals` | live items from `dealix/trust/ApprovalCenter` |
| `/workers/health` | runtime worker registry + last-run timestamps |
| `/trust/flags` | suppression, overclaim, breach events from `AuditSink` |
| `/finance/summary` | revenue metrics router + payment follow-up queue |
| `/distribution/summary` | channel + sector + experiment counters |

Definition of done: every page renders non-zero, real numbers when the
backing data is present.

## Phase 3 — Controlled actions

Add POST endpoints to the internal router:

- `POST /api/v1/internal/founder/approvals/{id}/approve`
- `POST /api/v1/internal/founder/approvals/{id}/reject`
- `POST /api/v1/internal/founder/approvals/{id}/request-edit`
- `POST /api/v1/internal/founder/approvals/{id}/escalate`

Each action call must:

1. Resolve the approval class (`A0`/`A1`/`A2`/`A3`) for the requested
   action through `dealix/trust/PolicyEvaluator`
2. For `A2`/`A3`, require an explicit founder decision recorded by
   `ApprovalCenter`
3. Reject if any of: suppression list match, overclaim guard tripped,
   missing evidence, audit log unwritable
4. Return a decision receipt

No action endpoint may bypass the Trust Plane.

## Phase 4 — Trust enforcement and audit binding

Every action records to `dealix/trust/AuditSink` and
`ToolVerificationLedger`. Failed policy evaluations are surfaced on the
`/trust` page as live flags. The frontend gains an "Audit trail" drawer
that calls a new `GET /api/v1/internal/founder/audit/recent` endpoint.

## Phase 5 — Production gates

- SLO targets per endpoint (p95 latency, error rate)
- Alert routes wired to the existing observability stack
- Founder Console becomes the **single daily operating interface** for
  Dealix
- Documentation update: replace this plan with `docs/runtime/FOUNDER_CONSOLE_OPERATING_GUIDE.md`

## Rule

No external-impact button can bypass the Trust Plane. The frontend may
render a button, but the backend always re-validates approval class,
policy, suppression, evidence, and audit success before any side effect.
