# Dealix Production Finalization Status

_Last updated: 2026-05-26_

This file separates repository-complete work from items that require external execution in GitHub, the hosting provider, DNS, payment dashboards, or a local package manager.

## Completed in repository

| Area | Status | Evidence |
|---|---|---|
| CI consolidation | Done | `.github/workflows/ci.yml` has one CI workflow with Python and web jobs. |
| Security automation | Done | `.github/workflows/security.yml` adds CodeQL and Dependency Review. |
| Dependency automation | Done | `.github/dependabot.yml` covers pip, npm, GitHub Actions, and Docker. |
| Production smoke automation | Done | `.github/workflows/production-smoke.yml` runs scheduled/manual smoke tests. |
| Env contract validation | Done | `scripts/check_env_contract.py`, `make env-check`. |
| OpenAPI export | Done | `scripts/export_openapi.py`, `make openapi-export`. |
| OpenAPI contract check | Done | `scripts/check_openapi_contract.py`, `make api-contract-check`. |
| Security smoke | Done | `scripts/security_smoke.py`, `make security-smoke`. |
| Production command bundle | Done | `make prod-verify`. |
| Live domain runbook | Done | `docs/ops/DOMAIN_OPERATIONS_RUNBOOK.md`. |
| Production secrets checklist | Done | `docs/ops/PRODUCTION_SECRETS_CHECKLIST.md`. |
| Monitoring matrix | Done | `docs/ops/MONITORING_MATRIX.md`. |
| Incident drill | Done | `docs/ops/LIVE_DOMAIN_INCIDENT_DRILL.md`. |
| Release process | Done | `docs/ops/RELEASE_PROCESS.md`. |
| API policy | Done | `docs/architecture/API_CONTRACT_POLICY.md`. |
| Ownership | Done | `.github/CODEOWNERS`, `docs/ops/OWNERSHIP_MATRIX.md`. |
| Execution backlog | Done | `docs/ops/EXECUTION_BACKLOG.md` and CSV importer. |
| README refresh | Done | `README.md` now points to the real repo and operating commands. |

## Requires external execution

| Item | Why it cannot be completed only by editing repository files | Exact action |
|---|---|---|
| Generate `apps/web/package-lock.json` | Requires running npm dependency resolution against the current package registry. | Run `cd apps/web && npm install --package-lock-only`, then commit `apps/web/package-lock.json`. |
| Confirm GitHub Actions are green | Requires GitHub runner execution. | Open Actions and run CI, Security, and Production Smoke. |
| Set production GitHub secrets | Secrets cannot be inferred or safely committed. | Set `DEALIX_PUBLIC_URL`, `DEALIX_PRODUCTION_BASE_URL`, and any smoke/API keys in repository secrets. |
| Confirm DNS records | DNS provider state is outside the repo. | Confirm `dealix.me` and `api.dealix.me` point to the intended hosts. |
| Confirm TLS renewal | Certificate state is outside the repo. | Check hosting provider TLS and auto-renewal for public/API domains. |
| Confirm payment/webhook dashboards | Provider dashboards are outside the repo. | Verify Moyasar/Calendly/WhatsApp webhook URLs and secrets. |
| Run live production smoke | Requires network access to the real deployment. | Run `make production-smoke PRODUCTION_BASE_URL=https://api.dealix.me`. |

## Recommended final execution order

1. Set GitHub repository secrets:
   - `DEALIX_PUBLIC_URL=https://dealix.me`
   - `DEALIX_PRODUCTION_BASE_URL=https://api.dealix.me`
2. Generate and commit `apps/web/package-lock.json`.
3. Run GitHub Actions: CI, Security, Production Smoke.
4. Run local verification if you have the repo cloned:

```bash
make env-check
make api-contract-check
make security-smoke
make production-smoke PRODUCTION_BASE_URL=https://api.dealix.me
```

5. Verify DNS/TLS in hosting/DNS provider dashboards.
6. Verify payment and webhook provider dashboards.
7. Update `docs/ops/EXECUTION_BACKLOG.md` with any remaining live findings.

## Arabic summary

تم إنجاز كل ما يمكن إنجازه داخل الريبو: CI، security، smoke، env، OpenAPI، runbooks، ownership، release، monitoring. المتبقي لا يمكن تنفيذه من داخل الملفات فقط لأنه يحتاج GitHub Secrets، تشغيل Actions، DNS/hosting dashboard، أو توليد npm lockfile من registry.
