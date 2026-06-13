# Dealix — Official Private Launch Decision / قرار الإطلاق الخاص الرسمي

- **Date / التاريخ:** 2026-06-07
- **Repository:** `Dealix-sa/dealix`
- **Decision owner / صاحب القرار:** Founder
- **Status / الحالة:** Private Launch — *conditional GO*. Public Launch — **NO-GO**.

> This file is the single decision/verdict layer. It does **not** repeat the
> technical evidence — that lives in `docs/ops/LAUNCH_READINESS_EXECUTION_2026_06_06.md`
> (PR #650). It ties that evidence to a GO/NO-GO decision, the merge path, and
> the founder-only steps.
>
> هذا الملف هو طبقة القرار فقط. الأدلة التقنية موجودة في ملف جاهزية الإطلاق
> (PR #650). هنا نربط الأدلة بقرار GO/NO-GO، ومسار الدمج، والخطوات التي لا
> ينفّذها إلا المؤسس.

---

## 1. Verdict / الحكم

| Track | Verdict | Condition |
|---|---|---|
| **Private Launch** (founder-led demos, paid diagnostics, approval-first dry-runs) | ✅ **GO — conditional** | After the merge path in §3 lands green in CI **and** the founder-only steps in §5 are done. |
| **Public Launch** (paid traffic, public "go-live", autonomous outreach) | ❌ **NO-GO** | Until ≥1 paid customer + real Proof Pack + verified live payment + production monitoring + tested rollback exist. |

Rationale: the no-overclaim doctrine (`dealix/registers/no_overclaim.yaml`) requires
**evidence before claim**. We have engineering readiness signals but **zero paid-customer
proof**, so public claims are not yet earned.

السبب: عقيدة عدم المبالغة تتطلب دليلًا قبل أي ادعاء. لدينا مؤشرات جاهزية هندسية،
لكن **لا يوجد عميل مدفوع بعد**، لذلك الإطلاق العام ممنوع حتى يوجد دليل حقيقي.

---

## 2. Current PR landscape / خريطة الـ PRs الحالية

There are **~10 overlapping open draft launch PRs**. Merging them blindly would
create drift. PR #650 itself flags this (§5.3: *"20 open PRs — mostly overlapping
draft Wave 7/8 / Company OS / launch branches. Consolidate or close."*).

| PR | Title (short) | Role | Recommendation |
|---|---|---|---|
| **#638** | Claude Code GitHub Action + `CLAUDE.md` | Enables `@claude` in PRs/issues; adds `CLAUDE.md`; **also fixes the two pre-existing `repository-hardening.yml` CI failures** (Trivy pin `@0.24.0`→`@master`; gitleaks org-license made non-blocking) | **Merge first** (small, additive: workflow + `CLAUDE.md` + lockfiles) |
| **#650** | Green doctrine/governance CI gates + canonical `/health` | Allowlists *compliant* references (no guard weakened); migrates `/healthz`→`/health` + `/health/deep`; adds readiness evidence doc | **Merge second** (the clean release candidate) |
| #641–#649 | Wave 7/8 / launch / E2E / revenue variants | Overlapping earlier attempts at the same goal | **Triage** — extract any *unique* launch-critical change into #650, then **close the rest** |
| #647 | — | Not open (closed/merged) | n/a |

**Do not** merge all of #641–#650. Pick **one** path: #638 → #650, then close the
overlapping cluster after diffing for uniques.

---

## 3. Recommended single merge path / مسار الدمج الموصى به

```text
1. #638  →  Claude Code workflow + CLAUDE.md         (after ANTHROPIC_API_KEY secret is set)
2. #650  →  doctrine gates green + canonical /health  (the release candidate)
3. Triage #641–#649 → cherry-pick any unique launch-critical change into #650, then close.
4. Resolve the P0 money-safety decision in §4 BEFORE relying on billing/checkout.
```

All merges require: green CI on the merge head, branch protection (§5), and 1 review.

---

## 4. Open product decision — P0 money-safety / قرار منتج عالق

PR #650 surfaced a real conflict that an agent must **not** guess:

- Doctrine: **rung-0 Free Diagnostic = 0 SAR**.
- Safety invariant in tests: **"no plan charges 0 halalas."**

These collide in the chargeable `PLANS` map. **Decision required:** does the Free
Diagnostic live in a separate *non-chargeable* catalog, or in `PLANS` with an
explicit free-tier exception? Then align `tests/test_billing_amounts.py` +
`tests/test_billing_moyasar_safety.py`. **Owner: Founder/PM.** Until resolved,
do not enable live checkout.

---

## 5. Founder-only blockers / ما لا ينفّذه إلا المؤسس

These **cannot** and **must not** be done by an agent or from the repo (doctrine:
never charge a customer, never send external without approval, Moyasar live is
founder-flipped only). Tracked as issues **#467–#471** and detailed in PR #650 §4.

- [ ] **GitHub Secrets** — add `ANTHROPIC_API_KEY` (+ the production set) under
      *Settings → Secrets and variables → Actions*. **Never commit secrets.**
      See `docs/ops/PRODUCTION_SECRETS_CHECKLIST.md`.
- [ ] **Branch protection** — enable a ruleset on `main` (require PR + 1 review +
      status checks + linear history + block force-push/deletions + no bypass).
- [ ] **Environments** — create `staging` and `production`; on `production` set
      required reviewers, prevent self-review, restrict deploy branch to `main`.
- [ ] **DNS/TLS** — verify `api.dealix.me` live in the DNS/host dashboard.
- [ ] **Moyasar live** — complete KYC (`docs/ops/MOYASAR_KYC_CHECKLIST.md`), then
      `python scripts/moyasar_live_cutover.py` (founder-only), verify webhook.
- [ ] **Railway deploy** — `railway up` from the linked project (founder-only).
- [ ] **Warm-list outreach** — fill `data/warm_list.csv`, generate **drafts only**
      via `python scripts/warm_list_outreach.py`; **nothing is sent without approval.**

---

## 6. Gate evidence measured this session / الأدلة المقيسة في هذه الجلسة

Run on the session branch tip (`claude/busy-lamport-az7ZF`, based on `#559`).
**CI on the merge head is the authoritative runner.**

| Gate | Result here | Note |
|---|---|---|
| `make env-check` | ✅ pass | Backend + frontend env contracts OK |
| `make security-smoke` | ⚠️ red on this older tip | Flags committed `.env.*.example` + secret-*prefix* patterns in test fixtures/docs. PR #650 reports `security_smoke.py` exit 0 on its head after **compliant-context allowlisting** (no real secrets). |
| `/health`, `/health/deep` | ✅ exist | Canonical in `api/routers/health.py`; #650 migrates landing refs off `/healthz`. |
| `make api-contract-check` | ⛔ inconclusive here | Needs `fastapi` (not installed in this ephemeral sandbox) → run in CI. |
| `make alembic-heads` | ⛔ inconclusive here | Needs `alembic` runnable → #650 reports a single head (`013`) in CI. |
| `make prod-verify` | ⛔ run in CI | Bundle needs app deps; CI / a full env is authoritative. |

> **CI note (PR #651):** the `Trivy filesystem scan` and `Gitleaks secret scan`
> checks fail **repo-wide** (Trivy pins a non-existent `aquasecurity/trivy-action@0.24.0`;
> gitleaks-action@v2 needs a `GITLEAKS_LICENSE` org secret). Both are **already fixed
> by PR #638** (Trivy → `@master` + `skip-files`; gitleaks → `continue-on-error` +
> license env). They are not introduced by this PR and need no change here.

Convenience: `scripts/dealix_close_now.sh` runs the canonical gates and prints this
founder checklist (read-only; never deploys/charges/sends).

---

## 7. Allowed vs. not-allowed in private launch / المسموح والممنوع

**Allowed / مسموح:** private demos · paid diagnostics · the Command Sprint
(`sales/COMMAND_SPRINT_OFFER.md`) · approval-first dry-runs · internal lead
scoring · evidence-backed claims · Proof Packs.

**Not allowed yet / ممنوع حتى الآن:** public mass launch · cold WhatsApp automation ·
scraping without lawful basis · guaranteed-revenue claims · autonomous live payments ·
autonomous external commitments · public compliance claims without evidence.

---

## 8. Existing assets to use (do NOT duplicate) / أصول موجودة تُستخدم ولا تُكرَّر

- Go-live gate: `docs/ops/COMMERCIAL_GO_LIVE_GATE.md`
- Readiness evidence (PR #650): `docs/ops/LAUNCH_READINESS_EXECUTION_2026_06_06.md`
- No-overclaim register: `dealix/registers/no_overclaim.yaml`
- Secrets checklist: `docs/ops/PRODUCTION_SECRETS_CHECKLIST.md`
- Prospect lists: `docs/ops/pipeline_tracker.csv`, `pipeline_tracker_enriched.csv`
- Execution tracker: `docs/ops/CEO_TOP50_TRACKER.csv`
- Rollback: `docs/ops/ROLLBACK_RUNBOOK.md`
- Sales OS: `docs/29_sales_os/` (proposals, objection handling), `docs/26_service_catalog/`

---

## 9. Rollback plan / خطة الرجوع

Use `docs/ops/ROLLBACK_RUNBOOK.md`. Summary: disable the production workflow →
revert the release commit → disable checkout/payment entry points → rotate impacted
secrets → freeze outbound workflows → publish an internal incident note → restore
last-known-good deployment.

---

## 10. What the agent did vs. founder-only / ما نفّذه الوكيل مقابل المؤسس

**Agent did (on branch `claude/busy-lamport-az7ZF`):** reconnaissance of repo +
PRs, measured the local gates above, and authored three complementary artifacts —
this decision file, `scripts/dealix_close_now.sh`, and `sales/COMMAND_SPRINT_OFFER.md`.

**Agent did NOT (founder-only / out of scope):** merge any PR, push to `main`, add
secrets, set branch protection, create environments, deploy to Railway, flip Moyasar
live, or send any outreach. See §5.

_Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة._
