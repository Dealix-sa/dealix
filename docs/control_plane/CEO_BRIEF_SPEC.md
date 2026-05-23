# CEO Brief Specification

The Daily CEO Brief is a deterministic render of `CompanyState`.

## Inputs

- `state: CompanyState` (required)
- `focus: str | None` — the single CEO focus for the day
- `kill_or_defer: list[str] | None` — items the CEO is choosing to drop

## Sections (fixed order)

1. Date
2. One Focus Today
3. Revenue
4. Sales
5. Delivery
6. Trust
7. Product
8. Decisions Required
9. Kill / Defer Today
10. End-of-Day Result

## Storage

The rendered brief is written by the daily workflow to:

- `dealix-ops-private/founder/daily_brief.md` (canonical, private repo)
- public archive is **not** allowed; the brief contains operational data

## Rules

- The brief is regenerated every day, not appended.
- No PII, no client names, no internal disputes in the public repo.
- A blank `One Focus Today` is a quality failure — the founder must pick one.
