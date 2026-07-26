# plans/

Backlog of executable implementation plans produced by the `improve` skill
(`.claude/skills/improve/`). **These are specs, not runtime output — they are
committed to the repo on purpose.**

## Convention

- One file per finding: `NNN-<slug>.md` (e.g. `001-extract-shadow-config.md`).
- `INDEX.md` — recommended order, dependency graph, and the Wave each plan serves.
- Each plan is self-contained and written for the weakest plausible executor.
  Format: `.claude/skills/improve/references/plan-template.md`.

## Lifecycle

```
/improve            → audit → you pick findings → plans land here
/improve execute N  → cheap executor implements plan N in a disposable worktree
                      (founder reviews the diff and merges — never automatic)
/improve reconcile  → verify DONE, unblock BLOCKED, retire fixed, refresh drifted
```

## Rules

- A plan never weakens a safety gate. If a change needs one, it STOPs and
  escalates to the founder — see the plan template's STOP conditions.
- One plan per branch → one Wave per PR → PRs open as **draft**.
- Plans reference only real gates from `.claude/skills/improve/references/dealix-gates.md`.
