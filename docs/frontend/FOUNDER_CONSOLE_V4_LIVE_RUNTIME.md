# Founder Console v4 — Live Runtime

## Purpose
Move Founder Console from buildable UI to live founder operating interface.

## v4 Goals
1. Read real runtime data.
2. Show source freshness.
3. Write approval audit records.
4. Block external-impact actions without Trust.
5. Surface one CEO top action.
6. Certify production readiness.

## Required Live Pages

### /ceo
Reads:
- sales funnel
- approval queue
- trust flags
- finance summary
- worker health

Outputs:
- top CEO action
- company status
- bottleneck

### /sales-cockpit
Reads:
- lead_intelligence_base
- outreach_queue
- conversation_log
- sample_queue
- proposal_queue
- payment_capture_queue

Outputs:
- funnel metrics
- bottleneck

### /approvals
Reads:
- approval_queue

Writes:
- approval_decisions audit log

Outputs:
- approved / rejected / needs edit

## Production Rule
No page is considered live unless it reads from a real source of truth and shows freshness timestamp.

## Trust Rule
Frontend requests actions.
Trust approves or blocks actions.
Audit records every decision.
