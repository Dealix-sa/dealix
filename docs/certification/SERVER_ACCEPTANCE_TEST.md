# Server Acceptance Test

## Purpose

Verify that the connected server actually runs Dealix workers and produces
current operating outputs — not just that files exist.

## Required Artifacts (under `$PRIVATE_OPS/runtime/`)

- `sales_cockpit.md` — updated within 48h (target 24h once cadence stable)
- `approval_center.md` — updated within 48h
- `distribution_command_center.md` — updated within 48h
- `strategic_stoplight.md` — updated within 48h

## Required Discipline

- Worker logs under `$PRIVATE_OPS/logs/*.log` contain no `Traceback` lines.
- `$PRIVATE_OPS` exists **outside** the repository.
- No row in `$PRIVATE_OPS/outreach/outreach_queue.csv` has
  `send_status=sent` while `approval_status!=approved`.

## Pass

Server is operational. Outreach scaling is allowed (within the limits
governed by the Revenue Factory Acceptance Test).

## Fail

Do not scale outreach until fixed. The orchestrator (`certify_dealix_os.py`)
returns non-zero and `ceo_verification_brief.md` flags the constraint.

## Script

`scripts/verify_server_runtime.py --private-ops $PRIVATE_OPS`

When run under CI (`CI=true`), private-ops assertions are skipped and the
script verifies only the surface contract (script imports, args).
