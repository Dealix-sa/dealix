# CEO Decision Log

Append-only. Every meaningful decision goes here on the day it is made.

## Purpose

Make decisions auditable. If a decision is not in this log it does not
exist — anyone in the company can use that rule to push back.

## Owner

Founder. Anyone can append a "decision proposed" entry; only the founder
moves it to "decided".

## Cadence

Per-decision. Reviewed weekly (see `CEO_WEEKLY_REVIEW.md`).

## Source of Truth

This file is the source of truth for decisions. The decision is
"the writeup", not what was said in a meeting.

## Inputs

- Context (what triggered the decision)
- Options considered (at least two)
- Risk + reversibility note
- Owner of follow-through

## Outputs

- A new row in the table below
- A scheduled review date if the decision is reversible

## KPI

- Decisions logged within the same day they were made
- 0 decisions found in chat / email that are not also here

## Trust Boundary

This log never leaves the company without explicit approval.

## Failure Mode

- Decisions made but not logged → impossible to learn from.
- Logged but no owner → drifts into limbo.

## Recovery Path

If you find a decision in chat that isn't here, write it here now with
the original date. Late is better than missing.

## Verification

```bash
make business-os
```

`verify_business_os.py` requires the structural sections above to be
present in every business doc — including this one.

## Decisions

| Date | Decision | Options Considered | Risk / Reversible? | Owner | Review By |
| --- | --- | --- | --- | --- | --- |
| 2026-05-24 | Adopt the Audit-First Remediation Layer | (a) ship features anyway, (b) build manifest+verifier first | Low risk, fully reversible (delete files) | Founder | 2026-06-07 |

## Next Action

When you make a decision today, add a row.
