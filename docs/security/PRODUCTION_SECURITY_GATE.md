# Production Security Gate

Production readiness is a separate gate from "sovereign readiness."

## Required for production

1. `DEALIX_INTERNAL_TOKEN` set in the production environment.
2. The internal token rotated within the last 90 days.
3. The private-ops directory backed up to an off-host location.
4. `make sovereign-operating-stack` green on the deploy commit.
5. `make smoke-internal-api` green against the deployed `/api/v1/internal/*`.
6. Branch protection on `main` requires the
   `dealix-sovereign-operating-stack` CI job (see
   [`BRANCH_PROTECTION_REQUIRED_CHECKS.md`](BRANCH_PROTECTION_REQUIRED_CHECKS.md)).
7. The frontend build (`npm --prefix apps/web run build`) succeeded for
   the same commit.

## Not required (but recommended)

* A scheduled restore drill (monthly).
* Operator runbooks for incident response.
* Per-agent kill-switch test (disable + enable from the console).

## Honest claim

This commit does **not** assert production readiness. It asserts
**sovereign readiness** for the internal control surface.
