# Enterprise Ready

## Definition
Dealix is enterprise-ready when every client-pilot gate passes under:
- multi-tenant workloads (per-tenant isolation in DB + cache)
- Postgres-backed persistence (no SQLite in prod)
- control surfaces visible in UI (admin / approvals / audit log)
- CI release blocker on the verification scripts in `scripts/`
- live-send safety: every external action gated by approval + policy + audit
  (see `docs/governance/AGENT_KILL_SWITCH.md`)

## Owner
Founder + on-call engineer.

## Cadence
- **Per release:** `dealix-everything` and `dealix-production-certification` workflows must be green.
- **Weekly:** founder runs `make audit` locally and reviews `docs/ops/DEALIX_FINAL_READINESS_REPORT.md`.

## Source of truth
- `dealix_manifest.yaml` (what must exist and be wired)
- `scripts/verify_everything.py` (the judge)
- `.github/workflows/dealix-everything.yml` (the enforcer)

## Current required checks

| # | Command                                                              | What it asserts                                       |
|---|----------------------------------------------------------------------|-------------------------------------------------------|
| 1 | `make everything`                                                    | Every manifest layer is PASS                          |
| 2 | `make production-certification`                                      | Above + frontend builds + no banned claims            |
| 3 | `bash scripts/verify_enterprise_control_plane.sh`                    | Legacy control-plane suite (kept for backward compat) |
| 4 | `python scripts/verify_railway_readiness.py`                         | Container + /healthz + predeploy gated correctly      |
| 5 | `python scripts/verify_live_send_safety.py`                          | No live-send path bypasses the approval gate          |

## Failure mode
A failing gate **blocks the release**. CI surfaces the exact failing layer and the file/keyword that's missing. Do not bypass; fix the underlying file and re-run.

## Recovery path
1. Read the CI log — `verify_everything.py` names the failing layer and reason.
2. Fix the file (add the missing keyword, fill the placeholder, wire the route).
3. Re-run `make everything` locally before pushing.
4. If a gate must be temporarily suppressed, open an explicit issue tagged `release-block-override` and require founder sign-off; never silently disable.
