# Go / No-Go Decision System

> Founder uses this to decide quickly. Bias is **default no** until the audit
> says yes.

## The 3-light protocol

Every irreversible decision (sending external messages, charging customers,
signing contracts, committing infra changes) goes through 3 lights.

| Light | Meaning | Source |
|---|---|---|
| 🟢 GO | All preconditions met, action approved | audit + checklist passes |
| 🟡 HOLD | One or more preconditions unknown — pause + investigate | open ambiguity |
| 🔴 NO | A precondition is failing — refuse | failing audit / red-list rule |

## Decision template

Copy/paste into `founder/decision_queue.md`:

```
## Decision: <one-line description>

Date: <YYYY-MM-DD>
Reversibility: <minutes | hours | days | irreversible>
Cost if wrong: <SAR / brand / legal>

Preconditions:
- [ ] Audit green for <system>
- [ ] Approval evidence captured at <path>
- [ ] Customer-visible artefact reviewed
- [ ] Revert procedure written

Verdict: <GO | HOLD | NO>
Notes:
```

Verdict line is the only line that an automation reads. If the verdict is not
exactly `GO`, no automation may act.

## Default verdicts

| Situation | Verdict |
|---|---|
| Any audit FAILED in the last 24 hours | 🔴 NO |
| Audit green, no human approval logged | 🟡 HOLD |
| Audit green + human approval in `trust/approval_log.csv` | 🟢 GO |
| Spending > SAR 500 with no PO | 🟡 HOLD |
| Sending > 5 messages in 24h on the same channel | 🟡 HOLD |

## Daily founder loop

```
make daily
```

prints, in order:

1. **Today's 3** — three things to ship today, from `founder/decision_queue.md`.
2. **Approvals waiting** — from `founder/approvals_waiting.md`.
3. **Yesterday's revenue actions** — last 24h of `revenue/revenue_action_log.csv`.
4. **Open red flags** — failing verifiers from last audit run.

If `Today's 3` is empty, the founder writes 3 before doing anything else.
Empty Today's 3 = day not started.

## Weekly founder loop

```
make weekly-close
```

writes `weekly_reviews/<ISO_week>.md` from the template in
`docs/learning/LEARNING_LOOP.md`. Requires the founder to fill in:

- What was shipped (artefacts created/updated).
- What was sold (revenue actions logged).
- What was learned (one playbook update committed).
- Next week's stage target.

Then:

```
make advance
```

Advances the stage if and only if the exit checklist for the current stage is
green. Otherwise it prints the unchecked items and exits non-zero.

## What this system refuses to do

- Decide on the founder's behalf.
- Send anything externally.
- Override a 🔴 NO.
- Pretend a HOLD is a GO.

## Related

- `docs/trust/TRUST_COMMAND_CENTER.md` — green/red list of automated actions.
- `docs/learning/LEARNING_LOOP.md` — weekly review template.
- `DEALIX_STAGE_GATED_ROADMAP.md` — what stage we are at, what unlocks the next.
