# Dealix Repo Discovery Report

Generated as part of the Audit-First Remediation Layer. This report is
the human-readable mirror of what `scripts/verify_repo_completeness.py`
checks every CI run.

## Purpose

Surface what actually exists in the Dealix repository so "موجود" can
never be claimed without proof.

## Owner

Founder. Auto-refreshed by the `governance_auditor` machine.

## Cadence

- Per CI run.
- Manually refreshable via `make audit`.

## Source of Truth

- `dealix_manifest.yaml`
- `scripts/verify_repo_completeness.py`
- `scripts/verify_everything.py`

## Detected Layout

| Concern | Path |
| --- | --- |
| Manifest | `dealix_manifest.yaml` |
| Backend (FastAPI) | `api/main.py` |
| Backend domain | `dealix/` |
| Customer / ops frontend (Next.js) | `apps/web/` |
| Founder dashboard frontend | `frontend/` |
| Docs root | `docs/` |
| Governance docs | `docs/governance/` |
| AI governance docs | `docs/ai_governance/` |
| Founder docs | `docs/founder/` |
| Trust docs | `docs/trust/` |
| Audit reports | `docs/ops/DEALIX_*_REPORT.md` |
| Policies | `policies/dealix_control_policy.yaml` |
| Registries | `registries/agent_registry.yaml`, `registries/machine_registry.yaml` |
| Evals | `evals/*.yaml` |
| CI workflows | `.github/workflows/` |
| Build | `Dockerfile`, `Makefile` |
| Deploy | `railway.toml`, `railway.json`, `scripts/railway_predeploy.sh` |

## Required Top-Level Files

| File | Purpose |
| --- | --- |
| `dealix_manifest.yaml` | Source of truth for layers |
| `Makefile` | Founder-runnable commands |
| `Dockerfile` | Production container |
| `railway.toml` / `railway.json` | Railway deploy contract |
| `README.md` | Brand + onboarding |
| `scripts/verify_everything.py` | Master verifier |
| `scripts/railway_predeploy.sh` | Pre-deploy migration gate |

## Required Directories

`api`, `apps/web`, `dealix`, `docs`, `docs/ops`, `docs/governance`,
`docs/founder`, `docs/ai_governance`, `docs/trust`, `evals`, `policies`,
`registries`, `scripts`, `tests`, `.github/workflows`.

## Missing / Drift

`scripts/verify_repo_completeness.py` exits non-zero and lists missing
items to stderr. CI surfaces them automatically.

## Verification

```bash
make audit
```

## Next Action

If this list ever drifts from the actual repo, edit
`scripts/verify_repo_completeness.py` *and* update this file in the same
commit.
