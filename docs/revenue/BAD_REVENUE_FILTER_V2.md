# Bad Revenue Filter V2

## Purpose
Reject revenue that costs more than it earns — financially, reputationally, or morally.

## Filter rules
A deal is **bad revenue** if any of these is true:

1. **Sector mismatch**: anti-ICP per `docs/strategy/ICP_OPERATING_SYSTEM.md`.
2. **Scope unbounded**: buyer refuses to define done.
3. **Hostile buyer**: tone signals contempt or unreasonable demands during sales.
4. **Margin negative**: list price minus expected effort cost < 0.
5. **Trust risk**: requested deliverable would violate proof, privacy, or doctrine rules.
6. **Capacity overrun**: would put existing customers at delivery risk.
7. **Strategic conflict**: would lock us out of a Primary ICP segment.

## Operating procedure
1. Score the lead before quoting.
2. Run this filter before sending a proposal.
3. If any rule triggers, document the decision in `pipeline/win_loss_log.md` as `Closed-lost: bad revenue`.
4. Communicate politely with the buyer: decline, offer a different path if relevant.

## Borderline cases
- Use the trust workflow to make the call.
- A written second opinion from a trusted advisor counts.

## Override
- The founder may override the filter for strategic value (e.g., a marquee logo).
- Overrides must be recorded in `trust/approval_log.csv` with explicit reasoning.

## Why this exists
Early-stage companies die from saying yes more often than from saying no. The filter is here to make "no" the default in ambiguous cases.
