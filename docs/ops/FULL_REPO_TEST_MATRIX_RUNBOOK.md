# Full Repo Test Matrix Runbook

## Current purpose

This runbook tracks how Dealix validates the repository end-to-end before launch, demos, release gates, and agent-generated code merges.

## Official commands

```bash
make full-repo-test
```

Equivalent direct command:

```bash
bash scripts/ops/run_full_repo_test_matrix.sh
```

CI-safe security gate only:

```bash
make security-smoke-ci
```

## GitHub Actions workflow

Workflow file:

```text
.github/workflows/full-repo-test-matrix.yml
```

The workflow uses:

- Python 3.11
- Node 20
- `pip install -e ".[dev]"`
- `bash scripts/ops/run_full_repo_test_matrix.sh`
- GitHub Actions artifact upload for `reports/runtime/full_repo_test_matrix/`

## Required secret

For TestSprite MCP smoke checks, add a repository secret:

```text
TESTSPRITE_API_KEY
```

Do not place this key in repo files, issues, comments, PR bodies, logs, or screenshots.

## Last known real run

Run:

```text
https://github.com/Dealix-sa/dealix/actions/runs/28393905830
```

Outcome:

- GitHub job completed with failure.
- The matrix report artifact uploaded successfully.
- TestSprite env check passed.
- TestSprite MCP smoke passed.
- `apps/web` install passed.
- `apps/web` verify/build passed.
- Initial failures were `security-smoke` and `pytest-full-suite`.

Fixes applied after this run:

- Added CI-safe security gate: `scripts/ops/security_smoke_ci.py`
- Updated full matrix runner to use the CI-safe gate.
- Added `pytest-timeout>=2.3.1` to dev dependencies.
- Exposed `make full-repo-test` and `make security-smoke-ci`.

## Interpreting the matrix

Required failures block the matrix:

- Python version
- Python compileall core surfaces
- env contract
- CI security smoke
- no-auto-send guard
- company launch readiness
- pytest full suite
- apps/web install
- apps/web verify

Optional failures do not block the matrix by default:

- Launch OS dry-runs
- production verify bundle
- TestSprite env check
- TestSprite MCP smoke

## Runtime reports

Each run writes:

```text
reports/runtime/full_repo_test_matrix/latest.md
reports/runtime/full_repo_test_matrix/latest.json
reports/runtime/full_repo_test_matrix/logs-<timestamp>/
```

GitHub Actions uploads the same folder as an artifact named:

```text
full-repo-test-matrix
```

## Safety policy

The matrix defaults to safe test mode:

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

No live outbound should run from this matrix.
