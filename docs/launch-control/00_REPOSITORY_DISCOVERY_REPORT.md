# 00 — Repository Discovery & Architecture Audit

> **Scope:** `Dealix-sa/dealix` — pre-flight audit for the **Dealix Full Startup Company OS V5**.
> **Date:** 2026-06-04 · **Branch:** `claude/dealix-full-startup-company-os-v5-NFrH1`
> **Rule of the build:** _AI drafts, analyzes, scores, ranks, recommends, prepares. Founder reviews, approves, sells, sends manually, signs off. The system never sends externally._

---

## 1. Current architecture (as found)

| Area | Finding | Status |
|------|---------|--------|
| Backend | `api/` — FastAPI app, 120+ routers incl. `api/routers/commercial.py` (diagnostic→pilot→proof→payment→upsell). | Ready |
| Business logic | `dealix/commercial/`, `dealix/payments/` (Moyasar, sandbox by default), `auto_client_acquisition/`, `autonomous_growth/`, `core/`. | Ready |
| Web | `apps/web/` — **Next.js 15.1.3 / React 19 App Router**, 21 existing routes (`value-engine`, `safety`, `approvals`, `go-to-market`, `status`, `ar/*` …). Build: `npm run verify` = `typecheck && build`. | Ready, extend |
| Legacy frontend | `frontend/` — older Next.js dashboard. | Leave |
| Docs | `docs/` — **218 existing doc directories** (constitution, data_os, governance_os, proof_os, value_os, capital_os, sales_os, delivery_playbooks, operating_finance, partners …). | Extend/merge |
| Scripts | `scripts/` — **243 Python scripts** + shell/ps1 (commercial expansion, launch readiness, verifiers, founder digests). | Extend, do not duplicate |
| Workflows | `.github/workflows/` — 50+ workflows (CI, security, codeql, daily/weekly founder ops, lighthouse, playwright). | Add 5 V5 workflows |
| Tests | `tests/` — large pytest suite (unit/integration/regression). | Add V5 tests |
| Make | `Makefile` — `env-check`, `api-contract-check`, `security-smoke`, `prod-verify`, `test`, `v5-verify`, `v10-verify`. | Reuse |
| Deploy | Railway (`railway*.toml`), Vercel/Pages (`deploy-pages.yml`), Docker (`Dockerfile*`, `docker-compose*`). | Leave |

## 2. What is ready
- Commercial chain endpoints, payments (sandbox), AR/EN content templates (`data/templates/`).
- Mature CI/security tooling: `.gitleaks.toml`, `.secrets.baseline`, `security-smoke`, codeql.
- A working Next.js marketing/app surface with bilingual `ar/` routes.

## 3. What is missing (V5 gap)
- A **single, named V5 company-OS doc tree** spanning all 24 functions with consistent doctrine.
- A **review-only 400+/day Draft Factory** with explicit `send_allowed=false / external_send_blocked=true / requires_founder_approval=true / no_auto_send=true` on every record.
- **Top-level verifiers** `startup_os_verify.py` and `final_launch_control_verify.py` that gate the whole company OS.
- A **secret-and-risk scan** dedicated to the V5 outputs/artifacts.
- **Public launch site pages** for the first 5 verticals + commercial/pricing/trust/launch.
- A consolidated **Evidence Pack** + GO/NO-GO.

## 4. Duplication risk — decisions per area
| Existing | V5 action | Why |
|----------|-----------|-----|
| `scripts/run_commercial_expansion.py`, `generate_commercial_content_pack.py` | **Leave** + reference | Different concern (content packs); V5 adds review-only *draft factory*. |
| `scripts/launch_readiness_check.py`, `verify_commercial_launch_ready.py` | **Extend via** `commercial_launch_readiness.py` (V5 thin wrapper, additive) | Avoid breaking existing CI. |
| `docs/company-os/`, `docs/company_os/`, `docs/company/` | **Merge** under canonical `docs/company-os/` (V5) | Three near-duplicates exist; V5 standardizes. |
| `docs/sales-kit/`, `docs/20_sales_os/`, `docs/29_sales_os/` | **New** `docs/sales-os/` references them | Keep historical; V5 is the operating index. |
| `.github/workflows/*` (50+) | **Add 5** clearly-namespaced V5 workflows | No overwrite of existing automation. |

## 5. External-send risk review
- Payments default to **sandbox** (`MOYASAR_LIVE_MODE` gated). No change.
- No V5 file introduces SMTP, WhatsApp, LinkedIn automation, scraping, or auto-submit.
- All V5 GitHub Actions are **`permissions: contents: read`, artifact-only, no secrets, no external network sends.**
- Draft Factory writes **local artifacts only**; every draft carries `external_send_blocked=true`.

## 6. Stale references found
- `README.md` / `SECURITY.md` / `CHANGELOG.md` reference **`github.com/VoXc2/dealix`** (old org). **Action:** update README clone URL + CI badge to `Dealix-sa/dealix`. (SECURITY.md advisory link left to a separate security PR to avoid scope creep — flagged in Security/Trust OS report.)

## 7. Execution decision per region
| Region | Decision |
|--------|----------|
| Company / Product / Engineering OS | **Create** (new canonical V5 index) |
| Site Launch | **Extend** `apps/web` + add checker |
| Commercial / Sales / Marketing / Media / Ads | **Create** V5 index, **reference** existing assets |
| Draft Factory / RevOps / Delivery / Support | **Create** working scripts + docs |
| Finance / Legal / Security / Analytics / AI-Evals | **Create** templates + verifiers (templates ≠ legal/financial advice) |
| People / Partnerships / Investor / Operations | **Create** readiness docs |
| Go-Live / Launch Control | **Create** + top-level verifiers |

**Conclusion:** V5 is **additive and non-destructive**. It introduces a named, verifiable company-OS layer on top of a mature codebase without touching deployment, secrets, or `main`.
