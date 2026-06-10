# Dealix — Launch Blockers Log

> Record every verification failure here. Do not ignore failures. Do not delete entries — resolve them.
> Updated by the launch verification run (Phase 9).

## How to use
- Each run of the verify scripts / build / lint / test appends its result.
- A blocker stays `OPEN` until fixed and re-verified.

## Verification run — 2026-06-05 (Wave 3 native reconstruction)

| Check | Result | Note |
|---|---|---|
| `verify_dealix_positioning.py` | ✅ PASS | 29 files scanned, claims clean (negation-aware) |
| `verify_dealix_cta_map.py` | ✅ PASS | 4 page bodies audited, one CTA each |
| `verify_dealix_module_status.py` | ✅ PASS | 32 services, all valid status (LIVE=8, TARGET=24) |
| `verify_dealix_growth_assets.py` | ✅ PASS | 5 sectors, 10 answers, routing valid |
| `verify_dealix_launch_readiness.py` | ✅ PASS | **VERDICT = PRIVATE_LAUNCH_READY** |
| `frontend/scripts/verify_wave3_content.mjs` | ✅ PASS | 21 files scanned |
| `npm run typecheck` (frontend) | ✅ PASS | tsc --noEmit clean |
| `npm run build` (frontend) | ✅ PASS | all Wave 3 routes compiled |
| `make env-check` | ✅ PASS | backend + frontend env contract OK |
| `scripts/security_smoke.py` | ⚠️ FAIL (pre-existing) | see OPEN-1 below |

## Open blockers

### OPEN-1 — `security_smoke.py` flags 17 fake-secret patterns (PRE-EXISTING)
- **Status:** OPEN, pre-existing — **not introduced by Wave 3.**
- **Detail:** `scripts/security_smoke.py` exits 1 because 17 files contain `sk_live_…`, `ghp_…`, `github_pat_…`, or `AKIA…` shaped strings. All are **existing test fixtures and docs** (e.g. `tests/test_agent_observability_integration.py`, `tests/test_finance_os_no_live_charge_invariant.py`, `docs/ops/GO_LIVE_CHECKLIST_AR.md`, `docs/launch/DEALIX_LAUNCH_NOW_BUNDLE.md`). None of the Wave 3 files (`scripts/verify_dealix_*`, `frontend/src/**/wave3`, `docs/00_platform_truth`, `sales/`, `customers/_template/`) are implicated.
- **Recommended fix (out of Wave 3 scope):** either replace the fixture strings with clearly non-matching placeholders (e.g. `sk_live_REPLACE_ME`), or add the test fixtures to the smoke scanner's allowlist. Decide with the founder before touching test fixtures.

## Notes / known limitations (not blockers)
- `/pricing` still renders inside the authenticated `AppLayout` shell. The CTA map declares `/pricing → Start Command Sprint`; swapping it to the public `MarketingShell` is deferred (no gate requires it, and the shell swap risks the build). Tracked for a follow-up.
- Public navigation (`PublicLaunchShell`) was not extended with the new Platform / Business OS / Industries / Security / Tools links to avoid destabilizing the shared shell; new pages are reachable directly and via internal links. Tracked for a follow-up.
- Legacy `docs/sales-kit/dealix_onepager.md` contains positioning that contradicts `PLATFORM_TRUTH.md` (auto-reply "without human intervention", CRM framing). It is outside the Wave 3 scan scope but should be reconciled. Tracked for a follow-up.
- `make prod-verify` / `npm run test` were not run to green in this container (require services / are heavier); run them in CI before any public launch.

## Resolved blockers
_(none yet)_
