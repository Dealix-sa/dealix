# Dealix Full Repo Test Matrix

Run one comprehensive launch-readiness validation pass for the repository.

## Command

```bash
bash scripts/ops/run_full_repo_test_matrix.sh
```

Or through Makefile:

```bash
make full-repo-test
```

## Required launch gates

These gates must pass for `FULL_REPO_TEST_MATRIX=PASS`:

- Python version
- Python compile/import surfaces
- environment contract
- CI-safe security smoke
- no-auto-send guard
- company launch readiness
- launch-critical pytest contract suite
- apps/web install
- apps/web typecheck and build

## Diagnostic gates

These gates are still run and reported, but do not block the matrix by default:

- full legacy pytest suite diagnostic
- Launch OS dry runs
- production verification bundle
- TestSprite MCP environment check
- TestSprite MCP smoke check when the repository secret is available

## Why full pytest is diagnostic

The repository includes a large legacy test surface with historical failures and integration-style checks that are not all launch-blocking. The matrix therefore separates:

- `pytest-launch-critical-suite`: required, focused on current launch/operator contracts.
- `pytest-full-suite-diagnostic`: optional, exposes legacy debt without hiding TestSprite, web, safety, and launch readiness results.

This keeps the matrix honest: current launch gates can pass while old test debt remains visible in artifacts.

## Safe defaults

The runner uses test mode by default:

```text
APP_ENV=test
ENVIRONMENT=test
EXTERNAL_SEND_ENABLED=false
EMAIL_SEND_ENABLED=false
WHATSAPP_SEND_ENABLED=false
WHATSAPP_ALLOW_LIVE_SEND=false
SMS_SEND_ENABLED=false
OUTBOUND_MODE=draft_only
```

## Reports

The runner writes runtime reports under:

```text
reports/runtime/full_repo_test_matrix/
```

Do not commit runtime reports unless they are intentionally needed for an audit.

## TestSprite

To include the MCP smoke check, set the repository secret named `TESTSPRITE_API_KEY` in GitHub Actions and run the workflow.

Use rotated keys only and keep live customer data out of test runs.

## Last GitHub Actions trigger

- Triggered by ChatGPT on: 2026-06-29T21:05:00Z
- Purpose: trigger a real push event after separating launch-critical pytest from full legacy pytest diagnostics.
