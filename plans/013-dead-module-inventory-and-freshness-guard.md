# 013 — Inventory unwired auto_client_acquisition modules + add a freshness guard

- **Finding:** `auto_client_acquisition/` has 80 subdirectories ending in
  `_os`. A sampled audit (15 dirs, cross-checked against every import in
  `api/`, `company/`, `dealix/`, and each other `_os` module) found the
  code itself is uniformly well-written (typed dataclasses, real
  computation, docstrings — e.g. `moat_os/moat_score.py:38-76`'s weighted
  scoring, `dominance_os/dominance_scorecard.py:51-58`'s validated
  recommendation logic), **not** stub/placeholder bloat. The problem is
  architectural: of the 80 `_os` directories, an estimated **39-45 (≈49%)**
  are never imported by anything the running product actually executes
  (`api/`, `company/`, `dealix/`) — including `dominance_os`, `moat_os`,
  `meta_os`, `holding_os`, `ultimate_manual_os`, `board_ready_os`,
  `institutional_os`, `sandbox_os`, `workflow_os`, `standards_os`,
  `investment_os`. Some form closed reference loops (`endgame_os` →
  `global_grade_os` → `sovereignty_os` → back) that look like an
  interconnected system but never reach a real entry point. This is
  exactly the pattern CLAUDE.md's "What NOT to Do" forbids ("claim
  features not yet implemented") in spirit — a technical buyer or investor
  running `grep -r "import auto_client_acquisition.dominance_os" api/
  company/` would find nothing, undermining any "150+ integrated systems"
  narrative. Given the scale (80 modules, thousands of lines, real tests
  for 56 of them), deciding module-by-module whether to wire, retire, or
  keep-for-a-future-Wave is a founder call, not something an executor
  should decide unilaterally by deleting tested code. This plan produces
  the inventory + a mechanical guard against the pattern recurring; it
  does not delete or rewire any module.
- **Category:** direction / tech-debt
- **Wave:** maintenance (informs future Wave sequencing decisions)
- **Effort:** M   **Confidence:** HIGH
- **Written against commit:** aae97bcefcf73e74aef8c75ac593238dc1ed690e

## Drift check (run first)
```bash
git rev-parse HEAD   # if != aae97bcefcf73e74aef8c75ac593238dc1ed690e, re-run the discovery commands below fresh — the exact wired/unwired split may have shifted
```

## Context (inlined)
- This plan writes one new doc and one new script; it does not touch any
  existing `auto_client_acquisition/` module.
- "Wired" definition for this plan: a module is wired if any file under
  `api/`, `company/`, or `dealix/` contains
  `from auto_client_acquisition.<module>` or `import auto_client_acquisition.<module>`
  (directly — not transitively through another `_os` module).
- Repo convention: docs like this belong under `docs/ops/` per the
  existing `docs/ops/VERIFY_SCRIPTS_CATALOG.md` precedent (built by plan
  003 in this same backlog — mirror its style: a generated table, a
  builder script, and a test asserting the table matches the live repo).

## Steps
1. Write `scripts/ops/build_os_module_wiring_catalog.py`, modeled on the
   existing `scripts/ops/build_verify_catalog.py` (read that file first for
   the pattern to mirror). It should:
   - Glob every immediate subdirectory of `auto_client_acquisition/`.
   - For each, grep `api/`, `company/`, `dealix/` for a direct import of
     `auto_client_acquisition.<name>` (use Python's `ast` module or a
     simple regex on `import`/`from` lines — mirror whatever approach
     `build_verify_catalog.py` uses for consistency).
   - For each, check whether it's imported by any *other* `_os` module
     (transitive-only wiring) and flag that separately from direct wiring.
   - Check whether a `tests/test_<module>*.py` file exists for it.
   - Emit a markdown table to `docs/ops/AUTO_CLIENT_ACQUISITION_WIRING_CATALOG.md`
     with columns: Module | Directly wired (Y/N) | Transitively wired (Y/N) | Has tests (Y/N) | File count | Line count.
   **Gate:** `python3 scripts/ops/build_os_module_wiring_catalog.py` → writes the file without error.
2. Add `tests/test_os_module_wiring_catalog.py` (mirror
   `tests/test_verify_catalog.py`'s structure) asserting the generated
   catalog file is up to date with the live repo (regenerate into a temp
   file, diff against the committed one) — this is a freshness guard, not
   an enforcement gate: it does not fail if a module is unwired, only if
   the *catalog* has drifted from reality.
   **Gate:** `python3 -m pytest tests/test_os_module_wiring_catalog.py -q` → passes.
3. At the top of `docs/ops/AUTO_CLIENT_ACQUISITION_WIRING_CATALOG.md`, add
   a short preamble (not a judgment on which modules to keep — that's the
   founder's call) stating: how to regenerate the table
   (`python3 scripts/ops/build_os_module_wiring_catalog.py`), and three
   options for any unwired module going forward — wire it into a real
   entry point, mark it explicitly `# STATUS: reserved for Wave <N>` in its
   package docstring, or move it to `archive/`. Do not apply any of these
   three options to any module yourself in this plan.
   **Gate:** `grep -n "STATUS: reserved" docs/ops/AUTO_CLIENT_ACQUISITION_WIRING_CATALOG.md` → the preamble text is present (as instructions, not applied to any module).
4. Add one line to `CLAUDE.md`'s "Key File Locations" table pointing at the
   new catalog doc, mirroring the existing "Verify scripts catalog" row.
   **Gate:** `grep -n "AUTO_CLIENT_ACQUISITION_WIRING_CATALOG" CLAUDE.md` → 1 match.

## Done criteria (machine-checkable)
- [ ] `python3 scripts/ops/build_os_module_wiring_catalog.py && python3 -m pytest tests/test_os_module_wiring_catalog.py -q` → passes
- [ ] `docs/ops/AUTO_CLIENT_ACQUISITION_WIRING_CATALOG.md` exists and lists all 80 `_os` directories present at run time (count must match `ls -d auto_client_acquisition/*_os | wc -l`)
- [ ] `make full-repo-test` → all required gates PASS

## Out of scope (do not touch)
- Do not delete, move, or modify any file under `auto_client_acquisition/`
  itself in this plan.
- Do not wire any currently-unwired module into `api/`, `company/`, or
  `dealix/` — that requires a per-module product decision this plan
  deliberately defers to the founder.
- Do not make the wiring status a required/blocking CI gate — only the
  catalog's own freshness is enforced, not module wiring itself.

## STOP conditions
- If the actual wired/unwired counts differ substantially from this
  plan's estimate (e.g. far more or fewer than ~40 unwired) → not a
  problem, just report the real numbers; the estimate was from a 15-module
  sample and the full catalog is expected to refine it.
- If `scripts/ops/build_verify_catalog.py` doesn't exist or has a
  substantially different structure than expected → STOP and read it fresh
  before modeling the new script on it.
