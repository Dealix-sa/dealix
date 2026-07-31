# 011 — Archive dead root-level "wave checkpoint" scripts and stale build files

- **Finding:** The repo root has 96 loose (non-directory) files. A cluster
  of ~30 one-off Python/TS scripts (`auto14.py`, `z7_check.py`,
  `z7_router.py`, `z7_snapshot.ts`, `z8_check.py`, `z8_snapshot.ts`,
  `u11_check.py`, `u11_snapshot.ts`, `v12_check.py`, `v12_snapshot.ts`,
  `s9_check.py`, `s9_snapshot.ts`, `t10_check.py`, `t10_snapshot.ts`,
  `m6_check.py`, `m6_runtime.py`, `m6_snapshot.ts`, `rcmax.py`,
  `rcmax_state.ts`, `client_ops_max.py`, `ci_core.py`, `score_core.py`,
  `run_os16.py`, `v3_app.py`, `tiny_ok.py`) form a self-referential import
  chain (`client_ops_max.py:7` imports `auto14`; `z7_router.py:6` imports
  `m6_runtime`; `z8_check.py:1` imports `dealix_daily_os`; `run_os16.py:4-6`
  imports `ci_core`, `score_core`, `client_ops_max`) but are **never**
  referenced by `Makefile`/`Makefile.*` or any `.github/workflows/*.yml`
  (confirmed via repo-wide grep, zero hits). `tiny_ok.py` is literally
  `print('ok')`. Four root-level `test_*.py` files
  (`test_auto14.py`, `test_client_ops_max.py`, `test_rcmax.py`,
  `test_service_os_frontend.py`) exist for some of these but are never
  collected by pytest (`pyproject.toml:167` sets `testpaths = ["tests"]`).
  Separately, six Makefile variants (`Makefile.cmd-v2`,
  `Makefile.command-center`, `Makefile.commercial`,
  `Makefile.commercial-growth-os-v2`, `Makefile.company`, `Makefile.launch`)
  are never `include`d by the canonical `Makefile` (per CLAUDE.md:54) and
  never invoked from CI — dead duplicates. `Dockerfile.company-brain` and
  `Dockerfile.web` are referenced only by `railway.company-brain.toml` and
  `railway.web.toml`, which are themselves never referenced by any CI
  workflow, Makefile target, or script — an abandoned alternate-deploy
  topology. This clutter is the first thing anyone browsing the repo root
  sees, and it actively looks unmaintained/abandoned to a technical buyer.
- **Category:** tech-debt
- **Wave:** maintenance
- **Effort:** M   **Confidence:** HIGH
- **Written against commit:** aae97bcefcf73e74aef8c75ac593238dc1ed690e

## Drift check (run first)
```bash
git rev-parse HEAD   # if != aae97bcefcf73e74aef8c75ac593238dc1ed690e, re-verify each file below is still unreferenced before moving/deleting it
```

## Context (inlined)
- This plan **moves to an archive directory rather than deletes**, since
  some of this code may still hold institutional logic the founder wants
  to reference later, and deletion of git-tracked history is always
  recoverable via git anyway but an archive folder makes the "this is
  intentionally retired, not lost" signal visible without digging through
  git log.
- Files in scope (root-level, move into `archive/wave-checkpoints/`):
  `auto14.py`, `auto14_state.ts`, `z7_check.py`, `z7_router.py`,
  `z7_snapshot.ts`, `z8_check.py`, `z8_snapshot.ts`, `u11_check.py`,
  `u11_snapshot.ts`, `v12_check.py`, `v12_snapshot.ts`, `s9_check.py`,
  `s9_snapshot.ts`, `t10_check.py`, `t10_snapshot.ts`, `m6_check.py`,
  `m6_runtime.py`, `m6_snapshot.ts`, `rcmax.py`, `rcmax_state.ts`,
  `client_ops_max.py`, `ci_core.py`, `score_core.py`, `run_os16.py`,
  `v3_app.py`, `tiny_ok.py`, `test_auto14.py`, `test_client_ops_max.py`,
  `test_rcmax.py`, `test_service_os_frontend.py`,
  `dealix_acquisition_pack.py`, `dealix_daily_os.py`,
  `dealix_gtm_launch_kit.py`, `dealix_revenue_machine.py`,
  `dealix_sales_materials_factory.py`, `generate_service_os_snapshot.py`.
- Makefiles to move: `Makefile.cmd-v2`, `Makefile.command-center`,
  `Makefile.commercial`, `Makefile.commercial-growth-os-v2`,
  `Makefile.company`, `Makefile.launch`.
- Root docs that document only the archived scripts (move alongside them):
  `AUTO14_RUNBOOK.md`, `M6.md`, `RCMAX_RUNBOOK.md`,
  `CLIENT_OPS_MAX_RUNBOOK.md`, `S9_REVENUE_PLAYBOOK.md`,
  `T10_CLIENT_ACQUISITION_PLAYBOOK.md`, `U11_SALES_MATERIALS_PLAYBOOK.md`,
  `V12_GTM_LAUNCH_PLAYBOOK.md`, `Z7.md`, `Z8.md`, `Z8_COMMERCIAL_PLAYBOOK.md`.
- `Dockerfile.company-brain`, `Dockerfile.web`, `railway.company-brain.toml`,
  `railway.web.toml`: move Dockerfiles to `archive/`, leave the `railway.*.toml`
  files in place but do not fix/wire them (flag their orphan status in the
  archive README instead — deleting Railway config the founder may still
  intend to use is riskier than deleting a checkpoint script).

## Steps
1. For every file in the "root-level" list above, re-verify it is still
   unreferenced before moving it (drift re-check, since this list was
   compiled from a point-in-time audit):
   `grep -rn "import auto14\|import z7_router\|import m6_runtime\|import ci_core\|import score_core\|import client_ops_max\|import dealix_daily_os" --include="*.py" . | grep -v "^\./archive/"`
   Any file whose only references are from other files *also* in this
   move-list is still safe to move (the whole cluster moves together).
   If a file turns out to be imported from somewhere outside this list
   (e.g. from `api/`, `company/`, `scripts/`) → remove it from scope and
   report it instead of moving it.
   **Gate:** command runs, output reviewed, scope list confirmed/adjusted.
2. Create `archive/wave-checkpoints/README.md` explaining what this
   directory is: retired one-off wave/sprint scripts and their runbooks,
   kept for reference, not wired into any Makefile/CI, safe to delete
   entirely in the future if never needed.
   **Gate:** file exists.
3. `git mv` each file from the scoped lists into `archive/wave-checkpoints/`
   (flat, preserving filenames) — use `git mv`, not `rm` + new file, so
   history is preserved.
   **Gate:** `git status --short` shows renames (`R`), not deletions +
   additions.
4. `git mv` the six dead Makefile variants into `archive/wave-checkpoints/`
   as well.
   **Gate:** `ls Makefile.*` at repo root shows none of the six remain.
5. `git mv Dockerfile.company-brain Dockerfile.web archive/wave-checkpoints/`.
   Leave `railway.company-brain.toml` and `railway.web.toml` in place, but
   add one line to each noting in a comment that the Dockerfile it pointed
   to has moved to `archive/` and this config is not currently wired to any
   CI/deploy path — do not delete these two toml files without founder
   confirmation they're truly unused (they might be a planned future
   deploy topology).
   **Gate:** `ls Dockerfile.company-brain Dockerfile.web` at repo root →
   "No such file"; both exist under `archive/wave-checkpoints/`.
6. Re-run compileall and the launch-critical test suite to confirm nothing
   broke:
   `python3 -m compileall -q api core db dealix company`
   **Gate:** exit 0.

## Done criteria (machine-checkable)
- [ ] `find . -maxdepth 1 -type f | wc -l` → fewer than the original 96 (report exact new count)
- [ ] `python3 -m compileall -q api core db dealix company` → exit 0
- [ ] `make full-repo-test` → all required gates PASS
- [ ] `git log --follow --oneline archive/wave-checkpoints/auto14.py | head -1` → shows history preserved (not a fresh file)

## Out of scope (do not touch)
- Do not move `Dockerfile`, `Dockerfile.worker`, `Dockerfile.watchdog` —
  these are actively wired (per `railway.toml`, `docker-compose.prod.yml`,
  `.github/workflows/ci.yml`).
- Do not move the canonical `Makefile`.
- Do not delete `railway.company-brain.toml` / `railway.web.toml` — only
  annotate them.
- Do not touch any file not explicitly listed above, even if it looks
  similar (e.g. leave `cli.py`, `cli/`, `auto_client_acquisition/` alone —
  those are separate, wired systems).

## STOP conditions
- If step 1's re-check finds a file imported from outside the move-list
  scope → STOP for that file, remove it from scope, continue with the rest.
- If any doctrine guard test or `test_full_repo_matrix_contract.py` fails
  after the move → STOP, do not edit the test; the move likely broke a
  path the test asserts on — report and reconsider which files to move.
- If `git mv` reports the destination already exists → STOP, do not
  overwrite; report the collision.
