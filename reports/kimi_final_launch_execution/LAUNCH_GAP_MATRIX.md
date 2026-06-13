# LAUNCH GAP MATRIX

## P0 — Blocks Launch 🔴

| # | Gap | Evidence | File Path | Proposed Fix | Risk | Acceptance Command |
|---|-----|----------|-----------|--------------|------|-------------------|
| P0-1 | **Two frontend directories** — `frontend/` and `apps/web/` both have Next.js 15.1.3 with overlapping pages | Both dirs have active code, similar pages (war-room, pricing) | `frontend/`, `apps/web/` | Consolidate unique pages from `apps/web/` into `frontend/`, mark `apps/web/` as deprecated | High — duplicate maintenance, divergent codebases | `cd frontend && npm run build` passes |
| P0-2 | **60 GitHub workflows** — many founder-automation workflows may be noisy/unmaintained | 40+ scheduled/business workflows that may fail silently | `.github/workflows/` | Audit each workflow: mark required vs optional, disable broken ones | Medium — CI noise, false confidence | `.github/workflows/ci.yml` passes cleanly |
| P0-3 | **2,754 doc files with duplication** — 44 numbered dirs with 30+ duplicates | `docs/14_*` appears 3x, `docs/15_*` 3x, `docs/16_*` 3x, 01-13 appear 2x | `docs/` | Create canonical doc index, mark duplicates, consolidate | Low — docs don't break prod, but confuse agents | Doc count < 500 after consolidation plan |
| P0-4 | **Archive files in repo root** — .zip and .tar.xz files committed | 4 archive files totaling ~13MB in git history | `*.zip`, `*.tar.xz` | Add to `.gitignore`, remove from tracking (keep in releases) | Low — repo bloat | Archives not in `git ls-files` |
| P0-5 | **Duplicate API routers** — both flat routers and domain aggregators may overlap | `api/routers/*.py` (172 files) + `api/routers/domains/*.py` | `api/routers/` | Verify domain aggregators import all needed routers; remove unreferenced flat imports | Medium — route conflicts | `python -c "from api.main import app; print(len(app.routes))"` |

## P1 — Blocks Enterprise Credibility 🟡

| # | Gap | Evidence | File Path | Proposed Fix | Risk | Acceptance Command |
|---|-----|----------|-----------|--------------|------|-------------------|
| P1-1 | **No unified ENVIRONMENT_CONTRACT.md** — env vars scattered across .env.example, .env.railway.example, frontend envs | Multiple env templates with potential conflicts | `.env.example`, `.env.railway.example` | Create unified `docs/ops/ENVIRONMENT_CONTRACT.md` | Medium — misconfig in production | `make env-check` passes |
| P1-2 | **Security workflows claim scanning but may not catch all secrets** | `security.yml`, `agentic-security-gate.yml` exist | `.github/workflows/` | Verify security workflows actually run and catch test secrets | Medium — secret leakage | `make security-smoke` passes |
| P1-3 | **No clear PDPL implementation evidence** — docs exist but code coverage unclear | PDPL docs in `docs/compliance/`, `api/routers/pdpl.py` | `dealix/pdpl/`, `api/routers/pdpl.py` | Verify PDPL endpoints are wired and tested | High — Saudi compliance | `pytest tests/test_pdpl*.py -q` |
| P1-4 | **Moyasar payment integration** — sandbox vs live mode unclear | `dealix/payments/moyasar.py` | `dealix/payments/` | Document sandbox-by-default, add live mode gate | High — accidental charges | `grep -r "MOYASAR_LIVE_MODE" dealix/payments/` |
| P1-5 | **OpenAPI export may drift** — no CI enforcement | `scripts/export_openapi.py`, `scripts/check_openapi_contract.py` | `docs/architecture/openapi.json` | Add CI check for OpenAPI drift | Low — API contract fidelity | `make api-contract-check` passes |
| P1-6 | **Frontend build not verified in CI** — `frontend/` may have build errors | `frontend/package.json` has build script | `frontend/` | Add frontend build to CI or verify locally | Medium — deploy failure | `cd frontend && npm run build` passes |

## P2 — Polish / Scale 🟢

| # | Gap | Evidence | File Path | Proposed Fix | Risk | Acceptance Command |
|---|-----|----------|-----------|--------------|------|-------------------|
| P2-1 | **AGENTS.md has Cursor-specific instructions but not Kimi** | References Claude, Cursor, but no Kimi guidance | `AGENTS.md` | Add Kimi section, update for multi-agent | Low | AGENTS.md references `docs/architecture/DEALIX_FUTURE_FILE_SYSTEM_AR.md` |
| P2-2 | **Token optimizer guides are Cursor/Claude specific** | `token-optimizer/` has 12 guides for Claude | `token-optimizer/` | Make agent-agnostic or add Kimi-specific guides | Low | Token optimizer runs for any agent |
| P2-3 | **README.md and README.ar.md may drift** | Two separate README files | `README.md`, `README.ar.md` | Add sync check or single-source i18n | Low | Both READMEs reference same commands |
| P2-4 | **No automated dead-link checker for docs** | 2,754 docs with internal links | `docs/` | Add link checker to CI (optional) | Low | N/A |
| P2-5 | **Lint drift** — AGENTS.md notes large pre-existing lint drift | `ruff check .` likely has many warnings | Entire repo | Fix critical lint issues, document accepted drift | Low | `ruff check .` has known count |

## Summary
- **P0**: 5 gaps — frontend duplication, workflow noise, doc duplication, archives in repo, router structure
- **P1**: 6 gaps — env contract, security verification, PDPL evidence, payment safety, OpenAPI CI, frontend build
- **P2**: 5 gaps — multi-agent docs, token optimizer i18n, README sync, link checking, lint
