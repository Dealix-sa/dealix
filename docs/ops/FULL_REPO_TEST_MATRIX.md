# Dealix Full Repo Test Matrix

Run one comprehensive validation pass for the repository.

## Command

```bash
bash scripts/ops/run_full_repo_test_matrix.sh
```

Or through Makefile after this PR is merged:

```bash
make full-repo-test
```

## What it checks

- Python version
- Python compile/import surfaces
- environment contract
- security smoke
- no-auto-send guard
- company launch readiness
- full pytest suite
- Launch OS dry runs
- production verification bundle
- apps/web install
- apps/web typecheck and build
- TestSprite MCP environment check
- TestSprite MCP smoke check when `TESTSPRITE_API_KEY` is available

## Safe defaults

The runner uses test mode by default:

```bash
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

To include the MCP smoke check:

```bash
export TESTSPRITE_API_KEY="..."
bash scripts/ops/run_full_repo_test_matrix.sh
```

Use rotated keys only and keep live customer data out of test runs.
