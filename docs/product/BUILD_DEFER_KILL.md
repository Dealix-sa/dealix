# Build / Defer / Kill

> The weekly decision. The same three verbs every Friday.

## How to use

In the Weekly CEO Review, the founder reviews:

- The feature intake queue
- The active builds
- The workflow success log

For each item, the decision is one of:

- **Build now** — passes the rules in `FEATURE_INTAKE.md`.
- **Defer** — has merit but lacks evidence (workflow level, reach, or
  effort budget).
- **Kill** — fails the rules; goes to `KILL_LIST.md`.

## Decision Recording

For each weekly decision, write into
`dealix-ops-private/product/build_defer_kill_log.md`:

```
- id: BDK-yyyy-mm-dd-NN
  item_id: F-...
  decision: build / defer / kill
  rationale: short
  next_review_date: yyyy-mm-dd (for defer)
  kill_list_entry: K-... (for kill)
```

## Defaults

When in doubt:
- Defer > Build.
- Kill > Defer when the item has been deferred for 90+ days without
  new evidence.

## What "Build" means

- A build is funded with founder hours (and any external cost).
- A build has a kill-by-date.
- A build has a written success metric.
- A build does not silently extend.

## What "Defer" means

- The intake stays in the queue.
- The defer rationale is named.
- The defer review date is set (default: 30 days).

## What "Kill" means

- The intake closes.
- An entry goes into `KILL_LIST.md`.
- A revisit trigger is named (or the kill is permanent).

## Weekly Reporting

The Weekly CEO Review includes:

- Number of items reviewed.
- Build / Defer / Kill counts.
- The dominant pattern (e.g. "most asks depend on a workflow at Level 0").
