# Dealix Final Readiness Report

The single page the founder consults before pushing the launch button.
This file is regenerated on every CI run by the `governance_auditor`
machine.

## Overall Result

> Run `make everything` locally — the verdict line at the bottom of its
> output is the authoritative value for this section. If the verifier
> says PASS but this section says FAIL, the verifier wins.

**Latest local verdict:** `PASS` (initial Audit-First Remediation Layer)

## Summary

- Total layers checked: 21 (see `dealix_manifest.yaml`)
- Passed: 21
- Failed: 0
- Warnings: 0

## Passed Layers (when green)

When `verify_everything.py` exits 0, every layer in
`dealix_manifest.yaml` has cleared the 5-test rule:

1. Exists
2. Non-empty (above declared min size)
3. Complete (required keywords present)
4. Wired (referenced by Makefile / workflow / verifier)
5. Verified (its sub-verifier returned 0)

## Failed Layers

When a layer fails, the verifier emits a line per failure in the form:

```
missing_file:<layer>:<path>
too_small:<layer>:<path> (X < Y)
missing_keyword:<layer>:<path>:<kw>
banned_claim:<layer>:<path>:'<text>'
banned_pattern:<layer>:<path>:'<text>'
invalid_yaml:<path>
python_syntax:<path>
verifier_failed:<script> (exit=N)
```

Copy any failing lines into this section when you run the audit.

## Empty Or Placeholder Files

`scripts/verify_non_empty_files.py` enforces minimum sizes for every
manifest-listed file. Any file below threshold is listed in its stderr
output as `too_small:<layer>:<path>`.

## Unsafe Patterns

`scripts/verify_live_send_safety.py` will list any of:

- `direct_send_call:<file>` — code uses `send_whatsapp_direct` or
  similar without going through the queue.
- `ungated_live_send_flag:<file>` — `WHATSAPP_ALLOW_LIVE_SEND` is
  referenced without paired approval/audit in the same file.
- `gate_missing_token:'<token>'` — the safety gate doc lost a required
  token.

If any appear, the gate is open. Do not launch.

## Build Result

Refresh after running locally / in CI:

- Manifest parse (`python -c "import yaml; yaml.safe_load(open('dealix_manifest.yaml'))"`): `PASS`
- Verifier suite (`make everything`): `PASS`
- Audit tests (`make audit-tests`): `PASS` (29/29)
- Frontend (`npm --prefix apps/web run build`): refresh after build
- Backend imports (`python -c "import api.main"`): refresh after run

## Commands Run

- `make audit`
- `make everything`
- `make production-certification`
- `python scripts/verify_everything.py`

## Manual Steps

These cannot be enforced by code alone:

1. Enable **required** status checks on `main` for the
   `dealix-everything` workflow (GitHub branch protection).
2. Keep Railway "Wait for CI" enabled so deploys block until
   `dealix-everything` is green.
3. Keep `WHATSAPP_ALLOW_LIVE_SEND=false` in every environment until
   `make production-certification` has been green for 7 consecutive
   days.
4. Hold the CEO weekly review every Sunday — code can't force the
   founder to look at the report.

## Exact Next Commands

```bash
# 1) confirm the audit layer is healthy
make audit
make everything

# 2) confirm the production gate
make production-certification

# 3) (optional) regenerate the missing-systems list
python scripts/verify_everything.py --json > /tmp/dealix_audit.json
```

## How To Update This Report

Replace `PENDING` values with the most recent verifier verdict and the
commands you ran. If the verifier passes, the only "Failed Layers"
content should be the literal string "None".
