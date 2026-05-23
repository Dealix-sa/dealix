# DEALIX DECISION RULES

> The rules the company uses to say YES, NO, LATER, KILL.
> If a rule here conflicts with a feature request, the rule wins.

## Decision Types

Every decision the company makes is one of seven:

- **BUILD** — start work on something new
- **FIX** — repair something that is broken
- **KILL** — stop something we already started
- **DEFER** — not now, revisit by a named date
- **APPROVE** — let an action through trust gate
- **REJECT** — block an action at trust gate
- **ESCALATE** — founder must decide personally

Every decision must be logged in `DEALIX_EXECUTION_LEDGER.md` **and** in `founder/decision_log.md` (private repo).

## The Strategy Filter (used by BUILD / DEFER)

Any proposed new work must pass at least one of these tests:
1. Does it directly serve **Revenue Sprint** delivery?
2. Does it directly serve **Retainer** conversion?
3. Does it directly serve **Trust** (reduce a real risk)?
4. Does it directly serve **Proof** (create a defensible case study or evidence)?
5. Does it directly serve **Founder leverage** (eliminate ≥ 1 hour/week of founder work)?

If the answer to all five is "no", the decision is **DEFER**. No exceptions.

## The Approval Matrix (used by APPROVE / REJECT)

| Action class | Default | Founder required? |
|---|---|---|
| Internal lead scoring | auto | no |
| Lead enrichment | auto | no |
| Message draft generation | auto | no |
| Sending first outreach DM | manual | yes |
| Sending proposal | manual | yes |
| Pricing change | manual | yes |
| Public claim (LinkedIn, case study, web) | manual | yes |
| Sending invoice | manual | yes |
| Refund / credit | manual | yes |
| Contract change | prohibited from automation | yes |
| Compliance / regulated claim | prohibited from automation | yes |

This matrix is enforced in code by `dealix/trust/approval_matrix.py`.

## The Kill Rules (used by KILL)

Kill any workstream that:
- Has not produced a logged customer interaction in 30 days
- Has consumed > 8 founder hours without producing a logged outcome
- Conflicts with a higher-priority Strategy Filter pass
- Requires automating an L4 (prohibited) action

When you kill something, log:
- date
- what was killed
- why (one sentence)
- what we learned (one sentence)
- what we redirected the time/capital to

## The Defer Rules (used by DEFER)

Every DEFER must include a **revisit date**. If a deferred item has no revisit date, it is implicitly KILLED.

Default revisit windows:
- Product idea → 30 days
- Hire → 60 days
- Geo expansion → 90 days
- New offer → 30 days

## The Escalate Rules (used by ESCALATE)

Escalate to the founder if:
- The action touches money > 5,000 SAR
- The action touches a regulated claim
- The action involves a contract change
- The action would conflict with the Strategy Filter
- The action would set a precedent for future automated behavior
- An agent or human is unsure (uncertainty itself is a signal)

## The Veto Rules (override everything)

These rules cannot be overridden, ever:
1. No client data leaves the private repo
2. No automated send to suppression-list contacts
3. No public compliance claim without a logged evidence pack
4. No auto-execution of an A3-prohibited action
5. No commit that fails the trust test suite
6. No PR merge without status checks green

## Conflict Resolution

If two rules conflict:
- Veto rule beats everything
- Trust rule beats efficiency rule
- Founder decision (logged) beats agent decision
- More-recent rule beats older rule (and the older rule must be marked superseded in this file)

## How To Change A Rule

1. Open a PR titled `RULE: <change description>`
2. Cite the data or incident that motivated the change
3. Founder approval required
4. Update this file + bump the changelog at the bottom
5. Update affected verification scripts in `scripts/verify_*.py`

## Changelog

- 2026-05-23 — Initial rules locked. Founder Command OS bootstrapped.
