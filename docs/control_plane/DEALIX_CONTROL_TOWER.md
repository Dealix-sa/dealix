# Dealix Control Tower

## Purpose
The control tower is the single brief the founder reads in the morning to know:
- What is on fire.
- What is paying or about to pay.
- What is blocked and why.
- What the one next action is.

## Inputs
- `dealix-ops-private/pipeline/pipeline_tracker.csv`
- `dealix-ops-private/revenue/revenue_action_log.csv`
- `dealix-ops-private/sales/proposal_tracker.csv`
- `dealix-ops-private/revenue/cash_collected.csv`
- `dealix-ops-private/trust/approval_log.csv`
- `dealix-ops-private/evidence/execution_evidence_ledger.csv`

## Output
- `dealix-ops-private/founder/control_tower_brief.md` (refreshed by `make control-tower`).

## Brief format
1. **Money**: cash this week, weighted pipeline, MRR.
2. **Risks**: open SEV-2+ incidents, pending approvals, stale data sources.
3. **Top action**: the single most important thing the founder must do today.
4. **One bet**: the bet for the week.
5. **Constraints**: anything blocking the top action.

## Refresh cadence
- Daily, every morning before any other work.
- Re-run if any input changes during the day.

## Use rules
- The control tower brief is read-only. To change priorities, edit the inputs and regenerate.
- Do not duplicate the brief into multiple places.
- If two priorities tie, the priority router decides.

## Anti-patterns
- Reading 12 dashboards in the morning.
- Ignoring the brief because it disagrees with intuition.
- Treating the brief as a feed instead of a directive.
