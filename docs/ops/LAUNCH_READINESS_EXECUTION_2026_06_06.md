# Launch Readiness Execution — 2026-06-06 / تنفيذ جاهزية الإطلاق

> Honest, evidence-based snapshot produced while driving the comprehensive
> launch pass. No inflated status. "Green" means a check was run locally and
> passed; "external" means it can only be completed by the founder in a
> provider dashboard.
>
> تقرير صادق قائم على الأدلة. "أخضر" = فحص شُغّل محليًا ونجح. "خارجي" = لا يمكن
> إكماله إلا من المؤسس في لوحة المزوّد.

---

## 1. What was fixed in this pass / ما أُصلح في هذه الجولة

The repository's branch was identical to `main`, and `main`'s CI was **not
clean** (latest runs `cancelled` / `failure`). Root causes were found and
fixed — all in the **doctrine / governance perimeter** (the non-negotiables
enforced in code), plus one real frontend endpoint drift:

| # | Failing gate | Root cause | Fix | Doctrine tie |
|---|---|---|---|---|
| 1 | `test_landing_forbidden_claims` + `test_v7_no_guaranteed_claims` | 15 landing pages carry the **mandatory bilingual value disclaimer** ("Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة") and policy-negation copy ("صفر cold WhatsApp", "لا scraping"), but were never added to the per-file allowlist | Added per-file allowlist entries with a new `DISCLAIMER` reason code; removed one stale `نضمن` entry (trust-center page was redesigned) | NO_FAKE_CLAIMS / NO_GUARANTEED_OUTCOMES |
| 2 | `test_no_linkedin_<token>_string_anywhere` (repo-wide LinkedIn-automation token guard) | A test-inventory doc names the guard test itself | Allowlisted the doc path | NO_LINKEDIN_AUTO + NO_SCRAPING |
| 3 | `test_v7_secret_leakage_guard::test_no_secret_prefix_outside_allowlist` | 35 files legitimately reference the live-secret / PAT / Google-API-key **prefixes** in secret-scan regexes, redaction modules, prefix `.startswith` checks, env placeholders, and runbooks — none are real secrets (verified line-by-line) | Allowlisted all 35 with one-line reasons | NO_PII_IN_LOGS / secret hygiene |
| 4 | `test_landing_no_railway_refs_v13` | 3 landing pages used the legacy `/healthz` endpoint name; the canonical liveness route is `/health` and the deep check is `/health/deep` (both real, schema-included; `/healthz` is an unschema'd alias) | Migrated `architecture.html`, `launch-status.html`, `system-status.html` to `/health` + `/health/deep` (verified live via in-process smoke) | — |

**Result:** the full doctrine-guard battery now passes — **137 passed, 1
skipped (env), 1 xfail (tracked debt)**. No guard was disabled; only
compliant-context references were allowlisted.

---

## 2. CI gates verified green locally / بوّابات CI التي تأكّدت محليًا

| Gate | Command | Result |
|---|---|---|
| Doctrine guards (non-negotiables) | `pytest tests/test_no_*.py tests/test_v7_no_*.py …` | ✅ 137 passed |
| Single Alembic head | `python scripts/check_alembic_single_head.py` | ✅ single head (013) |
| Service readiness matrix | `python scripts/verify_service_readiness_matrix.py` | ✅ 32 services, 8 live |
| Service readiness JSON export | `python scripts/export_service_readiness_json.py` + `git diff` | ✅ no diff |
| SEO audit | `python scripts/seo_audit.py` + `git diff` | ✅ no diff (76 pages) |
| Security smoke | `python scripts/security_smoke.py` | ✅ exit 0 |
| Env contract | `python scripts/check_env_contract.py` | ✅ OK |
| In-process API smoke | `python scripts/smoke_inprocess.py` | ✅ boots; `/health` 200; pricing/brief/launch-report 200 |

---

## 3. Full test suite — honest state / الحالة الكاملة لمجموعة الاختبارات

`pytest -n auto` over **4726 tests**: **4628 passed**. The remainder
categorized below (this is the pre-existing state of `main`, not a regression
from this pass — only test allowlists + 3 landing pages were touched):

| Category | Count | Nature | Action |
|---|---|---|---|
| Parallel-isolation flakiness | ~33 | Pass when run serially (e.g. all 22 `test_hermes_system` pass alone; shared module state collides under `-n auto`) | **Test infra debt** — needs per-worker isolation / `pytest-xdist` grouping. Not a product bug. |
| Environment-gated (no Postgres) | ~20 | `ConnectionRefusedError ('127.0.0.1', 5432)` — durable_workflow, referral_program, pricing_plans, sector_intel, revenue_learning_loop, delivery_sprint, tenant_theming, founder_commercial_digest | **Pass in CI** (Postgres service); cannot run in this sandbox. |
| Shell-verifier meta-tests | 5 | `*_verify_script` run shell verifiers that exit 1 (working-tree / tool-state sensitive) | Re-check post-merge on a clean tree. |
| Real drift — needs a product decision | ~9 | billing free-tier (`amount_halalas == 0` for rung-0 Free Diagnostic vs. the "all plans positive" safety invariant), seo advisory-exemption set, auth-flow env, WhatsApp prod-signature, checkout routing, internal-link guard, article-13 guard | **Founder/PM decision required** — several touch money & safety; not safe to guess unilaterally. See §5. |

> Why this matters: the billing failures are a **money-safety invariant**
> ("no plan charges 0 halalas") colliding with the **doctrine rung-0 Free
> Diagnostic = 0 SAR**. Resolving it means deciding whether the free tier
> belongs in the chargeable `PLANS` map or in a separate non-chargeable
> catalog. That is a deliberate decision, not a test tweak.

---

## 4. External / founder-only launch steps / خطوات الإطلاق الخارجية

These **cannot** be done from the repo or by an agent (doctrine: never charge
a customer, never send external without approval, Moyasar live is
founder-flipped only). Tracked as issues #467–#471.

- [ ] Set production secrets (Railway/host) per `docs/ops/PRODUCTION_SECRETS_CHECKLIST.md`.
- [ ] Generate/commit `apps/web/package-lock.json` if regenerating web deps.
- [ ] Verify live DNS + TLS for `api.dealix.me` in the DNS/host dashboard.
- [ ] Moyasar: complete KYC, then `python scripts/moyasar_live_cutover.py` (founder-only).
- [ ] Verify payment + webhook dashboards (Moyasar) with real credentials.
- [ ] Fill `data/warm_list.csv`, then `python scripts/warm_list_outreach.py` (drafts only — approval-gated).
- [ ] Run GitHub Actions: CI, Security, Production Smoke; attach evidence before closing #467–#471.

---

## 5. Recommended next decisions / القرارات التالية الموصى بها

1. **Billing free-tier (P0, money-safety):** decide free-tier placement, then
   align `tests/test_billing_amounts.py` + `tests/test_billing_moyasar_safety.py`.
2. **Test isolation (P1):** group or isolate the `-n auto` collision set so CI's
   coverage gate can pass deterministically (this is the real reason `main`'s
   CI shows `cancelled`).
3. **Open-PR triage (P2):** 20 open PRs — mostly overlapping draft "Wave 7/8 /
   Company OS / launch" branches. Consolidate or close to reduce drift.

---

_Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة._
