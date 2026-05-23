# Approval Matrix

> Companion to `docs/governance/APPROVAL_MATRIX.md` (canonical). This file
> is referenced by the Founder OS and Trust OS verifiers.

## Approval Levels

| Level | Meaning | Required Actor |
|---|---|---|
| A0 | No approval — agents may execute | n/a |
| A1 | Owner approval | System owner or sub-agent reviewer |
| A2 | Founder approval | Founder, recorded in `docs/founder/DECISION_LOG.md` |
| A3 | Founder + written rationale + risk acknowledgement | Founder + recorded mitigation |

## Action → Required Approval

| Action | Level | Notes |
|---|---|---|
| Lead scoring | A0 | Public information only |
| Internal report drafting | A0 | |
| Internal recommendation | A1 | |
| First outbound to a new prospect | A1 or A2 | A2 if message contains any claim about results |
| Sending a proposal | A2 | Must log to DECISION_LOG.md |
| Public claim / website edit | A2 | No-Overclaim Policy applies |
| Contract changes | A3 | |
| Refunds | A3 | |
| Pricing change (public) | A3 | |
| Regulatory or government contact | A3 | |
| Sharing client data externally | A3 | Even with consent, requires A3 |

## How to Request Approval

1. Open the relevant row in the approval queue (or `docs/founder/DAILY_COMMAND_BRIEF.md` Section 7).
2. State the action, the risk classification (per `WORKFLOW_RISK_CLASSIFICATION.md`), the proposed mitigation, and the rollback.
3. Founder records the decision in `docs/founder/DECISION_LOG.md`.

## Rule

No A2 / A3 action is executed without a DECISION_LOG entry. No exceptions.
