# Dealix Company OS — Missing Systems (Follow-up PRs)

Per the approved plan, this session was **scoped to founder-essential
six pages first** and **infra-only addition** (no Article 13 violation).
The remaining systems from the original 26-layer request live here as
explicit follow-up items, each gated on a clear unlock condition.

## Frontend routes not yet built (16 of 22)

These are tracked but **not** scaffolded in this session. Each remains
behind the same `INTERNAL_API_URL` + bearer pattern when built.

| Route | Unlock condition |
|---|---|
| `/ceo-os` | After 30 days of `ceo_daily_brief.md` history collected |
| `/founder-leverage` | After `founder_time_audit.csv` has ≥ 30 rows |
| `/strategy` | After `strategic_assumptions.csv` has ≥ 5 tested rows |
| `/sales-cockpit` | After Article 13 Phase G (3 paid pilots) |
| `/deal-desk` | After Phase G |
| `/approvals` (founder view) | Already exists at `/approvals`; consolidate when next pass |
| `/workers` | When worker_state.csv shows ≥ 3 distinct workers |
| `/launch` | After first paid-pilot Proof Pack is approved |
| `/revenue-intelligence` | After Phase G |
| `/productization` | After 3 paid pilots in the same sector |
| `/enterprise-sales` | After 6 months of retainer history |
| `/legal` | Index-only doc page; build when `docs/legal/` populated |
| `/security` | Index-only doc page; build when `docs/security/INDEX.md` lands |
| `/metrics` | Already exists in `revenue_metrics`; map when consolidated |

## Verifiers not yet built

| Verifier | Notes |
|---|---|
| `verify_revenue_factory.py` | Defer until Phase G; revenue surface is gated. |
| `verify_hypergrowth_ceo_layer.py` | Defer; covered functionally by `verify_founder_ceo_hypergrowth_layer.py` for now. |
| `verify_company_memory.py` | Defer; the existing `learnings.csv` is sufficient seed. |

## Doctrine items intentionally NOT changed

- The 11 non-negotiables — frozen by Doctrine Lock; any change needs
  RFC + 5-OS-owner review (CLAUDE.md documents this).
- Article 13 Build Order — frozen until 3 paid pilots collected.
- The 5-Rung Service Ladder pricing — frozen by approval policy.

## Infrastructure items requiring manual GitHub UI action

These cannot be configured via `.github/` files:

1. Mark `dealix-everything` as a required check on `main`.
2. Mark `dealix-company-os` as informational (daily artifact only).
3. Confirm CODEOWNERS for the new directories (`policies/`,
   `registries/`, `evals/gates/`, `api/internal/`, `api/routers/internal/`,
   `apps/web/{lib,components,app/ceo,app/capital-allocation,...}`).

## When to revisit this list

After the first 3 paid pilots and at least 30 days of private-ops
runtime data, open a `feat/dealix-company-os-phase-2` branch and pull
the next batch of routes + verifiers from this list. Do **not** ship
them ahead of the unlock conditions — the verifiers (and the doctrine)
will reject them.
