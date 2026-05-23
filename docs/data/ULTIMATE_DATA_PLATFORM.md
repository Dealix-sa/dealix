# Ultimate Data Platform

The data platform contract is "every business decision can be replayed
from disk." This is what makes Dealix auditable.

## Layers

| Layer | Store |
|---|---|
| Source of truth (today) | CSV + JSON under `DEALIX_PRIVATE_OPS` |
| Source of truth (future) | Postgres (see `POSTGRES_PRIMARY_MODE.md`) |
| Decision log | `<private_ops>/trust/approval_decisions.csv` |
| Audit log (HTTP) | `api/middleware/http_stack.py::AuditLogMiddleware` |
| Public exports | `data/` (only after founder approval) |

## Data quality

* Every CSV has a fixed header. Bootstrap creates them with the right
  fields. Workers MUST write all fields (empty values are OK).
* `scripts/verify_prompt_output_quality.py` scans for accidental secret
  leaks. Run it as part of pre-commit.
* `scripts/db_index_audit.py` (existing) covers Postgres index hygiene
  once we move to phase 2.

## Backup + restore

* Backup target: `s3://dealix-private-ops-backups/<yyyy-mm-dd>.tar.gz`
  (configured outside the repo).
* Restore = untar to a fresh path + `export DEALIX_PRIVATE_OPS=...`.
* Restore drills are scheduled monthly (handled by a separate Founder
  Cron — out of scope for this commit).
