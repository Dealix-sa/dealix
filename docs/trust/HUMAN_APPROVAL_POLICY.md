# Human Approval Policy

## Why Humans Approve

AI agents draft, score, and prepare. Humans approve anything that is
client-visible, hard to reverse, or carries trust or legal risk. Approval
is not bureaucracy — it is the trust gate that lets us automate the rest.

## Who Approves What

| Approval Level | Approver | Recorded In |
|---|---|---|
| A0 | n/a | Workflow logs |
| A1 | System owner / sub-agent reviewer | System's own ledger |
| A2 | Founder | `docs/founder/DECISION_LOG.md` |
| A3 | Founder + written rationale | `docs/founder/DECISION_LOG.md` + `RISK_REGISTER.md` |

## Standard Approval SLA

- A1 — same business day.
- A2 — within 24 hours.
- A3 — within 48 hours; founder may pause the underlying workflow.

## What Approval Looks Like

Approval is explicit, recorded, and references the artifact under review.
A "thumbs-up" without a DECISION_LOG entry does not count.

Approval form:
```
DECISION: Approve / Reject
ACTION: <what is being approved>
ARTIFACT: <path or URL to the proposal / draft / claim>
RISK: <Low / Medium / High / Critical>
REASON: <one sentence>
ROLLBACK: <one sentence, if applicable>
```

## Time Pressure

If the founder is unreachable and the action is A2/A3, the action waits.
We do not let urgency override the Trust gate.

## Audit

The approval log is reviewed weekly in the CEO Review and quarterly in the
Trust review. Any A2/A3 action executed without a DECISION_LOG entry is
treated as a Trust incident.
