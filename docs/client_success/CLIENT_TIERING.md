# Client Tiering

> Not all clients are equal. Treat them differently.

## The Four Tiers

### A — Strategic
- High health score (80+).
- Retainer at or above 10K SAR / month.
- Public case study consent given or in progress.
- Source of referrals.
- Founder personally owns the relationship.

**Treatment:** monthly executive review; founder direct line; advance
notice of any change in price or scope.

### B — Standard
- Health score 60–79.
- Retainer in range.
- Healthy, predictable, no friction.

**Treatment:** standard weekly report; monthly check-in.

### C — Watch
- Health score 40–59.
- Renewal at risk.
- Friction visible in feedback or behaviour.

**Treatment:** named intervention plan within 7 days; founder reviews
weekly until score recovers or contract ends.

### D — Reject / Refer
- Pre-contract: filter out per `BAD_REVENUE_FILTER.md`.
- Post-contract: contract sees out its term; not renewed; named alternative offered.

**Treatment:** professional, polite, finite.

## How a client moves between tiers

- A→B: drop in health score for 2 consecutive months.
- B→A: 3 consecutive months at score ≥ 80 + retainer ≥ 10K SAR.
- B→C: health score < 60 for 1 month.
- C→D: health score < 40 + no recovery within 30 days.
- D→C: only by re-scoping (see `RETENTION_PLAYBOOK.md`).

## What we do **not** do

- Demote a client without naming the trigger.
- Promote a client without evidence.
- Treat tier as a permanent attribute of the company.

## Linked Sources

- `dealix-ops-private/client_success/tiers.csv` — current tier per client.
- `dealix-ops-private/client_success/health_scores.csv` — monthly scores.
