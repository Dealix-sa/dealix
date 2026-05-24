# Dealix — Missing Systems (Punch List)

This is the honest list of surfaces from the AI Company OS spec that
are NOT yet implemented after the Production Certification Layer was
built. They show up as WARN in `make production-certification`, not
FAIL, so the gate is green while the punch list closes.

## Founder Console pages still to scaffold

Under `apps/web/app/<slug>/page.tsx`:

- `ceo/` — CEO landing view (today/this week)
- `ceo-os/` — operating system map
- `founder-leverage/` — highest-leverage suggestions
- `capital-allocation/` — read of finance/capital_allocation.csv
- `strategy/` — strategic scorecard
- `sales-cockpit/` — pipeline + activity
- `deal-desk/` — per-deal view
- `market-attack/` — beachhead scorecard
- `moat/` — data moat status
- `revenue-intelligence/` — RI summaries
- `ai-governance/` — agent registry + risk register
- `trust/` — approvals + incidents
- `workers/` — machine registry status
- `finance/` — revenue + cash
- `customer-success/` — health, expansion, referrals
- `company-memory/` — decisions, learnings
- `legal/` — commercial guardrails
- `audit/` — audit log viewer
- `metrics/` — hypergrowth metrics

Each should be a server component that calls
`/api/v1/internal/...` with the internal token (server-side only,
never exposed to the browser as `NEXT_PUBLIC_*`).

## Internal API endpoints to expose

`api/routers/internal/founder_console.py` ships with four:
`/ceo/summary`, `/approvals/queue`, `/finance/forecast`,
`/trust/incidents`. The remaining surfaces from the punch list above
each need a corresponding `runtime_reader` view + a router endpoint.

## Daily/weekly machines wired into a scheduler

`registries/machine_registry.yaml` declares them; the scripts exist
(`generate_*.py`). Wire them via GitHub Actions cron or Railway cron,
one workflow per machine, with `DEALIX_PRIVATE_OPS` pointing at the
volume.

## Eval suites that actually run

`evals/gates/dealix_agent_eval_gate.yaml` references cases files but
nothing runs them yet. Build `scripts/run_agent_evals.py` to execute
each suite and compare to the thresholds. Until that exists, the eval
gate verifier only checks declarations, not outcomes.

## Brand / DS components

Spec mentions `apps/web/components/brand/*` and `lib/dealix-runtime.ts`.
Not built. Recommendation: postpone until the punch list above is
half-closed; brand polish on empty pages is wasted effort.

## What's intentionally NOT going to be built

- Cold WhatsApp / LinkedIn automation. Forbidden by `dealix-sales`
  doctrine and the policy. Don't add it.
- Frontend that talks to GreenAPI / Moyasar / SMTP directly. Forbidden
  by `verify_live_send_safety.py`.
- Auto-A3. Forbidden by `no_a3_auto`.
