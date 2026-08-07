# 019 — Close the SHA-parity gap in the scheduled production smoke check

- **Finding:** Two production-verification mechanisms already exist and
  are well-built, but neither one continuously proves "the SHA on `main`
  is the SHA actually running in production":
  - `.github/workflows/railway_deploy.yml:230-281` ("Smoke test /healthz")
    *does* compare the live `/version` endpoint's `git_sha` against
    `$GITHUB_SHA` and fails the deploy if they don't match — but this only
    runs at the moment of a push-triggered deploy. If that specific
    workflow run doesn't execute cleanly (no `RAILWAY_TOKEN` configured,
    the job is skipped, etc.) or if Railway's service configuration is
    changed out-of-band afterward (a known risk explicitly flagged in
    `.claude/rules/dealix-railway.md`: "Service source may be
    `ghcr.io/railwayapp-temp` — must be reconnected to GitHub repo"),
    nothing re-checks it later.
  - `.github/workflows/production-smoke.yml` runs every 6 hours
    (`cron: '0 */6 * * *'`) via `scripts/dealix_smoke_test.py`, but that
    script's `/version` check (`scripts/dealix_smoke_test.py:143`:
    `expect_in_body=["status", "git_sha"]`) only asserts the field is
    *present* — it never compares the returned `git_sha` value against
    anything. A scheduled run reports ✅ PASS even if Railway is serving a
    SHA from a month ago, as long as `/version` returns some git_sha.
  This exact gap is why the Founder-360 report could plausibly find
  Railway running stale production while `main`'s CI stayed green — there
  is no standing, continuously-scheduled check that would have caught
  drift introduced between deploys. The fix is small: `production-smoke.yml`
  is triggered by `schedule:`, so `$GITHUB_SHA` in that run *is* the
  current `main` HEAD at trigger time — the value needed for comparison is
  already available for free, it's just never used.
- **Category:** doctrine / ops
- **Wave:** maintenance
- **Effort:** M   **Confidence:** HIGH
- **Written against commit:** aae97bcefcf73e74aef8c75ac593238dc1ed690e

## Drift check (run first)
```bash
git rev-parse HEAD   # if != aae97bcefcf73e74aef8c75ac593238dc1ed690e, re-read scripts/dealix_smoke_test.py and .github/workflows/production-smoke.yml before editing
```

## Context (inlined)
- Files in scope: `scripts/dealix_smoke_test.py`,
  `.github/workflows/production-smoke.yml`.
- `api/routers/platform_meta.py:66-79`'s `/version` endpoint already
  returns `git_sha` (via `_deployment_git_sha()`) — no backend change
  needed, this is purely a CI-script fix.
- `dealix_smoke_test.py` is structured as a list of check dataclasses fed
  through a `run()` function that returns a report dict
  (`{"passed": N, "total": N, "failed_required": N, "results": [...]}`)
  rendered as text or JSON (`main()`, lines 393-426). Add a new check in
  the same style, not a bolted-on side script.
- Do not build a brand-new standalone verifier script — that would add a
  38th script to an already-sprawling `scripts/` directory (37+ existing
  smoke/production-check scripts found via
  `grep -rli "smoke\|production" scripts/*.py scripts/*.sh` during this
  audit). Extend the two files already wired into the two relevant
  workflows.

## Steps
1. In `scripts/dealix_smoke_test.py`, add a `--expect-git-sha` CLI
   argument (default: `os.getenv("GITHUB_SHA", "")`) and a new required
   check that: fetches `/version`, extracts `git_sha` from the JSON body,
   and — only if `--expect-git-sha` is non-empty — fails (required check)
   if the live `git_sha` doesn't case-insensitively equal the expected
   value. When `--expect-git-sha` is empty (e.g. someone runs the script
   locally without it), the check is skipped entirely, not failed — this
   must never break local/manual usage.
   **Gate:** `python3 scripts/dealix_smoke_test.py --help | grep -q expect-git-sha`.
2. In `.github/workflows/production-smoke.yml`, pass
   `--expect-git-sha "$GITHUB_SHA"` to the `dealix_smoke_test.py`
   invocation (line 45) so every scheduled run (where `$GITHUB_SHA` is
   the current `main` HEAD at trigger time) now fails loudly the moment
   Railway drifts from `main`, instead of silently reporting a green
   dashboard.
   **Gate:** `grep -n "expect-git-sha" .github/workflows/production-smoke.yml` → 1 match.
3. Add a unit test for the new check logic in
   `tests/test_dealix_smoke_test_sha_parity.py` (or extend an existing
   smoke-test unit test file if one already covers `dealix_smoke_test.py`
   — check `tests/` for one before creating a new file) covering: matching
   SHA passes, mismatched SHA fails as a required check, empty
   `--expect-git-sha` skips the check without failing.
   **Gate:** `python3 -m pytest tests/test_dealix_smoke_test_sha_parity.py -q` → passes.

## Done criteria (machine-checkable)
- [ ] `python3 scripts/dealix_smoke_test.py --expect-git-sha deadbeef --base-url https://api.dealix.me --json 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['failed_required'] > 0)"` → prints `True` when pointed at any real deploy not currently on commit `deadbeef` (a manual sanity check the founder can run once; not part of automated CI since it requires network access to prod).
- [ ] `python3 -m pytest tests/test_dealix_smoke_test_sha_parity.py -q` → passes
- [ ] `bash -n .github/workflows/production-smoke.yml` is not applicable (YAML, not bash) — instead: `python3 -c "import yaml; yaml.safe_load(open('.github/workflows/production-smoke.yml'))"` → no exception
- [ ] `make full-repo-test` → all required gates PASS

## Out of scope (do not touch)
- Do not touch `.github/workflows/railway_deploy.yml` — its SHA-parity
  check at deploy-time is already correct; this plan only closes the gap
  in the *scheduled, standing* check.
- Do not add a new standalone script — extend the two files named above.
- Do not attempt to fix the underlying Railway configuration/source
  mismatch described in `.claude/rules/dealix-railway.md` — that's a
  founder-only infra action (billing, service source reconnection,
  environment variables), this plan only makes future drift impossible to
  miss.
- Do not touch `DEALIX_SMOKE_API_KEY` or any other secret.

## STOP conditions
- If `scripts/dealix_smoke_test.py`'s check/report structure has changed
  substantially from the pattern described above → STOP, re-read the file
  fresh before adding a check in a different style than the rest of the
  file.
- If `production-smoke.yml`'s `schedule:` trigger has been removed or
  changed such that `$GITHUB_SHA` no longer reliably means "current main
  HEAD" at trigger time → STOP and report; the fix's core assumption would
  no longer hold.
- If adding the required SHA-parity check would fail the *next* scheduled
  run because production is currently known to be stale (per the
  Founder-360 report) → this is expected and correct, not a bug — do not
  soften the check to avoid a red run; a red run here is the entire point
  (it makes the drift visible instead of hidden).
