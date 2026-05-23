# نظام جودة القرارات — Decision Quality System

> How to write a decision. Reversibility, evidence, owner, deadline.

## Purpose
Improve the average quality of every decision the founder logs. Make decisions inspectable, comparable, and learnable from.

## Owner
Founder/CEO.

## Inputs
- The decision itself (problem + options).
- Evidence available (artifacts in repo).
- Time and cash cost of each option.

## Outputs
- Decision file at `docs/founder/decisions/YYYY-MM-DD_<slug>.md`.
- Index entry in `docs/founder/decisions/INDEX.md`.

## Rules
1. Every decision has: owner, class, deadline, success criteria, kill criteria.
2. Reversible decisions are made fast (< 1 hour write-up). Irreversible decisions go through `GO_NO_GO_DECISION_SYSTEM.md`.
3. Evidence is linked, not summarized. The reader can click through.
4. Options considered: at least two, including the "do nothing" baseline.
5. The decision is written before the action — backfilling is forbidden.
6. Re-decisions reference the prior file; they do not overwrite it.

## Metrics
- Decisions logged per month: ≥ 8.
- Decisions with all six fields filled: 100%.
- Decisions reviewed at 90-day mark: ≥ 70% (closing the loop).
- Decision reversal rate within 90 days: ≤ 15%.

## Cadence
Per-decision. Quarterly sweep to score reversals and learnings.

## Evidence
`docs/founder/decisions/` and `INDEX.md`.

## Verifier
`make decision-quality-verify` — checks every decision file has all six fields and an index entry.

## Runtime Command
`make decide slug=<slug>`

---

## Decision file template

```
# Decision: <slug>
Date: YYYY-MM-DD
Class: A1 / A2 / A3
Owner: <name>
Deadline: YYYY-MM-DD

## Problem
<one paragraph — the question we are answering>

## Options
1. <option> — cost: <SAR or hours> — reversibility: <yes/no>
2. <option> — ...
3. Do nothing — cost: 0 — consequence: <text>

## Evidence
- <link>
- <link>

## Pre-mortem
"If this is wrong, we will see <signal> by <date>."

## Decision
<chosen option, one sentence>

## Success criteria (measurable, dated)
1.
2.

## Kill criteria (measurable, dated)
1.

## Review date
<90 days from today>: <YYYY-MM-DD>

## Review outcome (filled at review date)
[ ] Succeeded — why
[ ] Failed — why
[ ] Mixed — why
[ ] Killed — when, why
```

## Class quick guide

| Class | Write-up depth | Reviewer needed | Gate |
|---|---|---|---|
| A1 reversible | ≤ 150 words | no | no |
| A2 irreversible private | ≤ 400 words | no | yes (`GO_NO_GO`) |
| A3 irreversible public | ≤ 800 words | yes | yes (`GO_NO_GO`) |

## Anti-patterns
- "Let's just try it" with no kill criteria.
- Single-option decisions (no alternative considered).
- Evidence stated as belief instead of cited.
- Re-deciding silently — overwriting the previous file.
- 90-day reviews skipped.

## Linking decisions to bets
Every active item in `STRATEGIC_BETS.md` traces back to a decision file. The bet table includes the decision slug.

## القواعد العربية
1. كل قرار: مالك، مدة، معايير نجاح، معايير إلغاء.
2. الأدلة تُرفق برابط، لا تُلخَّص.
3. خياران على الأقل دائمًا، بما فيها "لا تفعل شيئًا".
4. القرار يُكتب قبل التنفيذ.

## Cross-links
- `GO_NO_GO_DECISION_SYSTEM.md`
- `KILL_LIST.md`
- `docs/strategy/STRATEGIC_BETS.md`
- `CEO_OPERATING_MODEL.md`
