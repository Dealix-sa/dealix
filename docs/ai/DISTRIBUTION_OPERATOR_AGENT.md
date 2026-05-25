# Distribution Operator Agent

Agent ID: `distribution_operator`
Worker name: `distribution_operator_worker`
Owner: Founder + Sales Operator

## 1. Purpose

The Distribution Operator coordinates the **15 distribution machines** (see `AUTONOMOUS_DISTRIBUTION_MACHINES.md`) — sequencing them, balancing approval queue load, and surfacing the right machine output at the right time for founder review.

The Operator is **conductor, not soloist**. It does not generate content; it orchestrates the machines that do.

## 2. Inputs

- Status of all 15 distribution machines.
- Approval queue size and age.
- Founder's available review budget (configurable; default 30 minutes/day).
- Sector calendar and active strategic accounts.

## 3. Outputs

- A **daily distribution plan**: which machine runs, with what input, producing what artefact.
- A **weekly distribution report**: machine-by-machine KPI roll-up, queue health, founder review load.
- A **per-machine recommendation**: continue / throttle / pause.

## 4. Approval class

**A2.** Some Operator decisions (e.g. throttling a machine) require founder approval; others (e.g. reordering the queue within doctrine bounds) are A1.

## 5. Doctrine

- The Operator cannot send anything externally.
- The Operator cannot enable a new machine — the founder authorises machines individually.
- The Operator cannot bypass the brand verifier or trust gates.

## 6. Failure modes

| Failure                                  | Recovery                                          |
|------------------------------------------|---------------------------------------------------|
| Queue size exceeds founder review budget | Throttle low-priority machines; recommend pause   |
| Approval queue age > SLA (24h)           | Surface to founder dashboard                      |
| Two machines produce duplicate drafts    | Suppress; log                                     |
| A machine fails 3 consecutive runs       | Auto-pause; escalate to founder                   |

## 7. Audit

Daily plan and weekly report are logged in `data/growth/distribution_reports/` (private mirror). Founder signs off the weekly report.

## 8. Registration

Registered in the agent registry with:

- `agent_id = distribution_operator`
- `approval_class_max = A2`
- `eval_required = true`
- `kill_switch = true`
- `audit_required = true`
- `external_send = false`
