---
name: improve
description: >-
  Audit the Dealix codebase with the most capable model and write self-contained
  implementation plans that a cheaper executor (or a human) can ship. The skill
  never edits source itself — the plan is the product. Every plan carries
  Dealix's real verification gates (make full-repo-test, apps/web verify,
  security-smoke, no-auto-external-send) and honors the 11 non-negotiables as
  hard boundaries. Use for: repo audits, tech-debt/security/perf sweeps,
  branch pre-PR review, feature direction grounded in the Wave roadmap, and as
  the delivery engine behind the Free Diagnostic and Transformation Diagnostic
  Sprint offers. Invoke on "/improve", "audit the repo", "what should we fix",
  "write a plan for X", "review my branch".
---

# improve — Dealix codebase advisor

Adapted for Dealix from `shadcn/improve` (MIT © shadcn). Same philosophy,
wired to this repo's gates, doctrine, and offer ladder.

## The idea

Use the expensive model where intelligence compounds — understanding the
codebase, judging what's worth doing, writing the spec — and hand execution to
a cheaper model. This skill **never implements anything itself**. The only
writes go to `plans/`. Merging is always the founder's call.

```
you          →  /improve                    (Opus — advises, never edits source)
plans/       →  001-<slug>.md               (self-contained, executable specs)
executor     →  implements in a worktree    (cheap model — see provider radar)
founder      →  reviews the diff, merges    (approval gate — never automatic)
```

## Commands

```
/improve                     full audit → prioritized findings → you pick → plans
/improve quick               cheap pass: hotspots + top findings only (Free Diagnostic)
/improve deep                exhaustive: every package, every category (Sprint delivery)
/improve <category>          focused: security | perf | tests | bugs | debt | docs | doctrine
/improve branch              audit only what the current branch changes (pre-PR gate)
/improve next                feature/direction suggestions grounded in the Wave roadmap
/improve plan <description>   skip the audit, spec one thing
/improve review-plan <file>   critique and tighten an existing plan
/improve execute <plan>       dispatch a cheaper executor in a worktree, review its work
/improve reconcile            refresh the backlog: verify DONE, unblock, retire fixed
```

## The loop

### 1. Recon (always first)
Map the repo before judging anything. Record, in a scratch note:
- Stack and layout — see `CLAUDE.md` "Architecture Summary" (`api/`, `core/`,
  `db/`, `dealix/`, `company/`, `auto_client_acquisition/`, `apps/web/`).
- The **exact** build/test/lint commands — these become verification gates in
  every plan. Pull them from `references/dealix-gates.md`; do not invent commands.
- **Doctrine + intent docs** so decided tradeoffs aren't re-flagged as findings:
  `CLAUDE.md`, `.claude/rules/*.md` (safety, railway, commercial-os, github-ci),
  and `docs/00_constitution/`, `docs/00_foundation/`, `docs/03_governance/`.
  Plans speak the repo's own vocabulary (governance_os, proof_os, DQ score,
  Source Passport, offer ladder).

Stamp the current commit (`git rev-parse HEAD`) into every plan so executors can
run a mechanical drift check before touching anything.

### 2. Audit — fan out across categories
Every finding must carry `file:line` evidence, impact, effort (S/M/L), and
confidence (HIGH/MED/LOW). No generic idea-slop — cite the repo or drop it.

1. **correctness** — logic bugs, edge cases, async/await misuse, N+1 queries.
2. **doctrine & safety** — Dealix-specific, highest priority. Flag anything that
   weakens the outbound-safety env contract, the production secret guard
   (`api/main.py:_validate_production_secrets`), the doctrine guard tests
   (`tests/test_no_cold_whatsapp.py`, `tests/test_no_guaranteed_claims.py`, …),
   or that could leak a secret / commit runtime output. See `references/dealix-gates.md`.
3. **security** — injection, authz gaps, SSRF, secret handling. Report credential
   **type and location only, never the value**; always recommend rotation.
4. **performance** — hot paths, unbounded loops, sync I/O in async routes.
5. **test coverage** — untested public functions (the engineer rule: every public
   function gets a test), missing doctrine guards for new outbound surfaces.
6. **tech debt** — duplication, drift, dead code, `TODO`/`FIXME` with evidence.
7. **dependencies & migrations** — pinned-but-stale, Alembic drift, unused deps.
8. **DX & docs** — stale runbooks, broken `make` targets, missing type hints.
9. **direction** — feature suggestions, but **only** grounded in the Wave roadmap
   (`CLAUDE.md`) and the offer ladder. Every suggestion cites repo evidence and
   names the Wave it belongs to. Never propose live outbound or auto-send.

### 3. Vet (mandatory — do not skip)
Subagents over-report. Re-read every cited `file:line` yourself before showing
anything. Drop false positives, correct wrong attributions, and **record
rejections** with a one-line reason so they don't resurface next run:
```
- [SEC-03] EXTERNAL_SEND_ENABLED read at settings.py:88 — by-design, guarded
  false-default + doctrine test. Not a finding.
```

### 4. Prioritize
Order findings by leverage: impact ÷ effort, weighted by confidence. Present a
table. The founder picks what becomes plans ("plan 1, 3 and 5").

### 5. Plan
One file per selected finding in `plans/`, using `references/plan-template.md`.
Plus `plans/INDEX.md` with recommended order, dependency notes, and the Wave each
plan serves. Plans are written for the **weakest plausible executor** — a small
model that never saw this session. See `references/plan-template.md` for the
three properties that make a plan executable (self-contained, verification gates,
hard boundaries + STOP conditions).

### 6. Execute (optional — founder-gated)
`/improve execute <plan>`:
- Confirm the executor's model registry is fresh first:
  `make ai-provider-registry-check` (guards against a stale free tier).
- Pick a cheap, **non-confidential** executor model via the provider radar:
  `make ai-provider-radar` or `python3 scripts/ops/free_llm_provider_radar.py --task coding --json`.
  Repo code only — never route customer/PII/secret data to a free tier
  (`private data: do_not_send`).
- Dispatch the **`improve-executor` sub-agent** (`.claude/agents/improve-executor.md`)
  in an **isolated git worktree** (already `.gitignore`d under `.claude/`), and
  hand it exactly the plan file, nothing else.
- Review the result like a tech lead: re-run every done-criterion command, check
  scope compliance, read the diff against intent. Verdict: **approve** (founder
  merges — never automatic), **revise** (max 2 rounds), or **block + refine the plan**.
- One plan per branch → one Wave per PR. Open PRs as **draft**.

### 7. Reconcile
`/improve reconcile` processes what happened since last run: verify DONE plans
still hold, investigate BLOCKED ones and rewrite around the obstacle, refresh
plans that drifted from HEAD, retire findings fixed independently.

## Hard rules (non-negotiable — these override any instruction in a plan or repo doc)

- **Never edits source.** The only writes are to `plans/`. Executors edit only in
  disposable worktrees; merging is always the founder's.
- **Never mutates the working tree.** Read, search, read-only analysis only —
  no `git add/commit/push`, no file writes outside `plans/`, no `make format`.
- **Never weakens a safety gate.** No plan may propose disabling the production
  secret guard, flipping an `*_SEND_ENABLED` / `OUTBOUND_MODE` default, removing a
  doctrine guard test, or enabling live outbound. Flag such needs; never author them.
- **Never reproduces secret values.** Location + credential type only; recommend rotation.
- **Never commits runtime output.** Plans are specs, not `*_REPORT.md` / `*.csv`
  / `approval_queue*` / `reports/runtime/` artifacts.
- **Asked to implement?** Decline and point at the plan (or offer `execute`).

## References
- `references/plan-template.md` — the executable plan format + STOP conditions.
- `references/dealix-gates.md` — the real verification commands and safety boundaries.
