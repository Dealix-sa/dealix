# CEO Decision Queue (Template)

> Copy this file into the **private founder repo** as
> `founder/decision_queue.md`. This public template defines the shape
> only — do not put real customer or pipeline data here.

The rule:

> Any decision without **Evidence** does not enter the CEO Decision
> Queue. This prevents emotional decisions.

## Template

| Priority | Decision | Type | Risk | Evidence | Recommendation | CEO Decision |
|---:|---|---|---:|---|---|---|
| 1 | Fix payment fallback | FIX | High | checkout blocked | Use manual invoice now | Pending |
| 2 | Approve proposal for X | APPROVE | Medium | qualified call | Send Growth Sprint | Pending |
| 3 | Defer dashboard animation | DEFER | Low | no revenue link | Delay 30 days | Pending |

## Type Values
- `FIX`     -- something is broken or blocking revenue/delivery/trust
- `APPROVE` -- requires explicit founder approval (Action Router APPROVE path)
- `DEFER`   -- not now, time-boxed defer
- `KILL`    -- stop entirely (links to `KILL_LIST.md`)
- `INVEST`  -- allocate capital (time, cash, engineering)

## Risk Levels
- High   -- revenue, trust, legal, customer-visible
- Medium -- delivery or pipeline quality
- Low    -- internal, reversible
