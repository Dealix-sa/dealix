# Founder Decision Log

> Public-safe summary of every meaningful CEO decision.
> Detailed reasoning + sensitive context lives in `founder/decision_log.md` (private repo).

## Format

```
YYYY-MM-DD | type | subject | rationale (one line) | revisit
```

- **type**: BUILD · FIX · KILL · DEFER · APPROVE · REJECT · ESCALATE
- **subject**: short noun phrase
- **rationale**: one line — public-safe (no client names, no numbers > 5K SAR)
- **revisit**: date or `n/a`

## Log

```
2026-05-23 | BUILD  | Company OS (12 Super Systems)         | Founder leverage + system-of-record       | n/a
2026-05-23 | DEFER  | Paid acquisition channels             | Wait until 3 paid sprints delivered       | 2026-08-01
2026-05-23 | KILL   | Multi-feature roadmap for v3 platform | Conflicts with Revenue Sprint focus       | n/a
2026-05-23 | APPROVE| Trust approval matrix v1              | NIST AI RMF aligned + audit-ready         | n/a
```

## Discipline

- Add the row the same day. Backfilling is a tell.
- One line. If you need more than one line, the decision is too vague — sharpen it.
- Sensitive context stays in the private log. The public log is for **what** and **why-in-one-line**.

## Connection To Other Systems

- Every `BUILD` row must link to a `docs/product/FEATURE_INTAKE.md` entry within 7 days
- Every `KILL` row must trigger removal/archival of the killed thing within 7 days
- Every `DEFER` row with a passed revisit date and no follow-up becomes an implicit `KILL`
- Every `APPROVE` of a Trust action must have a matching entry in `dealix/trust/approval_matrix.py`
