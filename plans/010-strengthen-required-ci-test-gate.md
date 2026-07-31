# 010 — Promote a real pytest slice into the required CI gate

- **Finding:** `scripts/ops/run_full_repo_test_matrix.sh:97-98` makes the
  **only** "required" pytest step run exactly two self-referential files:
    ```bash
    run_step "pytest-launch-critical-suite" required run_existing_pytest
    run_step "pytest-full-suite-diagnostic" optional python3 -m pytest -q --maxfail=25 --timeout=45
    ```
  `run_existing_pytest()` (lines 68-88) hardcodes exactly
  `tests/test_full_repo_matrix_contract.py` and `tests/test_growth_sales_cards.py`.
  `test_full_repo_matrix_contract.py` (47 lines) is **entirely meta**: it
  reads the matrix script/Makefile/pyproject.toml as text and asserts
  specific substrings exist (e.g. line 27 asserts the diagnostic step
  literally stays `optional`) — it tests zero application behavior. The
  remaining 774 test files (including all 8 doctrine guard tests, the
  api/core/db test suites) only run via the `optional`
  `pytest-full-suite-diagnostic` step, which is capped at `--maxfail=25`
  and whose failures never fail the CI job. This means "Repo matrix: PASS"
  (as claimed in `CLAUDE.md`'s launch status) is compatible with the
  doctrine guard tests, or any api/core test, being broken — a technical
  buyer or investor doing due diligence who reads "all required gates
  green" would reasonably assume much more test coverage is enforced than
  actually is.
- **Category:** tests
- **Wave:** maintenance
- **Effort:** M   **Confidence:** HIGH
- **Written against commit:** aae97bcefcf73e74aef8c75ac593238dc1ed690e

## Drift check (run first)
```bash
git rev-parse HEAD   # if != aae97bcefcf73e74aef8c75ac593238dc1ed690e, re-read the files below before editing
```

## Context (inlined)
- Files in scope: `scripts/ops/run_full_repo_test_matrix.sh`,
  `tests/test_full_repo_matrix_contract.py`
- Current state (`scripts/ops/run_full_repo_test_matrix.sh:68-98`):
    ```bash
    run_existing_pytest() {
      local tests=(
        "tests/test_full_repo_matrix_contract.py"
        "tests/test_growth_sales_cards.py"
      )
      local existing=()
      local test_path

      for test_path in "${tests[@]}"; do
        if [[ -f "$test_path" ]]; then
          existing+=("$test_path")
        fi
      done

      if [[ "${#existing[@]}" -eq 0 ]]; then
        echo "No launch-critical pytest files found"
        return 1
      fi

      python3 -m pytest -q "${existing[@]}"
    }
    ...
    run_step "pytest-launch-critical-suite" required run_existing_pytest
    run_step "pytest-full-suite-diagnostic" optional python3 -m pytest -q --maxfail=25 --timeout=45
    ```
- The doctrine guard tests (must stay green, never removed — per
  `references/dealix-gates.md`) are:
  `tests/test_no_source_passport_no_ai.py`, `tests/test_pii_external_requires_approval.py`,
  `tests/test_no_cold_whatsapp.py`, `tests/test_no_linkedin_automation.py`,
  `tests/test_no_scraping_engine.py`, `tests/test_no_guaranteed_claims.py`,
  `tests/test_output_requires_governance_status.py`, `tests/test_proof_pack_required.py`.
  These currently only run in the optional/capped diagnostic step — they
  should be part of the required gate, since they encode the repo's
  non-negotiables.
- Goal: widen `required` incrementally (doctrine guards first — they're
  fast, focused, and already passing) without suddenly making the whole
  774-file suite required in one step (that could break CI if some of the
  774 files are currently failing/flaky — verify first, don't assume).

## Steps
1. Run the current doctrine guard tests standalone to confirm they all
   pass today (this must be true before promoting them, or the promotion
   would immediately redden CI):
   `python3 -m pytest tests/test_no_source_passport_no_ai.py tests/test_pii_external_requires_approval.py tests/test_no_cold_whatsapp.py tests/test_no_linkedin_automation.py tests/test_no_scraping_engine.py tests/test_no_guaranteed_claims.py tests/test_output_requires_governance_status.py tests/test_proof_pack_required.py -q`
   **Gate:** all 8 files collected, `N passed`, 0 failed. If any fail, STOP
   (see STOP conditions) — do not promote a failing test into `required`.
2. In `scripts/ops/run_full_repo_test_matrix.sh`, extend the `tests` array
   inside `run_existing_pytest()` to include the 8 doctrine guard files
   alongside the existing 2:
    ```bash
    run_existing_pytest() {
      local tests=(
        "tests/test_full_repo_matrix_contract.py"
        "tests/test_growth_sales_cards.py"
        "tests/test_no_source_passport_no_ai.py"
        "tests/test_pii_external_requires_approval.py"
        "tests/test_no_cold_whatsapp.py"
        "tests/test_no_linkedin_automation.py"
        "tests/test_no_scraping_engine.py"
        "tests/test_no_guaranteed_claims.py"
        "tests/test_output_requires_governance_status.py"
        "tests/test_proof_pack_required.py"
      )
      ...
    ```
   **Gate:** `bash -n scripts/ops/run_full_repo_test_matrix.sh` → exit 0 (syntax only).
3. Update `tests/test_full_repo_matrix_contract.py`'s assertions to match
   the new array contents (it currently asserts the old 2-file list exists
   verbatim in the script — read the file first to find the exact
   assertion pattern before editing it, since this plan cannot see its
   exact current line numbers post-drift-check).
   **Gate:** `python3 -m pytest tests/test_full_repo_matrix_contract.py -q` → passes.
4. Run the full matrix locally to confirm the new required step passes:
   `bash scripts/ops/run_full_repo_test_matrix.sh`
   **Gate:** `pytest-launch-critical-suite` reports PASS with 10 files
   collected (2 original + 8 doctrine guards), overall matrix still PASS.

## Done criteria (machine-checkable)
- [ ] `python3 -m pytest tests/test_full_repo_matrix_contract.py tests/test_growth_sales_cards.py tests/test_no_source_passport_no_ai.py tests/test_pii_external_requires_approval.py tests/test_no_cold_whatsapp.py tests/test_no_linkedin_automation.py tests/test_no_scraping_engine.py tests/test_no_guaranteed_claims.py tests/test_output_requires_governance_status.py tests/test_proof_pack_required.py -q` → all pass
- [ ] `make full-repo-test` → all required gates PASS
- [ ] `bash -n scripts/ops/run_full_repo_test_matrix.sh` → exit 0

## Out of scope (do not touch)
- Do not promote the full 774-file `tests/` directory to `required` in this
  plan — that's a much bigger step needing its own audit of currently-
  failing/flaky tests first (a follow-up plan, not this one).
- Do not remove `--maxfail=25 --timeout=45` from the still-optional
  diagnostic step.
- Do not edit any of the 8 doctrine guard test files themselves.

## STOP conditions
- If any of the 8 doctrine guard tests fail when run standalone in step 1
  → STOP, report which one and why; do not "fix" a doctrine guard test to
  make it pass, and do not promote it into `required` while red — that
  would make CI red on a change unrelated to this plan's intent.
- If `test_full_repo_matrix_contract.py`'s current assertions don't match
  the pattern described in step 3 → STOP, re-read the file fresh rather
  than guessing at the edit.
- If promoting these tests reveals a currently-hidden failure (i.e. running
  the full matrix after the edit does NOT pass) → STOP, report the failure;
  do not weaken the new required step to force green.
