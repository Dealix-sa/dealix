# Official Launch Decision — قرار الإطلاق الرسمي

> **Date / التاريخ:** 2026-06-07
> **Scope / النطاق:** Repository launch-readiness decision for `Dealix-sa/dealix`.
> **Authority / المرجعية:** This document consolidates the launch verdict. The
> binding truth labels live in [`docs/phase-e/00_GO_NO_GO.md`](../phase-e/00_GO_NO_GO.md)
> (enforced by `tests/test_truth_labels_v11.py`); this file does **not** override them.
> **Process / المسار:** No direct pushes to `main`. Every release goes through
> **Launch Branch → PR → GitHub Actions → Review → Founder Approval → Merge → Deploy**.

---

## 1. Verdict — الحُكم

### ✅ Private Launch: **GO**  ·  ⛔ Public Launch: **NO-GO**

- **Private Launch GO** — warm intros + free Diagnostic + manual/test-mode paid pilot are authorized today.
- **Public Launch NO-GO** — no public revenue/ROI claims, no live send, no live charge, no cold WhatsApp, until production evidence proves otherwise via a coordinated truth-label PR.

**بالعربية:** الإطلاق **الخاص** مسموح الآن (تعريفات دافئة + تشخيص مجاني + تجربة مدفوعة يدويًا/test-mode). الإطلاق **العام** ممنوع حتى يثبت دليل إنتاجي العكس عبر PR منسّق يقلب اللِيبلات.

### Truth labels (source of truth) — اللِيبلات المُلزِمة

From [`docs/phase-e/00_GO_NO_GO.md`](../phase-e/00_GO_NO_GO.md):

| Label | Value | Meaning |
|---|---|---|
| `PRODUCTION_READY` | `yes` | `/health` 200 + valid `git_sha`; smoke ≥ 27/28 |
| `PHASE_E_GO` | `yes` | Founder may begin warm intros today |
| `FIRST_CUSTOMER_READY` | `yes_for_warm_intro_and_diagnostic` | Diagnostic + draft ready; pilot quote-only |
| `PAID_PILOT_READY` | `yes_manual_payment_only` | Manual / test-mode payment only (no live charge) |
| `PAID_BETA_READY` | `no_until_payment_or_written_commitment` | Block public "PAID_BETA" claims |
| `REVENUE_LIVE` | `no_until_real_money_or_signed_commitment` | **No public revenue/ROI claims** |
| `LIVE_SEND_READY` | `no` | **DRAFT-ONLY** content |
| `LIVE_CHARGE_READY` | `no` | TEST-MODE / MANUAL only |
| `LINKEDIN_AUTOMATION_READY` | `no` | Out of scope |
| `COLD_WHATSAPP_READY` | `never` | **Hard-pinned — never** |

> Flipping a label requires a `chore(go-no-go): flip <LABEL>` PR editing **both** the
> doc and `tests/test_truth_labels_v11.py`, with evidence. `LIVE_SEND_READY` /
> `LIVE_CHARGE_READY` need founder + safety review; `COLD_WHATSAPP_READY` is never flipped.

---

## 2. The 11 Non-Negotiables — الثوابت الـ11

Source: `auto_client_acquisition/trust_os/trust_pack.py` · Enforcement:
`auto_client_acquisition/safe_send_gateway/doctrine.py` (raises → HTTP 403).

1. No scraping (web/email/LinkedIn). 2. No cold WhatsApp. 3. No LinkedIn automation.
4. No fake/un-sourced claims. 5. No guaranteed sales outcomes. 6. No PII in logs.
7. No source-less answers (Source Passport required). 8. No external action without approval.
9. No agent without identity. 10. No project without Proof Pack. 11. No project without Capital Asset.

These are enforced by tests (`tests/test_doctrine_guardrails.py`,
`tests/test_commercial_doctrine.py`, `tests/test_truth_labels_v11.py`) and **must never be
disabled or weakened** to pass a gate.

---

## 3. Code blockers — العوائق البرمجية

CI authority is **GitHub Actions on the PR**, not any local run. Current honest state:

| Blocker | Status | Owner |
|---|---|---|
| Doctrine/governance guard gates green | **Open** → closed by **PR #650** (allowlists compliant disclaimer/negation copy; no guard disabled) | PR review |
| `make doctor` / `prod-verify` red via `security-smoke` (pre-existing fixture-secret false-positives + `.env.*.example`) | **Open** → addressed by #650 (`test_v7_secret_leakage_guard` allowlist) + #649 note | PR review |
| CI `Trivy filesystem scan` red — stale `aquasecurity/trivy-action@0.24.0` no longer resolves upstream (pre-existing on `main`, **not** from this PR) | **Open** → closed by **PR #638** (bumps to `@master` + `skip-files` false-positives; also softens the Gitleaks license gate) | PR review |
| OpenAPI contract has no committed baseline (`api-contract-check` short-circuits) | **Open** → closed by **PR #649** (commits `docs/architecture/openapi.json`, enables real breaking-change diff) | PR review |
| Official verdict script returns PASS after code-blocker fixes | **Open** → closed by **PR #648** (`DEALIX_OFFICIAL_LAUNCH_VERDICT=PASS`) | PR review |
| Claude Code review workflow + `CLAUDE.md` present | **Open** → closed by **PR #638** (needs `ANTHROPIC_API_KEY` secret) | Founder + PR review |
| `.env.example` missing `JWT_SECRET_KEY` (app fails-fast in prod) | **Closed in this PR** — key added to template + `REQUIRED_KEYS` | this PR |
| Stale `VoXc2/dealix` repo URLs (P0) | **Closed in this PR** — 37 operational/user-facing files retargeted to `Dealix-sa/dealix` | this PR |

### Open launch PRs — مسار الدمج الموصى به

All four are **draft**, branch from the same `main@7bd43c3`, are **independent (not stacked)**,
and CI is `pending/unstable` (none green yet). The only conflict surface is **#648 ↔ #650** on
**two files**: `tests/test_landing_forbidden_claims.py`, `tests/test_no_linkedin_scraper_string_anywhere.py`.

| PR | Branch | Essence |
|---|---|---|
| **#650** | `claude/comprehensive-implementation-launch-dPBAE` | Greens doctrine/governance gates + real `/healthz→/health` fix in 3 landing pages |
| **#648** | `claude/comprehensive-implementation-launch-iLABb` | Closes verdict code blockers + artifacts (`daily_packets.yaml`, `frontend/.env.local.example`) |
| **#649** | `claude/comprehensive-implementation-launch-1R1XC` | Productization: `openapi.json` baseline + PDPL erasure tests + service pages + 90-day plan |
| **#638** | `claude/github-ai-integration-setup-iYLS8` | `claude-code.yml` + `CLAUDE.md` (also touches lockfiles) — needs `ANTHROPIC_API_KEY` |

**Recommended order (founder executes via the gate — not automated):**
1. **#650 first** — most complete gate-greening; establishes the allowlist superset for the two shared test files.
2. **#648 second** — rebase on #650; resolve the two shared files by taking #650's allowlist as the base + #648's unique additions; keep #648's unique artifacts.
3. **#649** — disjoint; can merge in parallel. Adds the OpenAPI baseline that makes `api-contract-check` meaningful + PDPL tests.
4. **#638** — anytime after review + adding the `ANTHROPIC_API_KEY` secret + confirming least-privilege `permissions:` and that the lockfile changes are intentional. Also repairs `repository-hardening.yml` (stale `trivy-action@0.24.0` → `@master`; Gitleaks license gate), which currently reds the **Trivy** + **Gitleaks** scans on every PR.

---

## 4. Founder-only blockers — عوائق المؤسس فقط

These cannot be done from the repo (doctrine: never charge a customer, never send external
without approval, Moyasar live is founder-flipped only). They are **not** code blockers.

### 4.1 Production secrets — use the **canonical** names from `.env.example`

| Canonical key | Notes |
|---|---|
| `ENVIRONMENT`, `LOG_LEVEL` | core |
| `APP_SECRET_KEY` | 64-byte hex; app fails-fast on placeholder |
| `JWT_SECRET_KEY` | 64-byte hex; app fails-fast if unset / < 32 chars **(now in the template)** |
| `DATABASE_URL`, `APP_URL`, `CORS_ORIGINS` | core |
| `API_KEYS` | comma-separated; app fails-fast if empty in prod |
| `ADMIN_API_KEYS` (+ optional `DEALIX_ADMIN_API_KEY` alias) | `/api/v1/admin/*` |
| `MOYASAR_SECRET_KEY` (`sk_live_…`), `MOYASAR_WEBHOOK_SECRET` | **[REVENUE]** — founder-only live cutover |
| `ANTHROPIC_API_KEY` (+ optional `HERMES_API_KEY`) | LLM |
| `OPENAI_API_KEY` | optional LLM |
| `POSTHOG_API_KEY`, `POSTHOG_HOST` | analytics |
| `SENTRY_DSN` | optional observability |
| `GMAIL_CLIENT_ID/SECRET/REFRESH_TOKEN/SENDER_EMAIL` | email is **Gmail OAuth** (no SMTP password) |

**Name corrections vs. common assumptions:** `OPENROUTER_API_KEY` — **not used**;
`SMTP_PASSWORD` — **not used** (Gmail OAuth); `FRONTEND_URL` — use `NEXT_PUBLIC_API_URL` /
`NEXT_PUBLIC_SITE_URL` (in `apps/web`); `PRODUCTION_BASE_URL` — a **Makefile variable**, not an env var.

### 4.2 Other founder-only steps
- DNS/TLS for `dealix.me` / `api.dealix.me` (and the GitHub Pages `VoXc2.github.io` reference in `docs/ops/DEALIX_ME_FRONTEND_DNS_RAILWAY_AR.md` — confirm/replace if org Pages is used).
- Moyasar **KYC + live key cutover** + payment dashboards.
- Warm-list fill + first real Diagnostic / signed commitment.
- Hard-pinned labels stay: `LIVE_CHARGE_READY=no`, `COLD_WHATSAPP_READY=never`.

---

## 5. Launch checklist (gates) — قائمة بوابات الإطلاق

**Canonical local gates:** `make doctor` (env-check + alembic-heads + security-smoke) and
`make prod-verify` (env-check + security-smoke + api-contract-check + dependency-inventory +
release-manifest + v5-verify).

**CI checks that must be green before merge** (`ci.yml`, `security.yml`):
- Python quality, tests, readiness · Next.js web verify · Frontend verify
- Railway Docker image builds (API + worker + watchdog + web) · CodeQL · Dependency Review

**Live (founder/CI, needs running service):** `make production-smoke PRODUCTION_BASE_URL=https://api.dealix.me`,
then `curl /health` and `GET /api/v1/pricing/plans`.

### Honest gate results from this session (sandbox: Python 3.11, no app deps)
| Gate | Result | Note |
|---|---|---|
| `make env-check` | ✅ **PASS** | incl. the new `JWT_SECRET_KEY` / `API_KEYS` contract |
| `make security-smoke` | ❌ FAIL | **pre-existing** fixture-secret false-positives (`sk_live_/ghp_/AKIA/github_pat_` in `tests/*`, docs) + committed `.env.*.example`; **not introduced by this PR** — same residual #649/#650 document. Not a hard gate in `ci.yml`/`security.yml`. |
| `make api-contract-check` | ⚠️ needs deps | `ModuleNotFoundError: fastapi` in sandbox; runs in CI (no baseline on this branch ⇒ trivial pass). |
| `make test` / `lint` / `type-check` | ⏭️ deferred | require `make setup` (deps); **CI is authoritative**. |

---

## 6. Rollback plan — خطة التراجع

1. **Revert the PR** (`git revert` the merge commit) — `main` returns to the last green SHA.
2. **Redeploy the previous known-good build:**
   - **Railway:** re-trigger `railway_deploy.yml` on the previous `main` commit (auto on merge).
   - **VPS:** re-push the previous `v*.*.*` tag → `deploy.yml` (SSH + `docker compose up -d --build`) → smoke `/health`.
3. **Safety net:** truth labels in `docs/phase-e/00_GO_NO_GO.md` are test-pinned, so a rollback
   cannot silently re-enable live send/charge or cold WhatsApp.
4. **Verify after rollback:** `curl https://api.dealix.me/health` returns 200 with the expected `git_sha`.

---

## 7. First-revenue operating plan — خطة أول إيراد

Sell a **paid outcome**, not "a full platform." Ladder:

1. **Dealix Command Sprint** — 10 days. Output: Diagnostic + Revenue Bottleneck Map +
   AI workflow prototype + Proof Pack. (Rung-0 free Diagnostic → paid Sprint.)
2. **Upsell → Executive Growth OS** — monthly retainer: dashboard + follow-up engine +
   offer system + proof packs + weekly CEO brief.

Anchored to [`docs/commercial/DEALIX_90_DAY_ACTIVATION_PLAN_AR.md`](../commercial/DEALIX_90_DAY_ACTIVATION_PLAN_AR.md)
(arrives with PR #649): Days 0–30 soft pass → 31–60 paid Sprints → 61–90 recurring Growth OS.

**Private-launch cadence (warm only — no cold outreach):**

| Week | Target |
|---|---|
| 1 | 20 warm-list companies contacted |
| 2 | 5 Diagnostics delivered |
| 3 | 2 paid pilots |
| 4 | 1 case / Proof Pack |
| 5–8 | convert pilot → retainer |
| 9–12 | expand offer (Growth OS + Trust OS) |

---

## 8. What this PR does / does not do — ماذا يفعل هذا الـPR

**Does:** adds this decision doc; adds required `JWT_SECRET_KEY` to `.env.example` + the env
contract; retargets stale `VoXc2/dealix` URLs to `Dealix-sa/dealix` across 37 operational/
user-facing files; records honest local gate results.

**Does NOT (founder-only / out of scope):** merge any PR to `main`; add production secrets;
DNS/TLS; Moyasar live; deploy; any external outreach; flip any truth label; weaken any guard;
touch the 4 open PRs; rewrite `@VoXc2` code-owner handles (still the sole admin) or historical
PR/release links (GitHub auto-redirects transferred URLs).
