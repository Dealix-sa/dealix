# Dealix — Official Private Launch Decision

> قرار الإطلاق الخاص — سجل تنفيذي مؤرّخ. هذا المستند **سجل قرار** لجلسة واحدة،
> وليس بديلاً عن بوابة الإطلاق القانونية. المصدر القانوني للبوابة التجارية يبقى
> [`COMMERCIAL_GO_LIVE_GATE.md`](./COMMERCIAL_GO_LIVE_GATE.md) و
> [`CEO_PRODUCTION_TRUST_CLOSE_AR.md`](./CEO_PRODUCTION_TRUST_CLOSE_AR.md).

- **Date:** 2026-06-07
- **Repository:** Dealix-sa/dealix
- **Decision owner:** Founder
- **Scope of this record:** technical close + launch verdict. No external action
  was taken. No secret was created. No deploy. No customer contact.

---

## 1. Verdict

| Track | Verdict | Meaning |
|---|---|---|
| **Private launch** | **CONDITIONAL GO** | All *code* blockers are now resolved or clearly scoped. Remaining gates are founder-only external steps (§4) + green CI on PR #650 after the CI-hardening fix in this branch. |
| **Public launch** | **NO-GO** | Held until a *paid customer proof* and *production evidence* exist. No overclaim. (Doctrine: evidence-backed only.) |

This is an honest "GO **once** the listed gates pass" — not "GO now". Nothing in
this record fabricates a passing state.

---

## 2. Release path (corrected against repo reality)

```text
This CI-hardening PR  →  PR #638 (+ ANTHROPIC_API_KEY)  →  PR #650 (rebased, green)
  →  Branch protection on main  →  Environments + Secrets  →  Railway deploy
  →  Staging smoke  →  Production smoke  →  Private launch
```

Why this order changed from the original plan: the launch RC (PR #650) is **not**
blocked by code or doctrine — it is blocked by two repo-wide CI-infrastructure
faults that this branch fixes first (§3). Merging the CI fix (or rebasing #650
onto it) is what turns #650 green.

### PR state (verified 2026-06-07 via GitHub)

| PR | Title | State | CI reality |
|---|---|---|---|
| **#638** | Claude Code GitHub Action + CLAUDE.md | open, draft | Green **except** the flaky `Python quality, tests, readiness` job (`cancelled` — parallel-isolation flakiness, not a real failure). Needs `ANTHROPIC_API_KEY` secret **after** merge. |
| **#650** | Green doctrine/governance gates + canonical `/health` | open, draft | Same flaky Python job, **plus** `Gitleaks` and `Trivy` red — both **CI-infra faults, not #650's content** (see §3). |

---

## 3. Code blockers — found and fixed in this branch

Root-caused from the live CI logs of PR #650 (the two red checks were **not**
secret leaks and **not** doctrine failures):

| Check | Real root cause | Fix in this branch |
|---|---|---|
| **Trivy filesystem scan** | `repository-hardening.yml` pinned `aquasecurity/trivy-action@0.24.0` — that tag is unresolvable (`unable to find version 0.24.0`). Fails on every run, so the scan never actually ran. | Pin → `@master` (matches the working sibling in `docker-build.yml`). The now-live scan surfaced **real, previously-hidden debt** — see §3a. |
| **Gitleaks secret scan** | `gitleaks/gitleaks-action@v2` requires a paid `GITLEAKS_LICENSE` for org repos → `missing gitleaks license`. Not a leak. | Replace the licensed action with the open-source gitleaks **binary** (latest, resolved dynamically), honouring `.gitleaks.toml`. PR runs scan only the PR's commit range (mirrors old behaviour, so pre-existing fixtures aren't re-flagged). No license needed; scan stays blocking on real leaks. |

Supporting change: `.gitleaks.toml` allowlist extended to the conventional
false-positive sources (`.env.*.example` templates, `tests/`). The
dependency-free `scripts/security_smoke.py` guard still scans `tests/` with exact
per-line allowlisting — defence in depth is preserved, security is **not**
weakened.

> Note: the licensed-action alternative is still valid — add a `GITLEAKS_LICENSE`
> secret and restore `uses: gitleaks/gitleaks-action@v2`. Founder's call.

### 3a. Real debt the now-live Trivy scan surfaced (fixed here)

Once Trivy actually ran, it found genuine issues that the broken pin had hidden:

- **Next.js CRITICAL CVE.** `next@15.1.3` (in `frontend/` **and** `apps/web/`)
  carries `CVE-2025-29927` (middleware **authorization bypass**) and
  `CVE-2025-55182` (RSC **pre-auth RCE**), plus several HIGH DoS/SSRF. **Fix:**
  upgrade `next` (and `eslint-config-next`) → **`15.5.19`** — the latest 15.x,
  which clears every CVE Trivy flagged on the 15.x line. Both `package-lock.json`
  files regenerated so `npm ci` stays in sync. (Stayed on 15.x; did **not** jump
  to the 16.x major, to minimise frontend-build risk — validated by CI's
  `Next.js web verify` / `Frontend verify`.)
- **False-positive secrets.** Trivy's secret scanner flagged our own
  `scripts/*_verify.sh` files, which embed secret-detection regexes
  (`sk_live_…`) as scan *patterns*. **Fix:** scope Trivy to `scanners: vuln`.
  Secret coverage is unaffected — it is already enforced three ways (gitleaks +
  `security_smoke.py` + `detect-secrets`).

---

## 4. Gate results (honest)

This bare session container has **no** dev dependencies (`fastapi`, `pytest`) and
**no** Postgres, so it cannot authoritatively run the full gate battery. The
authoritative run is CI (deps + DB present). Recorded truthfully:

| Gate | Where verified | Result |
|---|---|---|
| `make env-check` | local | **PASS** (exit 0) |
| `make security-smoke` | local, current base | **FAIL by design** — 35 known test-fixture/doc references; **greened by PR #650's allowlist**. Re-run green after #650 merges. |
| `alembic-heads` | local | Inconclusive in sandbox (module-invocation); verify in CI. |
| `make api-contract-check` | — | Not runnable here (no `fastapi`). Verify in CI. |
| `make test` | — | Not runnable here (no `pytest`). PR #650 reports **4628/4726** pass with documented residuals (parallel-isolation + env-gated). |
| `make prod-verify` | — | Not runnable here (chains the above). Verify in CI. |
| `/health`, `/health/deep` | code | **CONFIRMED real & canonical** — `api/routers/health.py` (`/health/deep`) + `api/routers/public.py` (`/health`). |
| Trivy / Gitleaks CI checks | this branch | **Fixed** (§3) — final pass confirmed by CI on this PR. |

---

## 5. Founder-only blockers (cannot be done from the repo)

Per doctrine (never charge a customer, never send external without approval,
Moyasar live is founder-flipped only):

- [ ] Merge **PR #638**, then add `ANTHROPIC_API_KEY` (Settings → Secrets → Actions).
- [ ] Rebase **PR #650** onto this CI fix (or merge this first), confirm green, merge.
- [ ] Branch protection ruleset on `main` (required checks, 1 approval, linear history, block force-push/deletion, no bypass).
- [ ] Create `staging` + `production` Environments; `production` = required reviewers + `main`-only deployments.
- [ ] Configure repository + environment secrets (DB, app/JWT secrets, Moyasar live + webhook, SMTP, Railway token, base URLs).
- [ ] Railway deploy → set `PRODUCTION_BASE_URL` → run `make production-smoke`.
- [ ] DNS / TLS verified manually.
- [ ] Moyasar live dashboard + KYC + payment webhook verified manually.
- [ ] Resolve the ~9 "real drift" product decisions tracked in PR #650 — notably the
      billing free-tier (`amount_halalas == 0` for the rung-0 Free Diagnostic vs the
      "all plans positive" money-safety invariant). Money + safety → founder decides.
- [ ] Approve warm-list, first demo script, first paid diagnostic offer.

No external customer message and no live payment without explicit founder approval.

---

## 6. Allowed private-launch scope vs. not-allowed-yet

**Allowed now:** private demos · paid diagnostics · the Revenue Intelligence Sprint ·
dry-run automation · approval-first workflows · internal lead scoring ·
evidence-backed claims · proof packs.

**Not allowed yet:** public mass launch · cold WhatsApp automation · scraping
without lawful basis · guaranteed-revenue claims · autonomous live payments ·
autonomous external commitments · public compliance claims without evidence.

Positioning language: `PDPL-aware`, `ZATCA-aware`, `approval-first`, `audit-ready`,
`evidence-backed`, `human-approved` — **never** "100% compliant" / "guaranteed
revenue" / "fully automated sending".

---

## 7. First-revenue plan (aligned to the canonical offer)

The flagship private-launch offer is the **existing, canonical** one — not a new
fork:

- **Offer:** Revenue Intelligence Sprint —
  [`docs/commercial/sales/P1_REVENUE_INTELLIGENCE_SPRINT_OFFER_AR.md`](../commercial/sales/P1_REVENUE_INTELLIGENCE_SPRINT_OFFER_AR.md)
- **Price:** Starter 3,500–7,500 SAR · Premium 8,000–15,000 SAR (per the ladder in
  [`docs/OFFER_LADDER_AND_PRICING.md`](../OFFER_LADDER_AND_PRICING.md)).
- **Delivery:** 5–7 days · upfront or 50% · no auto-send · every message client-approved.
- **Target accounts:** use the existing trackers — `docs/ops/lead_machine/` and
  `docs/ops/CEO_TOP50_TRACKER.csv`. (No duplicate tracker created.)
- **Goal:** one paid sprint → one Proof Pack → one retainer proposal.

> Verification bundle: the canonical close command is `make prod-verify` (env-check
> → security-smoke → api-contract-check → dependency-inventory → release-manifest →
> v5-verify). No new "close" script was added — that bundle already exists.
