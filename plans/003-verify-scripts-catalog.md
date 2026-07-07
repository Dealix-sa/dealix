# 003 — Catalog the 57 verify_*.py scripts

- **Finding:** `scripts/` holds **57** `verify_*.py` scripts
  (`ls scripts/verify_*.py | wc -l` → 57) with no single index of what each one
  checks or which are wired into `make full-repo-test`. New contributors (and the
  `improve` executor) cannot tell which verifier covers which surface, so
  coverage gaps and duplication hide in plain sight.
- **Category:** docs/DX   **Wave:** maintenance
- **Effort:** S   **Confidence:** HIGH
- **Written against commit:** 2ec6a6c
- **Status:** 📋 TODO

## Drift check (run first)
```bash
git rev-parse HEAD          # if != 2ec6a6c, re-count below before planning
ls scripts/verify_*.py | wc -l
```

## Steps
1. Add `scripts/ops/build_verify_catalog.py`: import-free scan that reads the
   module docstring (first line) of each `scripts/verify_*.py` and emits a
   markdown table (script → one-line purpose). Mirror the offline, pure-function
   style of `scripts/ops/free_llm_provider_radar.py`
   (`from __future__ import annotations`, `pathlib`, no third-party deps).
   **Gate:** `python3 scripts/ops/build_verify_catalog.py > /dev/null` → exit 0.
2. Write the rendered table to `docs/ops/VERIFY_SCRIPTS_CATALOG.md` (committed
   doc, not runtime output).
   **Gate:** file exists and lists 57 rows.
3. Add `tests/test_verify_catalog.py`: assert the catalog covers every
   `scripts/verify_*.py` (no script missing a row).
   **Gate:** run the test standalone (repo `conftest.py` needs the async stack;
   this test is pure-stdlib) → passes.

## Done criteria (machine-checkable)
- [ ] `python3 scripts/ops/build_verify_catalog.py --check` → exit 0 (catalog in sync)
- [ ] `docs/ops/VERIFY_SCRIPTS_CATALOG.md` row count == `ls scripts/verify_*.py | wc -l`

## Out of scope
- Do NOT delete, merge, or rename any `verify_*.py` — cataloging only. Consolidation
  is a separate finding once the map exists.
- Do NOT change `make full-repo-test` wiring.

## STOP conditions
- If a `verify_*.py` has no module docstring → record it in the catalog as
  `(no docstring — needs one)`, do not invent a purpose.
- If the count differs from 57 → STOP, the repo drifted; re-run the audit.
