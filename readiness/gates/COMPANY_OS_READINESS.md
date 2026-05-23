# Company OS Readiness Gate

> The hard gate: is the Dealix Company OS fit for the founder to operate on?
> Checked weekly during the Weekly CEO Review.

## The Gate

The Company OS is "ready" when **all** of the following are true:

### Structural (verified in CI)
- [ ] `scripts/verify_company_os.py` exits 0 (all 12 systems have their files)
- [ ] `scripts/verify_founder_os.py` exits 0
- [ ] `scripts/verify_revenue_os.py` exits 0
- [ ] `scripts/verify_delivery_os.py` exits 0
- [ ] `scripts/verify_trust_os.py` exits 0
- [ ] `scripts/verify_learning_os.py` exits 0
- [ ] `scripts/verify_public_safety.py` exits 0
- [ ] All Trust tests in `tests/trust/` pass

### Operating (founder attestation, weekly)
- [ ] Daily Brief read ≥ 5/7 weekdays this week
- [ ] Weekly CEO Review completed this Sunday
- [ ] Decision Log updated within 24 hr per decision
- [ ] Execution Ledger has ≥ 10 entries this week
- [ ] No A4 violations
- [ ] No new SEV-1 or SEV-2 incidents
- [ ] Approval queue cleared (no items > 48 hr waiting on founder)

### Strategic (founder attestation, weekly)
- [ ] At least 1 KILL decision logged this week (focus discipline)
- [ ] At least 1 entry under "What We Learned" in Monthly Strategy Update
- [ ] Focus Policy time allocation honored (≥ 70% on Sales + Delivery)
- [ ] Cash trajectory consistent with 90-day milestone

## What "Not Ready" Means

If any structural item is red:
- The PR / change is blocked in CI
- Founder fixes before merging

If any operating item is red for 2 weeks running:
- Pause non-essential new work
- Run a 1-hour Company OS diagnosis
- Identify the missing playbook, broken delegation, or skipped cadence
- Add a corrective rule to `DEALIX_DECISION_RULES.md`

If any strategic item is red for 2 weeks running:
- Escalate to Monthly Strategy Update
- Founder + advisor honest conversation
- Decide: pivot, persevere, or change the OS

## When To Stop Using This Gate

Never. Continuous use is the point. Even if every box has been green for months, run the gate weekly.

## Linked Scorecards

- `readiness/scorecards/FOUNDER_OS_SCORECARD.md`
- `readiness/scorecards/REVENUE_OS_SCORECARD.md`
- `readiness/scorecards/DELIVERY_OS_SCORECARD.md`
- `readiness/scorecards/TRUST_OS_SCORECARD.md`
- `readiness/scorecards/LEARNING_OS_SCORECARD.md`
