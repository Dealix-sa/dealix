# Worker Queue Runtime v2

## Relationship to existing docs
Builds on the technology decisions in `dealix/registers/technology_radar.yaml`:
- Redis 7 — **ADOPT** for cache, rate-limits, and queues.
- Temporal — **TRIAL (Phase 2)** for long-running durable workflows; gated on a single critical-path spike before broader adoption.
- In-process pipeline — **ADOPT** for current single-process workloads.

## Purpose
Run Dealix background machines reliably on the server.

## Phase 1 — Cron
Use for:
- daily reports
- scoring
- approval queue generation
- follow-up queue generation

Cron file: `deploy/cron/dealix_growth_factory.cron`. Phase 1 lines: `make sales-cockpit` and `make approval-center`.

## Phase 2 — Redis Queue
Use for:
- lead enrichment jobs
- outreach draft generation
- reply routing
- sample generation

## Phase 3 — Durable Workflow
Use for:
- proposal to payment flow
- delivery lifecycle
- approval retries
- client onboarding

## Queue Names
- market.discovery
- lead.enrichment
- lead.scoring
- outreach.draft
- approval.build
- followup.schedule
- reply.route
- sample.create
- proposal.create
- payment.capture
- delivery.trigger
- retention.manage
- proof.content
- ceo.report

## Rule
External commitments require approval checkpoint. Any queue worker that produces an external-facing artifact must terminate at an approval gate in `dealix/trust/approval.py` before any subsequent send-step is enqueued.
