# Email Draft Machine

| Field | Value |
|---|---|
| Purpose | Maintain sequenced email cadences for engaged accounts |
| Inputs | account scores, reply history, suppression list |
| Outputs | Sequenced rows in `outreach_queue.csv` (cadence_step ≥ 2) |
| Approval class | Per-step founder approval |
| Trust gate | Brand check, suppression, sequence cap (max 4 steps) |
| Owner | Distribution Operator |
| KPI | Reply rate per step, opt-out rate, cash-per-cadence |
| Failure mode | Opt-out detected → cadence halts, suppression list updated |

## Cadence policy

- Max 4 touches per account in any 90-day window.
- Minimum 4 business days between steps.
- Cadence resets on any human reply.
- Cadence halts on any opt-out or negative reply.
- Cadence halts immediately if suppression status changes.

## Brand notes

- Step 1: insight; cite a trigger event or a sector pattern.
- Step 2: relevance; map the insight to the persona.
- Step 3: offer; the right rung of the offer ladder.
- Step 4: graceful close; offer to keep updates flowing through nurture.

## Forbidden

- Adding non-Dealix tracking pixels.
- Sending more than one step per business day per account.
- Using urgency / scarcity language.
