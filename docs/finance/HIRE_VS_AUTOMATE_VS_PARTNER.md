# Hire vs Automate vs Partner — Decision Matrix

A three-way comparison run any time
[`docs/founder/DELEGATION_DECISION_TREE.md`](../founder/DELEGATION_DECISION_TREE.md)
lands on questions 4 or 5.

## The matrix

| Dimension | Hire (contractor / FTE) | Automate (agent / tool) | Partner |
|---|---|---|---|
| Cost (90-day) | Highest | Medium up-front, low ongoing | Variable, often deferred |
| Speed to first output | Days–weeks | Hours–days (if pattern known) | Weeks (relationship setup) |
| Quality variance | Person-dependent | Deterministic, eval-gated | Partner-dependent |
| Reversibility | Easy for contractor, painful for FTE | Easy (turn off) | Moderate (contract terms) |
| Leverage on CEO time | Medium (still manage) | High (set and check) | High (set and check) |
| Trust risk | Personnel risk | Eval-gated; risk is misuse | Brand risk if partner overpromises |

## When each wins

- **Automate** — repeatable, well-bounded, eval-gateable, volume justifies the build time. Pattern: anything in [`docs/00_constitution/NON_NEGOTIABLES.md`](../00_constitution/NON_NEGOTIABLES.md) that requires human approval is still gated.
- **Hire** — judgment-heavy, customer-facing, evolving work where coaching builds long-term capability
- **Partner** — capability we will never own and customers expect bundled (e.g., specific compliance audits, regulated payment rails)

## Log

Every call is appended to PRIVATE_OPS `ceo/hire_vs_automate_log.csv` via
the existing decision-log mechanism. Columns:

| Column | Notes |
|---|---|
| `date` | ISO |
| `decision` | one of: hire, automate, partner |
| `role_or_function` | what is being delegated |
| `reasoning` | one sentence |
| `outcome` | filled in 90 days later — kept, reversed, expanded |

## Cross-references

- [`docs/founder/DELEGATION_DECISION_TREE.md`](../founder/DELEGATION_DECISION_TREE.md)
- [`docs/people/HIRING_TRIGGER_SYSTEM.md`](../people/HIRING_TRIGGER_SYSTEM.md)
- [ROI_PRIORITY_MATRIX](ROI_PRIORITY_MATRIX.md)
- [`docs/people/DELEGATION_SYSTEM.md`](../people/DELEGATION_SYSTEM.md)

## Non-negotiables

Automation paths must keep human approval where the existing trust system
requires it (e.g., outbound, payments, proof publishing). See
[`docs/founder/DO_NOT_SAY.md`](../founder/DO_NOT_SAY.md).
