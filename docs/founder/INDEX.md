# Founder Hub — INDEX

The Founder/CEO Operating Layer that runs on top of Dealix's existing
operational stack. This directory holds the **rhythm, leverage, and decision**
discipline. Day-to-day commercial execution still lives in `docs/commercial/`,
`docs/sales/`, and `docs/ops/`.

## Read in this order

1. [CEO_OPERATING_SYSTEM](CEO_OPERATING_SYSTEM.md) — the rhythm (day / week / month / quarter)
2. [CEO_DAILY_BRIEF_SYSTEM](CEO_DAILY_BRIEF_SYSTEM.md) — what to look at every morning
3. [CEO_WEEKLY_REVIEW](CEO_WEEKLY_REVIEW.md) — the Friday review template
4. [DECISION_LOG_SYSTEM](DECISION_LOG_SYSTEM.md) — append-only decision capture
5. [STRATEGIC_ASSUMPTIONS_REGISTER](STRATEGIC_ASSUMPTIONS_REGISTER.md) — falsifiable bets with kill-triggers
6. [FOUNDER_LEVERAGE_DASHBOARD](FOUNDER_LEVERAGE_DASHBOARD.md) — Make / Manage / Move time ratio
7. [FOUNDER_TIME_AUDIT](FOUNDER_TIME_AUDIT.md) — weekly time-allocation rubric
8. [DELEGATION_DECISION_TREE](DELEGATION_DECISION_TREE.md) — keep / coach / delegate / automate / hire
9. [CEO_ATTENTION_BUDGET](CEO_ATTENTION_BUDGET.md) — weekly attention envelope
10. [DO_NOT_SAY](DO_NOT_SAY.md) — the doctrine

## Where the data lives

| Class | Location | Reason |
|---|---|---|
| Sensitive (decisions, capital, assumptions, advisor updates, time audit) | `$DEALIX_OPS_PRIVATE/ceo/*` (default `/opt/dealix-ops-private`; macOS dev `~/.dealix-ops-private`) | Out of the repo by design |
| Evidence (pipeline, payments, friction) | `docs/ops/`, `docs/commercial/operations/` | Already in repo; not personally sensitive |
| Generated briefs | `data/founder_briefs/*` | Build artefacts, gitignored |

Use `make bootstrap-runtime` to lay down the PRIVATE_OPS skeleton. When the
env var is not set the bootstrap is a non-fatal no-op.

## Cross-references to existing systems

- [`docs/board_decision_system/`](../board_decision_system/) — board-level decision governance (separate forum; this hub is for solo CEO)
- [`docs/company/FOUNDER_COMMAND_CENTER.md`](../company/FOUNDER_COMMAND_CENTER.md) — historical command-center reference
- [`docs/ops/FOUNDER_OPERATING_SYSTEM_AR.md`](../ops/FOUNDER_OPERATING_SYSTEM_AR.md) — original Arabic founder OS
- [`dealix/execution_assurance/registry.yaml`](../../dealix/execution_assurance/registry.yaml) — authoritative source of CEO weekly review questions, scorecard rubric, and KPI targets

## How this layer is enforced

- Doctrine: [DO_NOT_SAY](DO_NOT_SAY.md)
- Lint: [`tests/test_no_founder_layer_promises.py`](../../tests/test_no_founder_layer_promises.py)
- Verifier: [`scripts/verify_founder_ceo_hypergrowth_layer.py`](../../scripts/verify_founder_ceo_hypergrowth_layer.py)
- CI: [`.github/workflows/founder_ceo_hypergrowth.yml`](../../.github/workflows/founder_ceo_hypergrowth.yml)

## Non-negotiables

This layer never sends external messages, never publishes proof without
ledger evidence, never commits to payment terms, and never carries customer
funds. See [`docs/00_constitution/NON_NEGOTIABLES.md`](../00_constitution/NON_NEGOTIABLES.md).
