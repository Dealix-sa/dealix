# Dealix Self-Operating Company OS — Execution Order

This document defines the practical merge and operating sequence for the self-operating company layer.

## Current order

1. **#872 — Production Smoke API key alignment**
   - Clear protected route smoke blocker.
   - Do not weaken auth.
   - Fresh CI required before merge.

2. **#858 — Railway production foundation**
   - Keep Dockerfile `/app/start.sh` as canonical runtime.
   - Prevent config drift.
   - Fresh CI or maintainer confirmation required before merge.

3. **#873 — First Paid Client Sprint**
   - Close first 499 SAR deal manually.
   - Payment evidence required before revenue.
   - Proof pack required before closed-won.

4. **#871 — Client Acquisition Queue**
   - Ranked founder-review queue.
   - No external sends.

5. **#874 — Grand Targeting Automation OS**
   - Safe source intake.
   - TargetCard scoring.
   - Offer matching.
   - Approval queue.
   - Learning loop.

6. **This PR — Self-Operating Company OS**
   - Daily company operating cycle.
   - Internal execution queue.
   - Approval queue.
   - Content queue.
   - Proof log.

7. **#869 — Autonomous OS**
   - Use the outputs from targeting and company OS.
   - Keep all irreversible actions behind approval.

8. **#849 then #850**
   - Founder CLIs, commercial readiness, product/pricing unification.
   - Merge only after trust and close path are clear.

## Daily operating cycle

```txt
read production status
-> read commercial queue
-> score targets
-> match offers
-> draft actions
-> route external actions to approval
-> create proof log
-> create content queue
-> report today’s execution plan
```

## Autonomy levels

| Level | Allowed |
|---|---|
| 0 Observe | Read and summarize only |
| 1 Analyze | Prioritize and score |
| 2 Draft | Generate messages, offers, reports |
| 3 Internal execute | Write reports, queues, proof logs |
| 4 Repo execute | Open branches/PRs and tests after review |
| 5 External execute | Sending, publishing, charging, merging, production changes — blocked unless separate controlled-live approval exists |

## Commercial KPI ladder

1. First approved target.
2. First approved draft.
3. First manual offer sent.
4. First invoice/payment instruction sent.
5. First payment received.
6. First proof pack delivered.
7. First retainer upsell.

## Safety invariants

- Draft-only by default.
- Founder approval for all external actions.
- No fake proof.
- No guaranteed claims.
- No cold WhatsApp.
- No mass LinkedIn.
- No revenue before payment evidence.
- No closed-won before proof pack delivery.
