# Build · Defer · Kill (Product Edition)

> Product-specific application of `KILL_DEFER_BUILD_RULES.md`.
> Use during weekly product triage.

## Quick Reference

| Question | Build | Defer | Kill |
|---|---|---|---|
| Serves Sprint/Retainer/Trust/Proof/Leverage? | ≥ 1 | none with revisit | none + dead |
| Size? | XS / S / M | L (need WCR approval) | XL (forbidden) |
| Reversibility? | ≤ 1 day rollback | days | weeks+ |
| Customer count asking? | 1+ active | 0 currently | 0 + 90+ days |
| Trust-gate impact? | strengthens or neutral | requires more analysis | weakens |

## Build Conditions (all must be true)

- Passes Strategy Filter (cite which test #)
- Fits Focus Policy time allocation
- Has measurable success metric
- Has defined kill switch
- Has owner (founder unless explicit hire)
- Sized XS to M (L only with WCR approval)
- Doesn't violate Veto Rules

## Defer Conditions (any one)

- Strategy Filter fails today but might pass later
- Waiting on evidence from another experiment
- Resource-constrained this quarter
- Customer demand not yet validated
- Requires irreversible commitment we're not ready for

Every defer = revisit date. Default windows:
- Product idea: 30 days
- Tech debt cleanup: 60 days
- New offer: 30 days
- Integration: 60 days

## Kill Conditions (any one)

- No customer interaction in 30 days
- Consumed > 8 founder hours without logged outcome
- Conflicts with quarter focus
- Success metric never defined and still isn't
- Duplicates an existing capability
- Trust audit fail with no clean fix
- Customer requesting it has churned / opted out

## Build Process

1. Open PR with title `[BUILD] {feature}` referencing intake row
2. Link to: strategy filter test passed, success metric, kill switch, intake ID
3. Required reviews: founder (always); advisor if Trust-touching
4. Add row to `DEALIX_EXECUTION_LEDGER.md` on merge
5. Add tests (especially Trust tests if applicable)
6. Update related docs in `docs/product/`

## Defer Process

1. Update intake row to status `deferred`
2. Set revisit date
3. Note one-line reason
4. Calendar reminder for revisit date

## Kill Process

1. Update intake row to status `killed`
2. Note one-line reason + one-line learning
3. Remove related code (don't leave dead code)
4. Update related docs
5. Notify any customer who asked for it (if applicable)
6. Add to `learning/EXPERIMENT_LOG.md` if it was an experiment

## Decision Pattern Examples

| Request | Decision | Why |
|---|---|---|
| "Build a Slack integration" | DEFER 60 days | No customer asked; not in Sprint; revisit when 3+ ask |
| "Add a payment retry loop" | BUILD S | Trust + Finance OS pass; serves Retainer |
| "Refactor old `auto_client_acquisition/` to FastAPI" | KILL | Wrong layer; doesn't serve Focus this quarter |
| "Build a mobile app" | KILL | Wrong format for buyer; XL effort; violates Focus |
| "Add a custom approval matrix per client" | BUILD M | Required for Revenue Desk tier; trust-strengthening |
| "Build founder Daily Brief generator" | BUILD M | Founder leverage (#5); already in intake INT-002 |

## Anti-Patterns

- "Almost done, let's finish" — sunk cost is not a build reason
- "It would look bad to kill publicly" — kill privately, learn publicly
- "Just one more feature" — that's exactly the trap
- "We'll need this eventually" — that's defer, not build

## Review Cadence

- Weekly: triage all intake rows
- Monthly: review deferred backlog
- Quarterly: kill anything stale + write learning

## What This Refuses

- Building without explicit decision
- Decisions without strategy-filter alignment
- Indefinite defers
- Quiet kills (no learning logged)
